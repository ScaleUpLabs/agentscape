resource "azurerm_storage_account" "this" {
  name                     = lower(join("", [local.prefix_cut,"strgacc"]))
  resource_group_name      = azurerm_resource_group.this.name
  location                 = azurerm_resource_group.this.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_storage_share" "this" {
  name                 = lower(join("", [local.prefix_cut, "share"]))
  storage_account_name = azurerm_storage_account.this.name
  quota                = 50
}

