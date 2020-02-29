import base64

import pika


class RabbitMQDriver:
    SCHEME = 'rabbitmq'
    _DEFAULT_EXCHANGE = ''

    def __init__(self, url):
        self._url = url
        self._connection_params = pika.ConnectionParameters(
            host=url.host,
            port=url.port
        )
        self._init_connection()

    def _init_connection(self):
        self._conn = pika.BlockingConnection(self._connection_params)
        self._channel = self._conn.channel()

    def publish(self, tag, message):
        self._channel.queue_declare(queue=tag)
        self._channel.basic_publish(exchange=self._DEFAULT_EXCHANGE,
                                    routing_key=tag,
                                    body=message)
        print(tag, message)

    def register_consumer(self, tag, callback):
        self._channel.queue_declare(queue=tag)

        def _consume_callback(channel, method, properties, body):
            message = body.decode()
            callback(message)

        self._channel.basic_consume(
            queue=tag,
            auto_ack=True,  # TODO: move to config
            on_message_callback=_consume_callback
        )

    def start_consuming(self):
        self._channel.start_consuming()
