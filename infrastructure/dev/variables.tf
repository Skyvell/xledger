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

variable "app_service_plan_name" {
  description = "The name of the App Service Plan."
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

variable "data_storage_container_name" {
  description = "The name of the container for storing files in the Data Lake Storage Account."
  type        = string
}

variable "app_configuration_name" {
  description = "The name of the app configuration used by the function app to keep the state."
  type        = string
}

variable "app_insights_name" {
  description = "The name of the Application Insights."
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


# Configure service principal to use in pipeline.
variable "client_id" {
  description = "Client ID for Azure DevOps"
}

variable "tenant_id" {
  description = "Tenant ID for Azure DevOps"
}

variable "client_secret" {
  description = "Client Secret for Azure DevOps"
  sensitive   = true
}

variable "org_service_url" {
  description = "Organization Service URL for Azure DevOps"
}


# Others.
variable "tags" {
  description = "A map of tags to assign to the resources"
  type        = map(string)
}