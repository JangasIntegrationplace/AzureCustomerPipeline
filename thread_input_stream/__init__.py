import json
import azure.functions as func
from azure.servicebus import ServiceBusMessage
from _core.integrations.pipelines.business_objects import InitialInputData
from _core.integrations.pipelines import InputStreamController
from _core.service_bus import service_bus


class Controller(InputStreamController):
    def process_data(self):
        self.data = InitialInputData(
            id=self.data["msg_id"],
            payload=self.data["payload"],
            source=self.data["msg_label"]
        )

    def handler(self):
        super().handler()
        get_or_create_slack_thread_message = {
            "msg_id": self.data.msg_id,
            "payload": self.data.payload,
            "source": self.data.source
        }
        msg = ServiceBusMessage(body=json.dumps(get_or_create_slack_thread_message))
        service_bus.topic_sender(msg, topic="unknown_slack_threads")


def main(msg: func.ServiceBusMessage):
    msg_id, msg_label = msg.message_id, msg.label
    payload = json.loads(msg.get_body())
    controller = Controller(data={
        "msg_id": msg_id,
        "msg_label": msg_label,
        "payload": payload
    })
    controller.handler()
