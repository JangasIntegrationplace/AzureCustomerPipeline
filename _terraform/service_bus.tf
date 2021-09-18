resource "azurerm_servicebus_namespace" "sb_namespace" {
  name                = "finteg-sb-namespace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  tags = {
    purpose = "hackathon"
  }
}


resource "azurerm_servicebus_queue" "content_inbound" {
  name                = "content_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}


resource "azurerm_servicebus_queue" "review_inbound" {
  name                = "review_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}


resource "azurerm_servicebus_queue" "slack_threads" {
  name                = "slack_threads"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}


resource "azurerm_servicebus_topic" "sentiment_analysis_inbound" {
  name                = "sentiment_analysis_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "sentiment_analysis_func_sub" {
  name                = "sentiment_analysis_func_sub"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.sentiment_analysis_inbound.name
  max_delivery_count  = 1
}


resource "azurerm_servicebus_queue" "slack_outbound" {
  name                = "slack_outbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}
