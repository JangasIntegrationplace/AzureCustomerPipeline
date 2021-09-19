import pytest
import uuid
import json
from unittest.mock import patch
from azure.functions.servicebus import ServiceBusMessage
from _testutils.mocks import ServiceBusClient, CosmosClient
from _testutils import states
from . import main as content_input_stream


@pytest.fixture
def payload():
    return {
        "source_thread_id": "6870f642-1969-11ec-9e1e-0242c0a89004",
        "body": "This should be proceed from unittest!",
        "info": {
            "username": "azure",
            "email": "azure@outlook.com"
        },
    }


@pytest.fixture
def msg(payload):
    return ServiceBusMessage(
        body=json.dumps(payload).encode(),
        label="support",
        message_id=uuid.uuid4().hex,
        user_properties={}
    )


@patch("_core.service_bus.ServiceBusClient", ServiceBusClient)
@patch("_core.cosmosdb.CosmosClient", CosmosClient)
def test_function(msg):
    content_input_stream(msg)
    assert states.LAST_UPSERT_ITEM is not None
    assert states.LAST_SEND_MESSAGE is not None
