import pytest
import uuid
import json
from unittest.mock import patch
from azure.functions.servicebus import ServiceBusMessage
from _testutils.mocks import ServiceBusClient
from _testutils import states
from . import main as dispatch


@pytest.fixture
def payload():
    return {
        'source_thread_id': 'a2d57c7203b145a59ac44ba3e0f08309',
        'source_type': 'support',
        'body': 'Hello Test!',
        'info': {'username': 'Janis'},
        'thread_ts': None
    }


@pytest.fixture
def msg(payload):
    return ServiceBusMessage(
        body=json.dumps(payload).encode(),
        message_id=uuid.uuid4().hex,
        user_properties={}
    )


@patch("_core.service_bus.ServiceBusClient", ServiceBusClient)
def test_function(msg):
    dispatch(msg)
    assert states.LAST_SEND_MESSAGE is not None
