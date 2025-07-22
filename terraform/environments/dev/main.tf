# Define the environment as a local variable.
locals {
  environment = "dev"
}

# Fetch existing resources to use in the function app.
module "shared_data" {
  source                                     = "../../modules/shared-data"
  app_resource_group_name                    = "DDBI-ResourceGroup"        
  app_storage_account_name                   = "ddbistorage"
  app_storage_container_name                 = "xledger-${local.environment}"
}

# The function app module is used to create the function app.
module "function_app" {
  environment                                = local.environment
  source                                     = "../../modules/function-app"
  app_configuration_name                     = "xledger-syncronizer-state-${local.environment}"
  app_storage_account_name                   = "syncronizerstorage${local.environment}"
  location                                   = "westeurope"
  app_service_plan_name                      = "xledger-syncronizer-asp-${local.environment}"
  app_insights_name                          = "xledger-syncronizer-ai-${local.environment}"
  function_app_name                          = "xledger-syncronizer-${local.environment}"
  app_config_name                            = "xledger-syncronizer-statemanager-${local.environment}"
  api_endpoint                               = "https://www.xledger.net/graphql"
  api_key                                    = var.api_key
  app_configuration_sku                      = "free"

  # Flexlinks.
  employee_groups_flex_link                  = var.employee_groups_flex_link
  employment_types_flex_link                 = var.employment_types_flex_link
  project_groups_flex_link                   = var.project_groups_flex_link
  financial_results_flex_link                = var.financial_results_flex_link
  part_time_data_ductus_ab_flex_link         = var.part_time_data_ductus_ab_flex_link
  part_time_data_ductus_holding_ab_flex_link = var.part_time_data_ductus_holding_ab_flex_link
  part_time_data_ductus_luleå_ab_flex_link   = var.part_time_data_ductus_luleå_ab_flex_link
  part_time_data_ductus_inc_flex_link        = var.part_time_data_ductus_inc_flex_link
  part_time_tromb_ab_flex_link               = var.part_time_tromb_ab_flex_link 

  # Existing resources.
  app_data_storage_account                   = module.shared_data.app_storage_account
  app_data_storage_container                 = module.shared_data.app_storage_container
  app_resource_group                         = module.shared_data.app_resource_group

  # Functions schedules as environment variables.
  function_schedules = {
    FINANCIAL_RESULTS_NOON_SCHEDULE                   = "0 50 10 * * *"
    FINANCIAL_RESULTS_MIDNIGHT_SCHEDULE               = "0 50 22 * * *"
    AP_TRANSACTIONS_SCHEDULE                          = "0 * * * *"
    AR_TRANSACTIONS_SCHEDULE                          = "0 * * * *"
    BUDGET_DETAILS_SCHEDULE                           = "0 22 * * *"
    CUSTOMERS_SCHEDULE                                = "10 * * * *"
    EMPLOYEES_SCHEDULE                                = "10 * * * *"
    PRELIMINARY_TIMESHEETS_FIRST_OF_MONTH_SCHEDULE    = "25,55 * * * *"
    PRELIMINARY_TIMESHEETS_DAILY_SCHEDULE             = "0 22 * * *"
    PROJECTS_SCHEDULE                                 = "20 * * * *"
    SUPPLIERS_SCHEDULE                                = "20 * * * *"
    TIMESHEETS_SCHEDULE                               = "30 * * * *"
    TRANSACTIONS_SCHEDULE                             = "30 * * * *"
  }
}