import logging
import json

import azure.functions as func
from azure.servicebus import ServiceBusMessage

from _core.settings import init_submodules
from _core.cosmosdb_handler import CosmosDBHandler
from _core.service_bus import ServiceBus

init_submodules()


def main(req: func.HttpRequest):
    logging.info('Python HTTP trigger function processed a request.')

    req_body = req.get_json()

    if req_body["type"] == "url_verification":
        return func.HttpResponse(
            json.dumps({"challenge": req_body["challenge"]}),
            status_code=200
        )

    event_id = req_body["event_id"]
    event = req_body["event"]
    if event["type"] != "message":
        return func.HttpResponse(
            json.dumps({"challenge": event_id}),
            status_code=200
        )

    if "thread_ts" not in event:
        return func.HttpResponse(
            json.dumps({"challenge": event_id}),
            status_code=200
        )

    if not event["text"].startswith("*send* "):
        return func.HttpResponse(
            json.dumps({"challenge": event_id}),
            status_code=200
        )

    thread = CosmosDBHandler.retrieve_slack_thread_by_thread_ts(event["thread_ts"])
    if thread is None:
        return func.HttpResponse(
            json.dumps({"challenge": event_id}),
            status_code=200
        )
    logging.info("Message found to proceed to web.")

    message = {
        "thread": thread["source_thread_id"],
        "user": {"username": "slack"},
        "body": event["text"].lstrip("*send* "),
        "source_type": thread["source_type"],
        "send_by_user": False
    }

    msg = ServiceBusMessage(body=json.dumps(message))

    ServiceBus.get().queue_sender(message=msg, queue="dispatch_message_to_client")
    logging.info("Message sent.")

    return func.HttpResponse(
        json.dumps({"challenge": event_id}),
        status_code=200
    )
