terraform {
  backend "azurerm" {
    resource_group_name   = "DDBI-ResourceGroup"
    storage_account_name  = "prodxledgertfstate"
    container_name        = "tfstate"
    key                   = "prod.terraform.tfstate"
  }
}