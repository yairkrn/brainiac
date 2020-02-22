import contextlib
import pathlib
import threading

from ..server.data_types import ServerSnapshot, ServerColorImage, ServerDepthImage, ServerFeelings, ServerRotation,\
    ServerTranslation
from ..message_queue.data_types import MessageQueueProduct
from ..config import config
from ..parser import parser
from ..protocol.data_types import ProtocolHello, ProtocolConfig, ProtocolSnapshot
from ..utils import Listener


class ClientHandler(threading.Thread):
    TIME_FORMAT = '%Y-%m-%d_%H-%M-%S-%f'
    SNAPSHOT_FILENAME = config['server-snapshot-filename']
    lock = threading.Lock()

    class Context:
        def __init__(self, directory):
            self.directory = directory

    def __init__(self, conn, publish):
        super().__init__()
        self._conn = conn
        self._publish = publish
        self._data_dir = pathlib.Path(config['server-local-dir'])

    def _get_user_dir(self, user_id, timestamp):
        formatted_time = timestamp.strftime(self.TIME_FORMAT)
        user_dir = self._data_dir / str(user_id) / formatted_time
        user_dir.mkdir(parents=True, exist_ok=True)
        return user_dir

    def _save_product(self, user_id, timestamp, product_name, product):
        user_dir = self._get_user_dir(user_id, timestamp)
        product_file = user_dir / product_name
        product_file.write_bytes(product)
        return product_file

    def _get_product_message(self, user_id, timestamp, product_name, product):
        product_path = self._save_product(user_id, timestamp, product_name, product)
        return MessageQueueProduct(user_id, timestamp.strftime(self.TIME_FORMAT), str(product_path))

    @classmethod
    def message_queue_products_from_protocol_snapshot(cls, snapshot, fields):
        products = {}
        if 'translation' in fields:
            products['translation'] = ServerTranslation.build(
                dict(x=snapshot.translation.x,
                     y=snapshot.translation.y,
                     z=snapshot.translation.z))
        if 'rotation' in fields:
            products['rotation'] = ServerRotation.build(
                dict(x=snapshot.rotation.x,
                     y=snapshot.rotation.y,
                     z=snapshot.rotation.z,
                     w=snapshot.rotation.w))
        if 'color_image' in fields:
            products['color_image'] = ServerColorImage.build(
                dict(h=snapshot.color_image.h,
                     w=snapshot.color_image.w,
                     colors=snapshot.color_image.colors))
        if 'depth_image' in fields:
            products['depth_image'] = ServerDepthImage.build(
                dict(h=snapshot.depth_image.h,
                     w=snapshot.depth_image.w,
                     depths=snapshot.depth_image.depths))
        if 'feelings' in fields:
            products['feelings'] = ServerFeelings.build(
                dict(hunger=snapshot.feelings.hunger,
                     thirst=snapshot.feelings.thirst,
                     exhaustion=snapshot.feelings.exhaustion,
                     happiness=snapshot.feelings.happiness))
        return products

    def run(self):
        # receive an Hello message
        hello = ProtocolHello.parse(self._conn.receive_message())

        # send back a Config message
        self._conn.send_message(
            ProtocolConfig.build(
                dict(supported_fields_number=len(parser.supported_fields),
                     supported_fields=parser.supported_fields)
            )
        )

        # receive a Snapshot message
        snapshot = ProtocolSnapshot.parse(self._conn.receive_message())

        # publish the messages
        products = self.message_queue_products_from_protocol_snapshot(snapshot, parser.supported_fields)
        for name, product in products.items():
            product_message = self._get_product_message(hello.user_id, snapshot.timestamp, name, product)
            self._publish(product_message, 'parsers', name)  # TODO: refactor

        # TODO: move to parsers microservice
        # parse the snapshot
        context = self.Context(
            self._get_user_dir(hello.user_id, snapshot.timestamp))
        parser.parse(context, snapshot)


def run_server(host, port, publish):
    with Listener(host=host, port=port, backlog=config['server-backlog']) as listener:
        with contextlib.suppress(KeyboardInterrupt):
            while True:
                client_connection = listener.accept()
                ClientHandler(client_connection, publish).start()
