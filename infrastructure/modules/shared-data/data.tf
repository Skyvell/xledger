# File contains resources that must exist in Azure for the function app to work properly.

data "azurerm_resource_group" "app_resource_group" {
  name = var.app_resource_group_name
}

data "azurerm_storage_account" "app_storage_account" {
  name                = var.app_storage_account_name
  resource_group_name = data.azurerm_resource_group.app_resource_group.name
}

data "azurerm_storage_container" "app_storage_container" {
  name                 = var.app_storage_account_name
  storage_account_name = var.app_storage_account_name
}