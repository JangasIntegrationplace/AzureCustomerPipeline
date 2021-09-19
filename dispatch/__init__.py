import json
import azure.functions as func
from _core.settings import init_submodules
from azure.servicebus import ServiceBusMessage
from _core.integrations.pipelines import DispatchController
from _core.service_bus import ServiceBus


init_submodules()
REQUIRED_MSG_FIELDS = ("source_thread_id", "source_type", "body", "info", "thread_ts", )


class Controller(DispatchController):
    def handler(self):
        # TODO: Workflow here is bad. Maybe refactor
        self.process_data()
        dispatch_message = {
            "source_thread_id": self.data.source_thread_id,
            "source_type": self.data.source_type,
            "body": self.data.body,
            "info": self.data.info,
            "thread_ts": self.data.thread_ts
        }
        msg = ServiceBusMessage(body=json.dumps(dispatch_message))
        if self.data.thread_ts:
            ServiceBus.get().queue_sender(msg, queue="slack_outbound")
        elif self.data.source_type == "support":
            ServiceBus.get().queue_sender(msg, queue="slack_outbound")
        else:
            raise ValueError(
                f"Source Type {self.data.source_type} is not supported yet."
            )


def main(msg: func.ServiceBusMessage):
    payload = json.loads(msg.get_body())
    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]

    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data=payload)
    controller.handler()
