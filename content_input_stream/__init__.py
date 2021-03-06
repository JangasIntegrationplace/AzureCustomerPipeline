import json
import azure.functions as func
from azure.servicebus import ServiceBusMessage
from _core.settings import init_submodules
from _core.integrations.pipelines.business_objects import InitialInputData
from _core.integrations.pipelines import InputStreamController
from _core.service_bus import ServiceBus


init_submodules()
REQUIRED_MSG_FIELDS = ("source_thread_id", "body", "info", )


class Controller(InputStreamController):
    def process_data(self):
        self.data = InitialInputData(
            source_thread_id=self.data["payload"]["source_thread_id"],
            source_type=self.data["source_type"],
            body=self.data["payload"]["body"],
            info=self.data["payload"]["info"],
            msg_id=self.data["msg_id"],
            payload=self.data["payload"]
        )

    def handler(self):
        super().handler()
        get_slack_thread_message = {
            "source_thread_id": self.data.source_thread_id,
            "source_type": self.data.source_type,
            "body": self.data.body,
            "info": self.data.info,
        }
        msg = ServiceBusMessage(body=json.dumps(get_slack_thread_message))
        ServiceBus.get().queue_sender(msg, queue="slack_threads")


def main(msg: func.ServiceBusMessage):
    msg_id, msg_label = msg.message_id, msg.label
    payload = json.loads(msg.get_body())
    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]

    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data={
        "msg_id": msg_id,
        "source_type": msg_label,
        "payload": payload
    })
    controller.handler()
