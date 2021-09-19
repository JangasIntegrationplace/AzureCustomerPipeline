import json
import azure.functions as func
import requests
from _core.settings import init_submodules, WEB_ENDPOINTS
from _core.integrations.pipelines import ReversedDispatchController


init_submodules()
REQUIRED_MSG_FIELDS = ("body", "thread_ts", )


class Controller(ReversedDispatchController):
    def handler(self):
        super().handler()
        request_data = {
            "source_thread_id": self.data.source_thread_id,
            "body": self.data.body
        }
        if self.data.source_type == "support":
            requests.post(url=WEB_ENDPOINTS["support"], data=request_data)
        else:
            raise ValueError("Source Type not implemented yet.")


def main(msg: func.ServiceBusMessage):
    payload = json.loads(msg.get_body())
    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]

    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data=payload)
    controller.handler()
