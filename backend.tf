terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "=2.51"
    }
  }
    backend "azurerm" {
        resource_group_name  = "OpenCohort1_IlinaGeorgieva_ProjectExercise"
        storage_account_name = "illigeorgieva102"
        container_name       = "illigeorgieva102"
        key                  = "terraform.OpenCohort1_IlinaGeorgieva_ProjectExercise"
    }

}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name     = "OpenCohort1_IlinaGeorgieva_ProjectExercise"
 
}

resource "azurerm_app_service_plan" "main" {
name = "terraformed-ilgdevops"
location = data.azurerm_resource_group.main.location
resource_group_name = data.azurerm_resource_group.main.name
kind = "Linux"
reserved = true
sku {
tier = "Basic"
size = "B1"
}
}
resource "azurerm_app_service" "main" {
name = "illigeorgieva102"
location = var.location
resource_group_name = data.azurerm_resource_group.main.name
app_service_plan_id = azurerm_app_service_plan.main.id

site_config {
app_command_line = ""
linux_fx_version = "DOCKER|ilgeo/my-production-image:latest"
}
app_settings = {
"DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
"CONNECTIONSTRING" =var.CONNECTIONSTRING 
"GITHUBID"=var.GITHUBID
"WEBAPPLICATIONCLIENT" =var.WEBAPPLICATIONCLIENT
"CLIENTSECRET" = var.CLIENTSECRET
"TODOBOARD"= var.TODOBOARD
"DOINGBOARD"=var.DOINGBOARD
"DONEBOARD"=var.DONEBOARD


}
}
resource "azurerm_cosmosdb_account" "db" {
  name                = "illigeorgieva102"
  resource_group_name = "opencohort1_ilinageorgieva_projectexercise"
  location            = data.azurerm_resource_group.main.location
  offer_type          = "Standard"
  kind                = "MongoDB"
  enable_automatic_failover = true

  capabilities { 
   name = "EnableServerless" 
  }

  lifecycle { 
  prevent_destroy = false
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

   geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
  consistency_policy {
    consistency_level = "Session"
  }
}

resource "azurerm_cosmosdb_mongo_database" "db" {
  name                = "illigeorgieva102"
  resource_group_name = "opencohort1_ilinageorgieva_projectexercise"
  account_name  = azurerm_cosmosdb_account.db.name

}

