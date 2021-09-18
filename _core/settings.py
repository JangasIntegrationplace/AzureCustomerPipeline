import os
from _core.integrations.pipelines import settings as pipeline_settings
from .cosmosdb import CosmosDBHandler

COSMOSDB_CONNECTION_STRING = os.getenv("COSMOSDB_CONNECTION_STRING")
COSMOSDB_DATABASE_NAME = os.getenv("COSMOSDB_DATABASE_NAME")

pipeline_settings.DB_HANDLER = CosmosDBHandler
