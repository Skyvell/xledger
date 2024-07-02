terraform {
  backend "azurerm" {
    resource_group_name   = "DDBI-ResourceGroup"
    storage_account_name  = "devxledgerterraformstate"
    container_name        = "tfstate"
    key                   = "dev.terraform.tfstate"
  }
}