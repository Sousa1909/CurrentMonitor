#!/bin/bash

# Prints VM IP (should be equal to the one in the Vagrantfile)
echo 'VM IP:' && hostname -I | awk '{print $2}'