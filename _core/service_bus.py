from azure.servicebus import ServiceBusClient, ServiceBusMessage


class ServiceBus:
    instance: "ServiceBus" = None

    @classmethod
    def get(cls):
        if not cls.instance:
            # again - brrrrr... hacky and ugly and unsecure
            from .settings import SERVICE_BUS_CONNECTION_STRING
            cls.instance = ServiceBus(SERVICE_BUS_CONNECTION_STRING)
        return cls.instance

    def __init__(self, connection_string: str):
        self.client = ServiceBusClient.from_connection_string(connection_string)

    def queue_sender(self, message: ServiceBusMessage, *, queue: str):
        with self.client as client:
            with client.get_queue_sender(queue) as sender:
                sender.send_messages(message)

    def topic_sender(self, message: ServiceBusMessage, *, topic: str):
        with self.client as client:
            with client.get_topic_sender(topic) as sender:
                sender.send_messages(message)
