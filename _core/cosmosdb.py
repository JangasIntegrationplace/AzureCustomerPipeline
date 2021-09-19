from azure.cosmos import CosmosClient, PartitionKey, exceptions


class CosmosDB:
    instance: "CosmosDB" = None

    @classmethod
    def get(cls):
        if not cls.instance:
            # brrrrrrr thats hacky
            from .settings import COSMOSDB_CONNECTION_STRING, COSMOSDB_DATABASE_NAME
            cls.instance = CosmosDB(COSMOSDB_CONNECTION_STRING, COSMOSDB_DATABASE_NAME)
        return cls.instance

    def __init__(self, connection_string: str, db_name: str):
        self.client = CosmosClient.from_connection_string(connection_string)
        self.db_client = self.client.get_database_client(db_name)

    def get_container(self, container_name, partition_key_path):
        try:
            return self.db_client.create_container(
                id=container_name,
                partition_key=PartitionKey(path=partition_key_path)
            )
        except exceptions.CosmosResourceExistsError:
            return self.db_client.get_container_client(container_name)
