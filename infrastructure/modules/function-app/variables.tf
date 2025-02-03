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

variable "app_service_plan_os_type" {
  type        = string
  description = "The OS type for the service plan (Linux/Windows)."
  default     = "Linux"  # Default value
}

variable "app_service_plan_sku" {
  type        = string
  description = "The SKU tier for the service plan."
  default     = "B2"  # Default value
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

variable "api_endpoint" {
  description = "API endpoint URL."
  type = string
}

variable "api_key" {
  description = "The value of the API key."
  type        = string
  sensitive   = true
}

variable "employee_groups_flex_link" {
  description = "Xledger flexlink to get employee groups from."
  type        = string
  sensitive   = true
}

variable "employment_types_flex_link" {
  description = "Xledger flexlink to get employment types from."
  type        = string
  sensitive   = true
}

variable "project_groups_flex_link" {
  description = "Xledger flexlink to get project groups from."
  type        = string
  sensitive   = true
}

variable "financial_results_flex_link" {
  description = "Xledger flexlink to get financial results from."
  type        = string
  sensitive   = true
}