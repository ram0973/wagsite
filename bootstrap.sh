#!/bin/bash

# Prepare base system
sudo apt-get update
sudo -H pip3 install pip --upgrade
sudo -H pip3 install wheel
sudo -H pip3 install -r requirements/fabric.txt
sudo -H pip3 install ansible --upgrade

./fix_ssh.sh