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
  description = "Xledger flexlink to get part time employee data from Tromb AB."
  type        = string
  sensitive   = true
}