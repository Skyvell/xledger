# General settings.
variable "location" {
  description = "The location for all resources."
  type        = string
}

variable "resource_group_name" {
  description = "The name of the resource group."
  type        = string
}


# Function App.
variable "function_app_name" {
  description = "The name of the Function App."
  type        = string
}

variable "function_app_storage_account_name" {
  description = "The name of the Storage Account for the Function App."
  type        = string
}

variable "app_config_name" {
  description = "The name of the App Configuration."
  type        = string
}

variable "data_storage_account_name" {
  description = "The name of the Data Lake Storage Account."
  type        = string
}


# Configuration of Function App.
variable "api_key" {
  description = "The value of the API key."
  type        = string
  sensitive   = true
}

variable "api_endpoint" {
  description = "API endpoint URL."
  type = string
}


# Backend settings.
variable "backend_storage_account_name" {
  description = "The name of the Storage Account for the backend."
  type        = string
}

variable "backend_container_name" {
  description = "The name of the container for the backend."
  type        = string
}

variable "backend_key_name" {
  description = "The name of the key for the backend state file."
  type        = string
}


# Others.
variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
}