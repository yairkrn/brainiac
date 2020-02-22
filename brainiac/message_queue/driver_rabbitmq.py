import pika


class RabbitMQDriver:
    SCHEME = 'rabbitmq'

    def __init__(self, url):
        self._url = url
        self._connection_params = pika.ConnectionParameters(
            host=url.host,
            port=url.port
        )

    def _init_connection(self):
        self._conn = pika.BlockingConnection(self._connection_params)
        self._channel = self._conn.channel()

    def publish(self, message, exchange, routing_key):
        # TODO: implement, might need more parameters
        print(exchange, routing_key, message)
