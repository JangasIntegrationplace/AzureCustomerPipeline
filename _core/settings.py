import os
from _core.integrations.pipelines import settings as pipeline_settings
from .cosmosdb_handler import CosmosDBHandler

COSMOSDB_CONNECTION_STRING = os.getenv("COSMOSDB_CONNECTION_STRING")
COSMOSDB_DATABASE_NAME = os.getenv("COSMOSDB_DATABASE_NAME")
SERVICE_BUS_CONNECTION_STRING = os.getenv("SERVICE_BUS_CONNECTION_STRING")

pipeline_settings.DB_HANDLER = CosmosDBHandler
