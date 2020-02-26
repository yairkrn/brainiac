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

    def publish(self, message, tag):
        self._channel.queue_declare(queue=tag)
        self._channel.basic_publish(exchange=self._DEFAULT_EXCHANGE,
                                    routing_key=tag,
                                    body=message)
        # TODO: implement, might need more parameters
        print(tag, message)
