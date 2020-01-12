#!/bin/bash

chmod 600 ~/.ssh/config
chmod 400 ~/.ssh/id_rsa
ssh-keygen -f "/home/$USER/.ssh/known_hosts" -R "[localhost]:2222"
ssh-copy-id -i ~/.ssh/id_rsa.pub dev -f
ssh-keygen -f "/home/$USER/.ssh/known_hosts" -R "[localhost]:2223"
ssh-copy-id -i ~/.ssh/id_rsa.pub staging -f