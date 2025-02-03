# Fetch existing resources to use in the function app.
module "shared_data" {
  source                              = "../../modules/shared-data"
  app_resource_group_name             = "DDBI-ResourceGroup"        
  app_storage_account_name            = "ddbistorage"
  app_storage_container_name          = "xledger-prod"
}

# The function app module is used to create the function app.
module "function_app" {
  source                              = "../../modules/function-app"
  app_configuration_name              = "xledger-syncronizer-state-prod"
  function_app_storage_account_name   = "syncronizerstorageprod"
  location                            = "westeurope"
  app_service_plan_name               = "xledeger-syncronizer-asp-prod"
  app_insights_name                   = "xledger-syncronizer-ai-prod"
  function_app_name                   = "xledger-syncronizer-prod"
  app_config_name                     = "xledger-syncronizer-statemanager-prod"
  api_endpoint                        = "https://demo.xledger.net/graphql"
  api_key                             = var.api_key

  # Flexlinks.
  employee_groups_flex_link           = var.employee_groups_flex_link
  employment_types_flex_link          = var.employment_types_flex_link
  project_groups_flex_link            = var.project_groups_flex_link
  financial_results_flex_link         = var.financial_results_flex_link

  # Existing resources.
  data_storage_account_name           = module.shared_data.data_storage_account_name
  data_storage_container_name         = module.shared_data.data_storage_container_name
  resource_group_name                 = module.shared_data.app_resource_group
}