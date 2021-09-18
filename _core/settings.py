import os
from _core.integrations.pipelines import settings as pipeline_settings
from .cosmosdb_handler import CosmosDBHandler
from dotenv import load_dotenv

load_dotenv()


COSMOSDB_CONNECTION_STRING = os.getenv("COSMOSDB_CONNECTION_STRING")
COSMOSDB_DATABASE_NAME = os.getenv("COSMOSDB_DATABASE_NAME")
SERVICE_BUS_CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")

SLACK_CHANNELS = {
    "support": os.getenv("SLACK_SUPPORT_CHANNEL"),
}

pipeline_settings.DB_HANDLER = CosmosDBHandler
pipeline_settings.SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
