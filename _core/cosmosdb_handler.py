from _core.integrations.pipelines.db_handler import BaseHandler
from _core.integrations.pipelines.business_objects import (
    InitialInputData,
    SlackOutboundMessageData
)
from .cosmosdb import CosmosDB


class CosmosDBHandler(BaseHandler):
    @classmethod
    def create_initial_input(cls, data: InitialInputData):
        container = CosmosDB.get().get_container("initial_input", "/msg")
        container.upsert_item({
            "id": data.msg_id,
            "msg": data.msg_id,
            "payload": data.payload
        })

    @classmethod
    def retrieve_slack_thread(cls, source_thread_id):
        container = CosmosDB.get().get_container("output", "/source_thread_id")
        query = f'SELECT o.thread_ts FROM output o WHERE o.id="{source_thread_id}"'
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return None if len(items) == 0 else items[0]

    @classmethod
    def create_output_stream(cls, data: SlackOutboundMessageData):
        container = CosmosDB.get().get_container("output", "/source_thread_id")
        container.upsert_item({
            "id": data.source_thread_id,
            "source_thread_id": data.source_thread_id,
            "thread_ts": data.thread_ts,
            "source_type": data.source_type,
            "info": data.info,
            "channel": data.channel,
            "text": data.text
        })

        container = CosmosDB.get().get_container("identify", "/thread_ts")
        container.upsert_item({
            "id": data.thread_ts,
            "source_thread_id": data.source_thread_id,
            "thread_ts": data.thread_ts,
            "source_type": data.source_type,
            "channel": data.channel
        })

    @classmethod
    def retrieve_slack_thread_by_thread_ts(cls, thread_ts):
        container = CosmosDB.get().get_container("identify", "/thread_ts")
        query = f'SELECT i.source_thread_id, i.source_type FROM identify i WHERE i.id="{thread_ts}"'
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        return None if len(items) == 0 else items[0]
