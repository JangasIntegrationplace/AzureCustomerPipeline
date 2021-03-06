import uuid
from . import states


class ServiceBusSender:
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return

    @classmethod
    def send_messages(cls, message, **kwargs):
        states.LAST_SEND_MESSAGE = message


class ServiceBusClient:
    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        return

    @classmethod
    def from_connection_string(cls, conn_str, **kwargs):
        return cls()

    def get_queue_sender(self, queue_name, **kwargs):
        return ServiceBusSender()


class ContainerProxy:
    def __init__(self, database, *args, **kwargs):
        self.database = database

    def upsert_item(self, body):
        states.LAST_UPSERT_ITEM = {"body": body, "database": self.database}

    def query_items(self, query, *args, **kwars):
        return []


class DatabaseProxy:
    def __init__(self, database, *args, **kwargs):
        self.database = database

    def create_container(self, *args, **kwargs):
        return ContainerProxy(database=self.database, *args, **kwargs)

    def get_container_client(self, *args, **kwargs):
        return ContainerProxy(database=self.database, *args, **kwargs)


class CosmosClient:
    @classmethod
    def from_connection_string(cls, conn_str, **kwargs):
        return cls()

    def get_database_client(self, database):
        return DatabaseProxy(database)


class SlackResponse:
    def __init__(self, action: str, json: dict):
        self.data = {
            "ts": uuid.uuid4().hex
        }


class SlackWebClient:
    def __init__(self, token, *args, **kwargs):
        pass

    def chat_postMessage(self, channel, text, thread_ts, *args, **kwargs):
        data = {
            "channel": channel,
            "text": text,
            "thread_ts": thread_ts,
        }
        states.LAST_SEND_SLACK_MESSAGE = data
        return SlackResponse("chat.postMessage", json=data)
