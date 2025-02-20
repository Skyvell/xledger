# General settings.
variable "location" {
  description = "The location for all resources."
  type        = string
}

# These should be existing resources.
variable "app_resource_group" {
  description = "Resource group object. Should supply an existing resource group."
  type        = any
}

variable "app_data_storage_account" {
  description = "Data lake storage account for storing the files."
  type        = any
}

variable "app_data_storage_container" {
  description = "Container for storing files in the Data Lake Storage Account."
  type        = any
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

variable "app_storage_account_name" {
  description = "The name of the Storage Account for the Function App."
  type        = string
}

variable "app_config_name" {
  description = "The name of the App Configuration."
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

variable "part_time_data_ductus_ab_flex_link" {
  description = "Xledger flexlink to get part time employee data from Data Ductus AB."
  type        = string
  sensitive   = true
}

variable "part_time_data_ductus_holding_ab_flex_link" {
  description = "Xledger flexlink to get part time employee data from Data Ductus Holding AB."
  type        = string
  sensitive   = true
}

variable "part_time_data_ductus_luleå_ab_flex_link" {
  description = "Xledger flexlink to get part time employee data from Data Ductus Luleå AB."
  type        = string
  sensitive   = true
}

variable "part_time_data_ductus_inc_flex_link" {
  description = "Xledger flexlink to get part time employee data from Data Ductus inc."
  type        = string
  sensitive   = true
}

variable "part_time_tromb_ab_flex_link" {
  description = "Xledger flexlink to get part time employee data from Data Ductus Holding AB."
  type        = string
  sensitive   = true
}