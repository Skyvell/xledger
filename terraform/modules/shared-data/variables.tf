variable "app_resource_group_name" {
  type        = string
  description = "The name of the resource group where the function app resources exist."
}

variable "app_storage_account_name" {
  type        = string
  description = "The name of the storage account used by the function app."
}

variable "app_storage_container_name" {
  type        = string
  description = "The name of the storage container in the storage account."
}