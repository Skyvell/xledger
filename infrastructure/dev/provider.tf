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
  client_id       = var.client_id
  tenant_id       = var.tenant_id
  client_secret   = var.client_secret
}







#provider "azurerm" {
#  features {}
#  # This tells Terraform to use the credentials from the Azure CLI login
#  use_cli = true
#}