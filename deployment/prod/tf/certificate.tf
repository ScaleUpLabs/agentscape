data "azurerm_dns_zone" "this" {
  name                = local.dns.name
  resource_group_name = local.dns.resource_group_name
}

resource "tls_private_key" "private_key" {
  algorithm = "RSA"
}

resource "acme_registration" "registration" {
  account_key_pem = tls_private_key.private_key.private_key_pem
  email_address   = "marco.cello@hotmail.com"
}

resource "azuread_application" "this" {
  display_name = lower(join("-", [local.prefix, "app"]))
}

resource "azuread_service_principal" "this" {
  client_id = azuread_application.this.client_id
}

resource "azuread_service_principal_password" "this" {
  service_principal_id = azuread_service_principal.this.id
}

resource "azurerm_role_assignment" "this" {
  scope                = data.azurerm_dns_zone.this.id
  role_definition_name = "Contributor"
  principal_id         = azuread_service_principal.this.object_id
}

resource "acme_certificate" "api" {
  account_key_pem           = acme_registration.registration.account_key_pem
  common_name               = lower(join(".", [local.prefix_dns, data.azurerm_dns_zone.this.name]))
  subject_alternative_names = [join(".", [local.prefix_dns, data.azurerm_dns_zone.this.name])]

  dns_challenge {
    provider = "azuredns"
    config = {
      AZURE_CLIENT_ID	      = azuread_application.this.client_id
      AZURE_CLIENT_SECRET   = azuread_service_principal_password.this.value
      AZURE_RESOURCE_GROUP  = data.azurerm_dns_zone.this.resource_group_name
      AZURE_SUBSCRIPTION_ID	= data.azurerm_subscription.this.subscription_id
      AZURE_TENANT_ID	      = data.azurerm_subscription.this.tenant_id
      AZURE_ENVIRONMENT	    = "public"
    }
  }

  depends_on = [
    azuread_application.this,
    azurerm_role_assignment.this
  ]
}

data "azurerm_key_vault" "this" {
  name                = local.keyvault.name
  resource_group_name = local.keyvault.resource_group_name
}

resource "azurerm_key_vault_certificate" "api" {
  name         = lower(join("-", [local.prefix,"certificate"]))
  key_vault_id = data.azurerm_key_vault.this.id

  certificate {
    contents = lookup(acme_certificate.api, "certificate_p12")
    password = ""
  }

  certificate_policy {
    issuer_parameters {
      name = "Unknown"
    }

    key_properties {
      exportable = true
      key_size   = 2048
      key_type   = "RSA"
      reuse_key  = true
    }

    secret_properties {
      content_type = "application/x-pkcs12"
    }
  }
}

