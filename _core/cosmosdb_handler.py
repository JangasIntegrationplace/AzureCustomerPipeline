from _core.integrations.pipelines.db_handler import BaseHandler
from dataclasses import dataclass
from .cosmosdb import cosmosdb


@dataclass
class InitialInputData:
    msg_id: str
    payload: dict


class CosmosDBHandler(BaseHandler):
    def create_initial_input(cls, data: InitialInputData):
        container = cosmosdb.get_container("initial_input", "/msg")
        container.upsert_item(id=data.msg_id, payload=data.payload)

    def create_output_stream(cls, data: dict):
        # container = cosmosdb.get_container("output", "/msg")
        pass
