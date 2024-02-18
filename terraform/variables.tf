variable "project" {}
variable "credentials_file" {}

variable "region" {
    default = "europe-west10"
}

variable "zone" {
    default = "europe-west10-b"
}

variable "disk_parameters" {
    type = object({
        name = string
        image = string
        size = number
        type = string
        auto_delete = bool
    })
    description = "disk parameters"
    default = {
        name = "disk-010"
        image = "ubuntu-os-cloud/ubuntu-2204-lts"
        size  = 10
        type  = "pd-balanced"
        auto_delete = false
    }

    validation {
        condition = length(var.disk_parameters) == 5
        error_message = "disk parameters must have 5 elements"
    }
}

variable "vm_parameters" {
    type = object({
        name = string
        machine_type = string
        zone = string
        allow_stopping_for_update = bool
        mode = string
    })
    description = "vm parameters"
    default = {
        name = "vm-010"
        machine_type = "e2-standard-4"
        zone = "europe-west10-b"
        allow_stopping_for_update = true
        mode = "READ_WRITE"
    }

    validation {
        condition = length(var.vm_parameters) == 5
        error_message = "vm parameters must have 5 elements"
    }  
}

variable "ssh_key_path" {
    type = string
    description = "ssh key path"
    default = "/home/kssocha/Desktop/Nauka/portfolio/202312-gold-and-silver-dashboard/ssh/.ssh/ssh-alk.pub" 
}

variable "network_parameters" {
    type = object({
        network_name = string
        network_tier = string
        queue_count = number
        stack_type = string
        subnetwork = string
    })
    description = "network parameters"
    default = {
        network_name = "default"
        network_tier = "PREMIUM"
        queue_count = 0
        stack_type = "IPV4_ONLY"
        subnetwork = "default"
    }

    validation {
        condition = length(var.network_parameters) == 5
        error_message = "network parameters must have 5 elements"
    }

    validation {
        condition = var.network_parameters.network_tier == "PREMIUM" || var.network_parameters.network_tier == "STANDARD"
        error_message = "network_tier must be PREMIUM or STANDARD"
    }

    validation {
        condition = var.network_parameters.stack_type == "IPV4_ONLY" || var.network_parameters.stack_type == "IPV4_IPV6"
        error_message = "stack_type must be IPV4_ONLY or IPV4_IPV6"
    }

    validation {
        condition = var.network_parameters.queue_count >= 0
        error_message = "queue_count must be greater than or equal to 0"
    } 
}

variable "service_account_scopes" {
    type = list(string)
    description = "scopes"
    default = ["https://www.googleapis.com/auth/cloud-platform"]
    validation {
        condition = length(var.service_account_scopes) >= 1
        error_message = "scopes must have 1 element"
    }
}

variable "tags" {
    type = list(string)
    description = "tags"
    default = ["http-server", "https-server"]
    validation {
        condition = length(var.tags) == 2
        error_message = "tags must have 2 elements"
    }
}

variable "access_port" {
    type = object({
        name = string
        allow = object({
            protocol = string
            ports = list(string)
        })
        source_ranges = list(string)
    })
    description = "access port"
    default = {
        name = "access-port-010"
        allow = {
                protocol = "tcp"
                ports = ["8050"]
        }
        source_ranges = ["0.0.0.0/0"]
    }

    validation {
        condition = length(var.access_port) == 3
        error_message = "firewall parameters must have 3 elements"
    }
    validation {
        condition = length(var.access_port.allow) == 2
        error_message = "firewall parameters allow must have 2 elements"
    }
}