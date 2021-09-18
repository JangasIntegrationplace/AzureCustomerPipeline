import json
import azure.functions as func
from _core.integrations.pipelines import OutputStreamController
from _core.settings import SLACK_CHANNELS


REQUIRED_MSG_FIELDS = ("source_thread_id", "source_type", "body", "info", "thread_ts", )


class Controller(OutputStreamController):
    def get_channel(self):
        if self.data.source_type == "support":
            return SLACK_CHANNELS["support"]
        else:
            raise ValueError("Message Not supported yet")


def main(msg: func.ServiceBusMessage):
    payload = json.loads(msg.get_body())

    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]
    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data=payload)
    controller.handler()
