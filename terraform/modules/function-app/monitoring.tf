resource "azurerm_application_insights" "application_insights" {
  name                = var.app_insights_name
  location            = var.location
  resource_group_name = var.app_resource_group.name
  application_type    = "web"
}

resource "azurerm_monitor_action_group" "sync_alert_group" {
  name                = "sync-stale-alert-group"
  resource_group_name = var.app_resource_group.name
  short_name          = "syncAlert"
  email_receiver {
    name                    = "EmailAlerts"
    email_address           = var.alert_email_address
    use_common_alert_schema = true
  }
}

resource "azurerm_monitor_scheduled_query_rules_alert" "sync_status_alert" {
  name                = "sync-stale-or-missing-alert"
  location            = var.location
  resource_group_name = var.app_resource_group.name
  description         = "Alert on stale or missing sync status from telemetry"
  enabled             = true
  severity            = 2
  frequency           = 1440   # Run every 24 hours
  time_window         = 1440   # Look at past 24 hours
  query               = <<-KQL
      traces
      | where message == "Sync health check"
      | where customDimensions.status in ("stale", "missing")
    KQL
  data_source_id = azurerm_application_insights.application_insights.id
  trigger {
    operator          = "GreaterThan"
    threshold         = 0
  }
  action {
    action_group = [azurerm_monitor_action_group.sync_alert_group.id]
  }
  tags = {
    environment = var.environment
  }
}