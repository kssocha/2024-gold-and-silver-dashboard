provider "google" {
  project = var.project
  credentials = file(var.credentials_file)
  region = var.region
  zone = var.zone
}

resource "google_compute_instance" "vm-010" {
    name = var.vm_parameters.name
    machine_type = var.vm_parameters.machine_type
    zone = var.vm_parameters.zone
    allow_stopping_for_update = var.vm_parameters.allow_stopping_for_update

    boot_disk {
        auto_delete = var.disk_parameters.auto_delete
        device_name = var.disk_parameters.name

        initialize_params {
        image = var.disk_parameters.image
        size  = var.disk_parameters.size
        type  = var.disk_parameters.type
    }

    mode = var.vm_parameters.mode
    }

    network_interface {
        access_config {
        network_tier = var.network_parameters.network_tier
        }

        queue_count = var.network_parameters.queue_count
        stack_type  = var.network_parameters.stack_type
        subnetwork  = var.network_parameters.subnetwork
    }
    
    service_account {
        scopes = var.service_account_scopes
    }

    metadata = {
        sshKeys = "g64202_ckp:${file(var.ssh_key_path)}"
    }

    tags = var.tags
}

resource "google_compute_firewall" "access-port-010" {
    name = var.access_port.name
    network = var.network_parameters.network_name
    allow {
        protocol = var.access_port.allow.protocol
        ports = var.access_port.allow.ports
    }
    source_ranges = var.access_port.source_ranges
}