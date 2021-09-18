resource "azurerm_servicebus_namespace" "sb_namespace" {
  name                = "finteg-sb-namespace"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  tags = {
    purpose = "hackathon"
  }
}


resource "azurerm_servicebus_topic" "message_inbound" {
  name                = "message_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "review_forwarder" {
  name                = "review_forwarder"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.message_inbound.name
  forward_to          = azurerm_servicebus_topic.review_inbound.name
  max_delivery_count  = 1
}

resource "azurerm_servicebus_subscription_rule" "review_forward_rule" {
  name                = "review_forward_rule"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.message_inbound.name
  subscription_name   = azurerm_servicebus_subscription.review_forwarder.name
  filter_type         = "SqlFilter"
  sql_filter          = "label = 'review'"
}

resource "azurerm_servicebus_subscription" "support_forwarder" {
  name                = "support_forwarder"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.message_inbound.name
  forward_to          = azurerm_servicebus_topic.thread_inbound.name
  max_delivery_count  = 1
}

resource "azurerm_servicebus_subscription_rule" "support_forwarder_rule" {
  name                = "support_forwarder_rule"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.message_inbound.name
  subscription_name   = azurerm_servicebus_subscription.support_forwarder.name
  filter_type         = "SqlFilter"
  sql_filter          = "label = 'support' OR label = 'thread'"
}


resource "azurerm_servicebus_topic" "review_inbound" {
  name                = "review_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "review_input_stream_sub" {
  name                = "review_input_stream_sub"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.review_inbound.name
  max_delivery_count  = 1
}


resource "azurerm_servicebus_topic" "thread_inbound" {
  name                = "thread_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "thread_input_stream_func_sub" {
  name                = "thread_input_stream_func_sub"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.thread_inbound.name
  max_delivery_count  = 1
}


resource "azurerm_servicebus_topic" "unknown_slack_threads" {
  name                = "unknown_slack_threads"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "get_or_create_slack_thread_func_sub" {
  name                = "get_or_create_slack_thread_func_sub"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.unknown_slack_threads.name
  max_delivery_count  = 1
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


resource "azurerm_servicebus_topic" "context_grouping_inbound" {
  name                = "context_grouping_inbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}

resource "azurerm_servicebus_subscription" "context_grouping_func_sub" {
  name                = "context_grouping_func_sub"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name
  topic_name          = azurerm_servicebus_topic.context_grouping_inbound.name
  max_delivery_count  = 1
}


resource "azurerm_servicebus_queue" "slack_outbound" {
  name                = "slack_outbound"
  resource_group_name = azurerm_resource_group.rg.name
  namespace_name      = azurerm_servicebus_namespace.sb_namespace.name

  enable_partitioning = true
}
