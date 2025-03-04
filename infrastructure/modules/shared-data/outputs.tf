# These outputs are used in the module "function-app" to create the function app.

output "app_resource_group" {
  value       = data.azurerm_resource_group.app_resource_group
  description = "The resource group object where the function app resources exist."
}

output "app_storage_account" {
  value       = data.azurerm_storage_account.app_storage_account
  description = "The storage account object used by the function app."
}

output "app_storage_container" {
  value       = data.azurerm_storage_container.app_storage_container
  description = "The storage container object in the storage account."
}