terraform {
  backend "azurerm" {
    resource_group_name  = "prod-terraformstate-rg"
    storage_account_name = "prdtfstrg"
    container_name       = "tfstate"
    key                  = "prod-agentscape-backend"
  }
}