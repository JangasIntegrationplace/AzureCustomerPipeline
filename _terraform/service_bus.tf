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


resource "azurerm_servicebus_queue" "dispatch" {
  name                = "dispatch"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}


resource "azurerm_servicebus_queue" "slack_outbound" {
  name                = "slack_outbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}
