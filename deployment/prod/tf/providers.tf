terraform {
  required_providers {
    acme = {
      source  = "vancluever/acme"
    }
    azuread = {
      source  = "hashicorp/azuread"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
    }
  }
}

provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
  subscription_id           = var.subscription_id
}

provider "acme" {
  server_url = "https://acme-v02.api.letsencrypt.org/directory"
}