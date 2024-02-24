#!/bin/bash

# Extract IP address from Terraform output
IP_ADDRESS=$1

# Update the hosts file
sed -i "s/^vm-010 ansible_host=.*/vm-010 ansible_host=$IP_ADDRESS ansible_user=g64202_ckp ansible_connection=ssh ansible_ssh_private_key_file=\/home\/kssocha\/Desktop\/Nauka\/portfolio\/2024-gold-and-silver-dashboard\/ssh\/.ssh\/ssh-alk/" /home/kssocha/Desktop/Nauka/portfolio/2024-gold-and-silver-dashboard/ansible/hosts