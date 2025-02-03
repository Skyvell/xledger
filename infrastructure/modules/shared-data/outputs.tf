# These outputs are used in the module "function-app" to create the function app.

output "app_resource_group" {
  value       = data.azurerm_resource_group.app_resource_group.name
  description = "The name of the resource group where the function app resources exist."
}

output "app_storage_account" {
  value       = data.azurerm_storage_account.app_storage_account.name
  description = "The name of the storage account used by the function app."
}

output "app_storage_container" {
  value       = data.azurerm_storage_container.app_storage_container.name
  description = "The name of the storage container in the storage account."
}