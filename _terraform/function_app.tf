resource "azurerm_storage_account" "storage" {
  name                     = "fintegjangastorage"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    "purpose" = "hackathon"
  }
}

resource "azurerm_app_service_plan" "service_plan" {
  name                = "finteg_asp"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  kind                = "Linux"
  reserved            = true

  sku {
      tier = "Basic"
      size = "B1"
  }

  tags = {
    "purpose" = "hackathon"
  }
}

resource "azurerm_application_insights" "insights" {
  name                = "finteg-insights"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  application_type    = "web"
}

resource "azurerm_function_app" "functions" {
  name                       = "finteg-functions"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  app_service_plan_id        = azurerm_app_service_plan.service_plan.id
  storage_account_name       = azurerm_storage_account.storage.name
  storage_account_access_key = azurerm_storage_account.storage.primary_access_key

  site_config {
    linux_fx_version          = "PYTHON|3.8"
    use_32_bit_worker_process = true
  }

  app_settings = {
    APPINSIGHTS_INSTRUMENTATIONKEY = azurerm_application_insights.insights.instrumentation_key
    APPLICATIONINSIGHTS_CONNECTION_STRING = "InstrumentationKey=${azurerm_application_insights.insights.instrumentation_key}"
    COSMOSDB_CONNECTION_STRING = "AccountEndpoint=https://${azurerm_cosmosdb_account.db.name}.documents.azure.com:443/;AccountKey=${azurerm_cosmosdb_account.db.primary_key};"
    COSMOSDB_DATABASE_NAME = azurerm_cosmosdb_sql_database.integrations.name
    SERVICE_BUS_CONNECTION_STRING = azurerm_servicebus_namespace.sb_namespace.default_primary_connection_string
    XGD_CACHE_HOME = "/tmp/.cache"
    FUNCTIONS_EXTENSION_VERSION = "~3"
    FUNCTIONS_WORKER_RUNTIME = "python"
  }

  tags = {
    "purpose" = "hackathon"
  }
}
