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

        network = google_compute_network.network-010.self_link
        subnetwork = google_compute_subnetwork.subnetwork-010.self_link

        access_config {
        network_tier = var.network_parameters.network_tier
        }

        queue_count = var.network_parameters.queue_count
        stack_type  = var.network_parameters.stack_type
    }
    
    service_account {
        scopes = var.service_account_scopes
    }

    metadata = {
        sshKeys = "g64202_ckp:${file(var.ssh_key_path)}"
    }

    tags = var.tags

    provisioner "local-exec" {
        command = "./update_hosts.sh ${google_compute_instance.vm-010.network_interface.0.access_config.0.nat_ip}"
    }
}

output "instance_ip" {
    value = google_compute_instance.vm-010.network_interface.0.access_config.0.nat_ip
}

resource "google_compute_network" "network-010" {
  name = var.network_parameters.network_name
  auto_create_subnetworks = var.network_parameters.auto_create_subnetworks  
}

resource "google_compute_subnetwork" "subnetwork-010" {
  name = var.network_parameters.subnetwork
  network = google_compute_network.network-010.self_link
  ip_cidr_range = "10.20.0.0/16"
  region = var.region  
}

resource "google_compute_firewall" "firewall-010" {
    name = var.firewall-010.name
    network = google_compute_network.network-010.self_link
    allow {
        protocol = var.firewall-010.allow.protocol
        ports = var.firewall-010.allow.ports
    }
    source_ranges = var.firewall-010.source_ranges
    priority = var.firewall-010.priority
}

resource "google_compute_firewall" "firewall-020" {
    name = var.firewall-020.name
    network = google_compute_network.network-010.self_link
    allow {
        protocol = var.firewall-020.allow.protocol
        ports = var.firewall-020.allow.ports
    }
    source_ranges = var.firewall-020.source_ranges
    priority = var.firewall-020.priority
    target_tags = var.firewall-020.target_tags
}

resource "google_compute_firewall" "firewall-030" {
    name = var.firewall-030.name
    network = google_compute_network.network-010.self_link
    allow {
        protocol = var.firewall-030.allow.protocol
        ports = var.firewall-030.allow.ports
    }
    source_ranges = var.firewall-030.source_ranges
    priority = var.firewall-030.priority
    target_tags = var.firewall-030.target_tags
}