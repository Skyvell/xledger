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
api_key = "AABAYVMcMgAAAAACD2TJ45KHP6xt-rvklRxnOgTYS4L6HF48w91EYEnHg9OdVXmgfg3qWuxkBIM_yom33goqiTpSZ0ev8LhsrvMfihpYoU8cA0CRtcuiXeBoB4eeQy8M1TWcpcQ9LEy4Df1SZxDr4dgQFb60IaPMutQtaA4gyeQVDgkcE_SLE4awhiyYeDrfiW2wgtlb0eUM3yWDSIqAuD--t3d_KjfyzfjERhumU5TkuxVBNHQ37_cN-VAaqZdk0xe-9Diz6Q4c7sPMxtpiuy2V_nu2YLgECdWNne4Bilp9OpZrGWREikpdZPmJ0yoiDmqWV-2bsUCK7eaVNjoA"

# Backend settings.
backend_storage_account_name  = "devterraformstate"
backend_container_name        = "tfstate"
backend_key_name              = "dev.terraform.tfstate"

# Others.
tags = {
  environment = "dev"
  project     = "xledger-syncronizer"
}