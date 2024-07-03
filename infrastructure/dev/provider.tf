terraform {
  required_providers {
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = ">=0.1.0"
    }
  }
}

provider "azuredevops" {
  org_service_url = var.org_service_url
}







#provider "azurerm" {
#  features {}
#  # This tells Terraform to use the credentials from the Azure CLI login
#  use_cli = true
#}