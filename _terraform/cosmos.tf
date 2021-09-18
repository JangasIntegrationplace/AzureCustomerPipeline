resource "azurerm_cosmosdb_account" "db" {
  name                = "finteg-janga-cosmos-db"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"

  enable_automatic_failover = true
  enable_free_tier = var.enable_cosmos_db_free_tier == "true" || var.enable_cosmos_db_free_tier == true

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 10
    max_staleness_prefix    = 200
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }

  tags = {
    purpose = "hackathon"
  }
}


resource "azurerm_cosmosdb_sql_database" "integrations" {
  name                = "integrations"
  resource_group_name = azurerm_resource_group.rg.name
  account_name        = azurerm_cosmosdb_account.db.name
  throughput          = 400
}
