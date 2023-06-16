#!/bin/bash

# Install Mosquitto MQTT
sudo apt-get install -y mosquitto mosquitto-clients

# Define username and password (user -> admin | password -> admin)
sudo mosquitto_passwd -c /etc/mosquitto/credentials admin <<<$'admin\nadmin'

# Copy mosquitto.conf from the shared folder to the correct directory inside the VM
cp ./share/mosquitto.conf /etc/mosquitto/mosquitto.conf

# Restart the mosquitto service with the new configs 
sudo systemctl restart mosquitto.service