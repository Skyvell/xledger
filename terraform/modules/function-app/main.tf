# Creates the xledger-syncronizer-dev function app infrastructure.

resource "azurerm_app_configuration" "app_configuration" {
  name                = var.app_configuration_name
  resource_group_name = var.app_resource_group.name
  location            = var.location
  sku                 = var.app_configuration_sku
}

resource "azurerm_storage_account" "app_storage_account" {
  name                     = var.app_storage_account_name
  resource_group_name      = var.app_resource_group.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
  name                = var.app_service_plan_name
  location            = var.location
  resource_group_name = var.app_resource_group.name
  os_type             = var.app_service_plan_os_type
  sku_name            = var.app_service_plan_sku
}

resource "azurerm_application_insights" "application_insights" {
  name                = var.app_insights_name
  location            = var.location
  resource_group_name = var.app_resource_group.name
  application_type    = "web"
}

resource "azurerm_linux_function_app" "function_app" {
  name                       = var.function_app_name
  service_plan_id            = azurerm_service_plan.service_plan.id
  location                   = var.location
  resource_group_name        = var.app_resource_group.name
  storage_account_name       = azurerm_storage_account.app_storage_account.name
  storage_account_access_key = azurerm_storage_account.app_storage_account.primary_access_key
  https_only                 = true

  site_config {
    application_stack {
      python_version = "3.11"
    }
    always_on = true
    application_insights_key = azurerm_application_insights.application_insights.instrumentation_key
    cors {
      allowed_origins = ["https://portal.azure.com"]
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = merge(
    {
    "ENVIRONMENT"                                = var.environment,
    "API_ENDPOINT"                               = var.api_endpoint,
    "API_KEY"                                    = var.api_key,
    "APPLICATIONINSIGHTS_CONNECTION_STRING"      = azurerm_application_insights.application_insights.connection_string,
    "DATA_STORAGE_ACCOUNT_NAME"                  = var.app_data_storage_account.name,
    "DATA_STORAGE_CONTAINER_NAME"                = var.app_data_storage_container.name,
    "APP_CONFIG_ENDPOINT"                        = azurerm_app_configuration.app_configuration.endpoint,
    "EMPLOYEE_GROUPS_FLEX_LINK"                  = var.employee_groups_flex_link,
    "EMPLOYMENT_TYPES_FLEX_LINK"                 = var.employment_types_flex_link,
    "PROJECT_GROUPS_FLEX_LINK"                   = var.project_groups_flex_link,
    "FINANCIAL_RESULTS_FLEX_LINK"                = var.financial_results_flex_link,
    "PART_TIME_DATA_DUCTUS_AB_FLEX_LINK"         = var.part_time_data_ductus_ab_flex_link,
    "PART_TIME_DATA_DUCTUS_HOLDING_AB_FLEX_LINK" = var.part_time_data_ductus_holding_ab_flex_link,
    "PART_TIME_DATA_DUCTUS_LULEÅ_AB_FLEX_LINK"   = var.part_time_data_ductus_luleå_ab_flex_link,
    "PART_TIME_DATA_DUCTUS_INC_FLEX_LINK"        = var.part_time_data_ductus_inc_flex_link,
    "PART_TIME_TROMB_AB_FLEX_LINK"               = var.part_time_tromb_ab_flex_link,
    "WEBSITE_TIME_ZONE"                          = "Europe/Stockholm"
  },
  var.function_schedules
  )
}

resource "azurerm_role_assignment" "storage_container_access" {
  principal_id         = azurerm_linux_function_app.function_app.identity[0].principal_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = "${var.app_data_storage_account.id}/blobServices/default/containers/${var.app_data_storage_container.name}"
  depends_on           = [azurerm_linux_function_app.function_app]
}

resource "azurerm_role_assignment" "app_configuration_access" {
  principal_id         = azurerm_linux_function_app.function_app.identity[0].principal_id
  role_definition_name = "App Configuration Data Owner"
  scope                = azurerm_app_configuration.app_configuration.id
  depends_on           = [azurerm_linux_function_app.function_app]
}
# Workaround for when principal_id complains: https://github.com/hashicorp/terraform-provider-azurerm/issues/11613


# NOTES
# Infra: FOR EACH ENV: Functionapp, functionapp storage, app config, terraform backend.
# Permissions for function app to access external storage account and appconfig.
# API key dev in azure pipeline.
# One pipeline for dev and one for prod.