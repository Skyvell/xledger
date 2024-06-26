data "azurerm_resource_group" "existing" {
  name = var.resource_group_name
}

resource "azurerm_storage_account" "app_storage_account" {
  name                     = var.function_app_storage_account_name
  resource_group_name      = data.azurerm_resource_group.existing.name
  location                 = var.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_app_service_plan" "service_plan" {
  name                = "${var.function_app_name}-asp"
  location            = var.location
  resource_group_name = data.azurerm_resource_group.existing.name
  kind                = "FunctionApp"
  reserved            = true  # required for Linux

  sku {
    tier = "Dynamic"
    size = "Y1"
  }
}

resource "azurerm_function_app" "example" {
  name                       = var.function_app_name
  location                   = var.location
  resource_group_name        = data.azurerm_resource_group.existing.name
  app_service_plan_id        = azurerm_app_service_plan.service_plan.id
  storage_account_name       = azurerm_storage_account.app_storage_account.name
  storage_account_access_key = azurerm_storage_account.app_storage_account.primary_access_key
  os_type                    = "linux"
  version                    = "~4"
  https_only                 = true

  site_config {
    use_32_bit_worker_process = false
    always_on                 = true
    linux_fx_version          = "PYTHON|3.11"
  }

  app_settings = {
    "FUNCTIONS_WORKER_RUNTIME"    = "python",
    "FUNCTIONS_EXTENSION_VERSION" = "~4",
  }
}


# NOTES
# Infra: FOR EACH ENV: Functionapp, functionapp storage, app config, terraform backend.
# Permissions for function app to access external storage account and appconfig.
# API key dev in azure pipeline.
# One pipeline for dev and one for prod.