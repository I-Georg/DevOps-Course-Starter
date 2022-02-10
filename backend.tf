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
        key                  = "terraform.tfstate"
    }

}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "state-demo-secure" {
  name     = "state-demo"
  location = "eastus"
}