terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = "=2.51"
        }
    }
}
provider "azurerm" {
features {}
}
data "azurerm_resource_group" "main" {
name = "opencohort1_ilinageorgieva_projectexercise"


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
location = data.azurerm_resource_group.main.location
resource_group_name = data.azurerm_resource_group.main.name
app_service_plan_id = azurerm_app_service_plan.main.id
MONGODB_CONNECTION_STRING" = "mongodb://$
{opencohort1_ilinageorgieva_projectexercise}:$
{azurerm_cosmosdb_account.main.primary_key}@$
{opencohort1_ilinageorgieva_projectexercise}.mongo.cosmos.azure.
com:10255/DefaultDatabase?
ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTi
meMS=120000
site_config {
app_command_line = ""
linux_fx_version = "DOCKER|appsvcsample/python-helloworld:latest"
}
app_settings = {
"DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
}
}
data "azurerm_cosmosdb_account" "example" {
  name                = "illigeorgieva102"
  resource_group_name = "opencohort1_ilinageorgieva_projectexercise"
  capabilities { name = "EnableServerless" }
}

resource "azurerm_cosmosdb_mongo_database" "example" {
  name                = "illigeorgieva102"
  resource_group_name = data.azurerm_cosmosdb_account.illigeorgieva102.opencohort1_ilinageorgieva_projectexercise
  account_name        = data.azurerm_cosmosdb_account.illigeorgieva102.name
  throughput          = 400
  capabilities { name = "EnableServerless" }
}
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.resource_group_location
}

resource "random_integer" "ri" {
  min = 10000
  max = 99999
}

resource "azurerm_cosmosdb_account" "db" {
  name                = "tfex-cosmos-db-${random_integer.ri.result}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  enable_automatic_failover = true

  capabilities {
    name = "EnableAggregationPipeline"
  }

  capabilities {
    name = "mongoEnableDocLevelTTL"
  }

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = var.failover_location
    failover_priority = 1
  }

  geo_location {
    location          = azurerm_resource_group.rg.location
    failover_priority = 0
  }
}