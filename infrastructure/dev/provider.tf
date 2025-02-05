provider "azurerm" {
  features {}
  
  # This tells Terraform to use the credentials from the Azure CLI login.
  # Uncomment when run from command line.
  use_cli = true
  subscription_id = "a42468e7-3510-409f-849a-111d4574481d"
}