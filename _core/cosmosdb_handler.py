from _core.integrations.pipelines.db_handler import BaseHandler
from _core.integrations.pipelines.business_objects import (
    InitialInputData,
    SlackOutboundMessageData
)
from .cosmosdb import cosmosdb


class CosmosDBHandler(BaseHandler):
    def create_initial_input(cls, data: InitialInputData):
        container = cosmosdb.get_container("initial_input", "/msg")
        container.upsert_item({"id": data.msg_id, "payload": data.payload})

    def retrieve_slack_thread(cls, source_thread_id):
        container = cosmosdb.get_container("output", "/source_thread_id")
        query = f'SELECT o.thread_ts FROM output o WHERE o.id="{source_thread_id}"'
        items = list(container.query_items(query=query))
        return None if len(items) == 0 else items[0]

    def create_output_stream(cls, data: SlackOutboundMessageData):
        container = cosmosdb.get_container("output", "/source_thread_id")
        container.upsert_item({
            "id": data.source_thread_id,
            "source_type": data.source_type,
            "info": data.info,
            "channel": data.channel,
            "text": data.text,
            "thread_ts": data.thread_ts,
        })
