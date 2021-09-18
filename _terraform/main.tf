terraform {
    required_providers {
        azurerm = {
            source  = "hashicorp/azurerm"
            version = "2.76"
        }
    }

    required_version = ">= 0.14.9"
}

provider "azurerm" {
    features {}
}


resource "azurerm_resource_group" "rg" {
    name = "finteg"
    location = "westeurope"
    tags = {
        purpose = "hackathon"
    }
}
