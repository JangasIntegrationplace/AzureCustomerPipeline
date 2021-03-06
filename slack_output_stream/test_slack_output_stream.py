import pytest
import uuid
import json
from unittest.mock import patch
from azure.functions.servicebus import ServiceBusMessage
from _testutils.mocks import CosmosClient, SlackWebClient
from _testutils import states
from . import main as slack_output_stream


@pytest.fixture
def payload():
    return {
        'source_thread_id': 'a2d57c7203b145a59ac44ba3e0f08309',
        'source_type': 'support',
        'body': 'Hello Test!',
        'info': {'username': 'Janis'},
        'thread_ts': '1632072487.056900'
    }


@pytest.fixture
def msg(payload):
    return ServiceBusMessage(
        body=json.dumps(payload).encode(),
        message_id=uuid.uuid4().hex,
        user_properties={}
    )


# @patch("_core.cosmosdb.CosmosClient", CosmosClient)
# @patch("_core.integrations.pipelines.slack.WebClient", SlackWebClient)
def test_function(msg):
    slack_output_stream(msg)
    assert states.LAST_SEND_SLACK_MESSAGE is not None
    assert states.LAST_UPSERT_ITEM is not None
