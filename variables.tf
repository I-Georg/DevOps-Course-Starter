variable "prefix" {
description = "The prefix used for all resources in this environment"
}

variable "location" {
description = "The Azure location where all resources in this deployment should be created"
default = "uksouth"
}

variable "GITHUBID" {
description = "The githubid"
default = "47190936"
}

variable "WEBAPPLICATIONCLIENT" {
description = "client web"
default = "88de9a9a5377861febef"
}