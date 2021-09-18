import json
import azure.functions as func
from azure.servicebus import ServiceBusMessage
from _core.integrations.pipelines.business_objects import GetSlackThreadData
from _core.integrations.pipelines import GetSlackThreadController
from _core.service_bus import service_bus


REQUIRED_MSG_FIELDS = ("source_thread_id", "source_type", "body", "info", )


class Controller(GetSlackThreadController):
    def process_data(self):
        self.data = GetSlackThreadData(
            source_thread_id=self.data["source_thread_id"],
            source_type=self.data["source_type"],
            body=self.data["body"],
            info=self.data["info"]
        )

    def handler(self):
        # TODO Check thread ts type. It should be flat string.
        thread_ts = super().handler()
        dispatch_message = {
            "source_thread_id": self.data.source_thread_id,
            "source_type": self.data.source_type,
            "body": self.data.body,
            "info": self.data.info,
            "thread_ts": thread_ts,
        }
        msg = ServiceBusMessage(body=json.dumps(dispatch_message))
        service_bus.queue_sender(msg, queue="dispatch")


def main(msg: func.ServiceBusMessage):
    payload = json.loads(msg.get_body())

    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]
    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data=payload)
    controller.handler()
