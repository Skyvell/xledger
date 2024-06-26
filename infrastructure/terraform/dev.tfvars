# General settings.
location                      = "westeurope"
resource_group_name           = "DDBI-ResourceGroup"

# Function App infrastructure settings.
function_app_name               = "xledger-syncronizer-dev"
function_app_storage_account_name = "syncronizerstoragedev"
app_config_name                 = "xledger-syncronizer-statemanager-dev"
data_storage_account_name    = "ddbistorage"

# Function App environment settings.
api_endpoint = "https://demo.xledger.net/graphql"

# Backend settings.
backend_storage_account_name  = "devterraformstate"
backend_container_name        = "tfstate"
backend_key_name              = "dev.terraform.tfstate"

# Others.
tags = {
  environment = "dev"
  project     = "xledger-syncronizer"
}