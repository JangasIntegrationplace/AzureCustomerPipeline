from azure.cosmos import CosmosClient, PartitionKey, exceptions
from .settings import COSMOSDB_CONNECTION_STRING, COSMOSDB_DATABASE_NAME


class CosmosDB:
    def __init__(self, connection_string: str, db_name: str):
        self.client = CosmosClient.from_connection_string(connection_string)
        self.db_client = self.client.get_database_client(db_name)
        self.get_container("initial_input", "/msg")
        self.get_container("output", "/msg")

    def get_container(self, container_name, partition_key_path):
        try:
            return self.db_client.create_container(
                id=container_name,
                partition_key=PartitionKey(path=partition_key_path)
            )
        except exceptions.CosmosResourceExistsError:
            return self.db_client.get_container_client(container_name)


cosmosdb = CosmosDB(COSMOSDB_CONNECTION_STRING, COSMOSDB_DATABASE_NAME)
