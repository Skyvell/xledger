# General settings.
location                          = "westeurope"
resource_group_name               = "DDBI-ResourceGroup"

# Function App infrastructure settings.
function_app_name                 = "xledger-syncronizer-dev"
app_service_plan_name             = "xledeger-syncronizer-asp-dev"
function_app_storage_account_name = "syncronizerstoragedev"
app_config_name                   = "xledger-syncronizer-statemanager-dev"
data_storage_account_name         = "ddbistorage"
data_storage_container_name       = "xledger-dev"
app_configuration_name            = "xledger-syncronizer-state-dev"
app_insights_name                 = "xledger-syncronizer-ai-dev"

# Xledger API settings.
api_endpoint                      = "https://demo.xledger.net/graphql"

# Backend settings.
backend_storage_account_name      = "devterraformstate"
backend_container_name            = "tfstate"
backend_key_name                  = "dev.terraform.tfstate"

# Others.
tags = {
  environment                     = "dev"
  project                         = "xledger-syncronizer"
}
org_service_url                   = "https://dev.azure.com/dataductusddbi"