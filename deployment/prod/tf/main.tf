data "azurerm_subscription" "this" {
}

data "azurerm_client_config" "this" {
}

data "azuread_client_config" "this" {
}

locals {
  prefix            = join("-", compact([local.input.stage, local.input.project, local.input.component]))
  prefix_condensed  = join("", compact([local.input.stage, local.input.project, local.input.component]))
  prefix_cut        = join("", compact([substr(local.input.stage,0,3), substr(local.input.project,0,3), substr(local.input.component,0,3)]))
  prefix_dns        = local.input.stage == "prod" ? join(".", ["api"]) : join(".", [local.input.stage, "api"])
  custom_tags       = local.input
}

locals {
  input = {
    stage     = "prod"
    project   = "agentscape"
    component = "backend"
    service   = ""
    cloud     = "azure"
    location  = "West Europe"
    managedBy = "terraform"
    owner     = "marco.cello@hotmail.com"
  } 
}

locals {
  dns = {
    name = "agentscape.cc"
    resource_group_name = "prod-infrastructure-dnszone-rg"
  }
}

locals {
  keyvault = {
    name = "proinfkubvault"
    resource_group_name = "prod-infrastructure-kubernetes-rg"
  }
}