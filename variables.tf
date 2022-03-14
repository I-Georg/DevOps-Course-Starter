

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
variable "CONNECTIONSTRING" {
description = "mongo connection"
default = "mongodb://tododatabaseproject:JAyasz79f7yRR2zqi34xJG5PkjXbaRlvKJC4XlUYrqezapD97bHUF9WFeIpoDxXdaUNhby7ohYnSYK5Pommsfw==@tododatabaseproject.mongo.cosmos.azure.com:10255/?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000&appName=@tododatabaseproject@"
}

variable "CLIENTSECRET" {
description = "client secret"
default = "50d6114064c16235db5973535c97b5d6cda6faa"
}
variable "TODOBOARD" {
description = "todo"
default = "6005828032dafa5707bf5dc3"
}
variable "DOINGBOARD" {
description = "doing"
default = "6005828032dafa5707bf5dc7"
}
variable "DONEBOARD" {
description = "done"
default = "6005828032dafa5707bf5dc5"
}