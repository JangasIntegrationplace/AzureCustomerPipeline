import pytest
import uuid
import json
from unittest.mock import patch
from azure.functions.servicebus import ServiceBusMessage
from _testutils.mocks import ServiceBusClient, CosmosClient
from _testutils import states
from . import main as get_slack_thread


@pytest.fixture
def payload():
    return {
        'source_thread_id': 'a2d57c7203b145a59ac44ba3e0f08309',
        'source_type': 'support',
        'body': 'Hello Test!',
        'info': {'username': 'Janis'},
    }


@pytest.fixture
def msg(payload):
    return ServiceBusMessage(
        body=json.dumps(payload).encode(),
        message_id=uuid.uuid4().hex,
        user_properties={}
    )


@patch("_core.service_bus.ServiceBusClient", ServiceBusClient)
# @patch("_core.cosmosdb.CosmosClient", CosmosClient)
def test_function(msg):
    get_slack_thread(msg)
    assert states.LAST_SEND_MESSAGE is not None
