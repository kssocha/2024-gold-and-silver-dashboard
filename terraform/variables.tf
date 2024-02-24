variable "project" {}
variable "credentials_file" {}

variable "region" {
    default = "europe-west2"
}

variable "zone" {
    default = "europe-west2-a"
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
        zone = "europe-west2-a"
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
    default = "/home/kssocha/Desktop/Nauka/portfolio/2024-gold-and-silver-dashboard/ssh/.ssh/ssh-alk.pub" 
}

variable "network_parameters" {
    type = object({
        network_name = string
        auto_create_subnetworks = bool
        network_tier = string
        queue_count = number
        stack_type = string
        subnetwork = string
    })
    description = "network parameters"
    default = {
        network_name = "network-010"
        auto_create_subnetworks = false
        network_tier = "PREMIUM"
        queue_count = 1
        stack_type = "IPV4_ONLY"
        subnetwork = "subnet-010"
    }

    validation {
        condition = length(var.network_parameters) == 6
        error_message = "network parameters must have 6 elements"
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

variable "firewall-010" {
    type = object({
        name = string
        allow = object({
            protocol = string
            ports = list(string)
        })
        source_ranges = list(string)
        priority = string
    })
    description = "tcp port access"
    default = {
        name = "allow-tcp-port"
        allow = {
                protocol = "tcp"
                ports = ["22", "8050"]
        }
        source_ranges = ["0.0.0.0/0"]
        priority = "1000"
    }

    validation {
        condition = length(var.firewall-010) == 4
        error_message = "firewall parameters must have 4 elements"
    }
    validation {
        condition = length(var.firewall-010.allow) == 2
        error_message = "firewall parameters allow must have 2 elements"
    }
}

variable "firewall-020" {
    type = object({
        name = string
        allow = object({
            protocol = string
            ports = list(string)
        })
        source_ranges = list(string)
        priority = string
        target_tags = list(string)
    })
    description = "http-server access"
    default = {
        name = "allow-http-server"
        allow = {
                protocol = "tcp"
                ports = ["80"]
        }
        source_ranges = ["0.0.0.0/0"]
        priority = "1001"
        target_tags = ["http-server"]
    }

    validation {
        condition = length(var.firewall-020) == 5
        error_message = "firewall parameters must have 5 elements"
    }
    validation {
        condition = length(var.firewall-020.allow) == 2
        error_message = "firewall parameters allow must have 2 elements"
    }
}

variable "firewall-030" {
    type = object({
        name = string
        allow = object({
            protocol = string
            ports = list(string)
        })
        source_ranges = list(string)
        priority = string
        target_tags = list(string)
    })
    description = "https-server access"
    default = {
        name = "allow-https-server"
        allow = {
                protocol = "tcp"
                ports = ["443"]
        }
        source_ranges = ["0.0.0.0/0"]
        priority = "1001"
        target_tags = ["https-server"]
    }

    validation {
        condition = length(var.firewall-030) == 5
        error_message = "firewall parameters must have 5 elements"
    }
    validation {
        condition = length(var.firewall-030.allow) == 2
        error_message = "firewall parameters allow must have 2 elements"
    }
}