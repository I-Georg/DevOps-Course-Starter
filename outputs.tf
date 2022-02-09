output "webapp_url" {
value = "https:/https://illigeorgieva102.azurewebsites.net/"
}

output"cd_webhook" {
value= "https://${azurerm_app_service.main.site_credential[0].username}:${azurerm_app_service.main.site_credential[0].password}@${azurerm_app_service.main.name}.scm.azurewebsites.net/docker/hook"
}
