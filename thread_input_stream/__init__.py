import json
import azure.functions as func
from _core.cosmosdb_handler import InitialInputData
from _core.integrations.pipelines import InputStreamController


class Controller(InputStreamController):
    def process_data(self):
        self.data = InitialInputData(
            id=self.data["msg_id"], payload=self.data["payload"]
        )

    def handler(self):
        super().handler()
        # Send to other topic


def main(msg: func.ServiceBusMessage):
    msg_id = msg.message_id
    payload = json.loads(msg.get_body())
    controller = Controller(data={"msg_id": msg_id, "payload": payload})
    controller.handler()
