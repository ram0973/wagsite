# -*- mode: ruby -*-
# vi: set ft=ruby :

VM_BOX = "generic/ubuntu1804"

Vagrant.configure("2") do |config|
  # boxes are available at https://vagrantcloud.com/search/

  config.vm.define "dev", primary: true do |dev|
    dev.vm.box = VM_BOX
    dev.vm.hostname = 'dev'
    dev.vm.box_check_update = true
    dev.vm.network "forwarded_port", guest: 5432, host: 5432, auto_correct: true
    dev.vm.network "forwarded_port", guest: 80, host: 80, auto_correct: true
    dev.vm.network "forwarded_port", guest: 443, host: 443, auto_correct: true
    dev.vm.network :forwarded_port, guest: 22, host: 2222, id: 'ssh'
    dev.vm.provision "shell", inline: "sudo apt-get update && sudo apt-get install mc tldr nmap neofetch -y"
    #dev.vm.provision "shell", inline: "sudo sed -i '/^PasswordAuthentication/s/no/yes/' /etc/ssh/sshd_config"
    #dev.vm.provision "shell", inline: "sudo systemctl restart sshd"
  end

  config.vm.define "staging", autostart: false do |staging|
    staging.vm.box = VM_BOX
    staging.vm.hostname = 'staging'
    staging.vm.box_check_update = true
    staging.vm.network "forwarded_port", guest: 5432, host: 5433, auto_correct: true
    staging.vm.network "forwarded_port", guest: 443, host: 444, auto_correct: true
    staging.vm.network :forwarded_port, guest: 22, host: 2223, id: 'ssh'
    staging.vm.provision "shell", inline: "sudo apt-get update && sudo apt-get install mc tldr nmap neofetch -y"
    #staging.vm.provision "shell", inline: "sudo sed -i '/^PasswordAuthentication/s/no/yes/' /etc/ssh/sshd_config"
    #staging.vm.provision "shell", inline: "sudo systemctl restart sshd"
  end

  config.vm.provider "virtualbox" do |vb|
    vb.gui = false
    vb.memory = "1024" # enough for server (no GUI)
  end
end
