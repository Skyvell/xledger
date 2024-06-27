data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

data "azurerm_storage_account" "existing" {
  name                = var.data_storage_account_name
  resource_group_name = data.azurerm_resource_group.existing.name
}

data "azurerm_storage_container" "existing_container" {
  name                 = var.data_storage_container_name
  storage_account_name = data.azurerm_storage_account.existing.name
}

resource "azurerm_app_configuration" "app_configuration" {
  name                = var.app_configuration_name
  resource_group_name = data.azurerm_resource_group.existing.name
  location            = var.location
}

resource "azurerm_storage_account" "app_storage_account" {
  name                     = var.function_app_storage_account_name
  resource_group_name      = data.azurerm_resource_group.existing.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_service_plan" "service_plan" {
  name                = var.app_service_plan_name
  location            = var.location
  resource_group_name = data.azurerm_resource_group.existing.name
  os_type             = "Linux"
  sku_name            = "Y1"
}

resource "azurerm_application_insights" "application_insights" {
  name                = var.app_insights_name
  location            = var.location
  resource_group_name = var.resource_group_name
  application_type    = "web"
}

resource "azurerm_linux_function_app" "function_app" {
  name                       = var.function_app_name
  service_plan_id            = azurerm_service_plan.service_plan.id
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.existing.name
  storage_account_name       = azurerm_storage_account.app_storage_account.name
  storage_account_access_key = azurerm_storage_account.app_storage_account.primary_access_key
  https_only                 = true

  site_config {
    application_stack {
        python_version = "3.11"
    }
  }

  identity {
    type = "SystemAssigned"
  }

  app_settings = {
    "API_ENDPOINT"                = var.api_endpoint,
    "API_KEY"                     = var.api_key,
    "DATA_STORAGE_ACCOUNT_NAME"   = var.data_storage_account_name,
    "DATA_STORAGE_CONTAINER_NAME" = var.data_storage_container_name,
    "APP_CONFIG_ENDPOINT"         = azurerm_app_configuration.app_configuration.endpoint
    "APPINSIGHTS_INSTRUMENTATIONKEY" = azurerm_application_insights.application_insights.instrumentation_key
  }
}

resource "azurerm_role_assignment" "storage_container_access" {
  principal_id         = azurerm_linux_function_app.function_app.identity[0].principal_id
  role_definition_name = "Storage Blob Data Contributor"
  scope                = "${data.azurerm_storage_account.existing.id}/blobServices/default/containers/${data.azurerm_storage_container.existing_container.name}"
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