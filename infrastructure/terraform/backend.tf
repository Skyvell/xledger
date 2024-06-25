terraform {
  backend "azurerm" {
    resource_group_name   = var.resource_group_name
    storage_account_name  = "devterraformstate"
    container_name        = "tfstate"
    key                   = "dev.terraform.tfstate"
  }
}