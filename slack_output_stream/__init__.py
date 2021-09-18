import json
import azure.functions as func
from _core.integrations.pipelines.business_objects import SlackOutboundMessageData
from _core.integrations.pipelines import OutputStreamController, Slack
from _core.settings import SLACK_BOT_TOKEN, SLACK_CHANNELS


REQUIRED_MSG_FIELDS = ("source_thread_id", "source_type", "body", "info", "thread_ts", )


class Controller(OutputStreamController):
    def process_data(self):
        self.data = SlackOutboundMessageData(
            source_thread_id=self.data["source_thread_id"],
            source_type=self.data["source_type"],
            info=self.data["info"],
            text=self.data["text"],
            channel=self.data["channel"],
            thread_ts=self.data["thread_ts"]
        )

    def handler(self):
        if self.data.source_type == "support":
            channel = SLACK_CHANNELS["support"]
        else:
            raise ValueError("Message Not supported yet")

        json_info = json.dumps(self.data["info"], indent=True)
        text = (
            "**New Thread**\n\n"
            f"**Info**\n{json_info}\n\n"
            f"**text**\n{self.data['body']}"
        )

        slack_message = Slack.post_message(
            self.data.channel, self.data.text,
            slack_bot_token=SLACK_BOT_TOKEN,
            thread_ts=self.data.thread_ts
        )

        thread_ts = self.data.get("thread_ts", slack_message.data["ts"])

        modified_data = {
            "source_thread_id": self.data["source_thread_id"],
            "source_type": self.data["source_type"],
            "info": self.data["info"],
            "text": text,
            "channel": channel,
            "thread_ts": thread_ts
        }
        self.data = modified_data
        super().handler()


def main(msg: func.ServiceBusMessage):
    payload = json.loads(msg.get_body())

    missing_fields = [field for field in REQUIRED_MSG_FIELDS if field not in payload]
    if len(missing_fields) > 0:
        raise KeyError(f"Missing Fields in Payload: {missing_fields}")

    controller = Controller(data=payload)
    controller.handler()
