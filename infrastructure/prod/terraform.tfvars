# General settings.
location                          = "westeurope"
resource_group_name               = "DDBI-ResourceGroup"

# Function App infrastructure settings.
function_app_name                 = "xledger-syncronizer-prod"
app_service_plan_name             = "xledeger-syncronizer-asp-prod"
function_app_storage_account_name = "syncronizerstorageprod"
app_config_name                   = "xledger-syncronizer-statemanager-prod"
data_storage_account_name         = "ddbistorage"
data_storage_container_name       = "xledger-prod"
app_configuration_name            = "xledger-syncronizer-state-prod"
app_insights_name                 = "xledger-syncronizer-ai-prod"

# Xledger API settings.
# api_endpoint                      =
# api_key                           = 

# Backend settings.
backend_storage_account_name      = "prodterraformstate"
backend_container_name            = "tfstate"
backend_key_name                  = "prod.terraform.tfstate"

# Others.
tags = {
  environment                     = "prod"
  project                         = "xledger-syncronizer"
}