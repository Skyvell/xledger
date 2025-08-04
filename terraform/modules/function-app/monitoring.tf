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
    email_address           = "ted.skyvell@ductus.se"
    use_common_alert_schema = true
  }
}