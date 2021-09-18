import json
import logging
import azure.functions as func
from dataclasses import dataclass
from datetime import datetime

from _core.integrations.pipelines import InputStreamController
from _core.integrations.pipelines.controller import BaseBO

logger = logging.getLogger(__name__)


@dataclass
class Sample(BaseBO):
    id: int
    description: str


@dataclass
class ReviewBO(BaseBO):
    id: int
    author: str
    body: str
    timestamp: datetime.date
    sample: Sample


class Controller(InputStreamController):
    business_object = ReviewBO


def main(msg: func.ServiceBusMessage):
    data = json.loads(msg.get_body())
    controller = Controller(data=data)
    controller.handler()
