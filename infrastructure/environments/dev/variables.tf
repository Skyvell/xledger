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