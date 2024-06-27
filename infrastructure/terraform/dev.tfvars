# General settings.
location                      = "westeurope"
resource_group_name           = "DDBI-ResourceGroup"

# Function App infrastructure settings.
function_app_name               = "xledger-syncronizer-dev"
app_service_plan_name = "xledeger-syncronizer-asp-dev"
function_app_storage_account_name = "syncronizerstoragedev"
app_config_name                 = "xledger-syncronizer-statemanager-dev"
data_storage_account_name    = "ddbistorage"
data_storage_container_name = "xledger-dev"
app_configuration_name = "xledger-syncronizer-state-dev"
app_insights_name = "xledger-syncronizer-ai-dev"

# Function App environment settings.
api_endpoint = "https://demo.xledger.net/graphql"
api_key = "AABA3lMcMgAAAAACD2TJCDBFPJ-0zrpMAhykBr4Msf0TbOiUAiw_xeQsnPkElVcXCtceS_CZVcBEeuSB48H12UrFiS7HaSIC38a4BRj7hmrzc6RUxED02m2_5vZ7vordbwXOlZZni839CQEmHSo_IVdpao8rRdXb-3rKbvD_CN7j_KGQDWhow2rfVUnNC7rPrYatbwvdKGE7WX2NQ-QAvJ2_j6MrJ5T50hs9dEeI9k6vhwfZ1iUQHko5we6TpJQ9zZjmvWK37RbGFMbDdQnhzARP62ZJFDa-Q-SrT4eL18o4b1AGQOQ5xqxK-Uk8YJFDWiKUf3c8GMXSmqCGpA4A"

# Backend settings.
backend_storage_account_name  = "devterraformstate"
backend_container_name        = "tfstate"
backend_key_name              = "dev.terraform.tfstate"

# Others.
tags = {
  environment = "dev"
  project     = "xledger-syncronizer"
}