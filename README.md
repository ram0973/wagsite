# Django blog
### Django 2.2+ blog engine
[![CircleCI](https://circleci.com/gh/ram0973/djblog.svg?style=svg)](https://circleci.com/gh/ram0973/djblog)
[![Maintainability](https://api.codeclimate.com/v1/badges/85562fb4af688d096860/maintainability)](https://codeclimate.com/github/ram0973/djblog/maintainability)
[![codecov](https://codecov.io/gh/ram0973/djblog/branch/master/graph/badge.svg)](https://codecov.io/gh/ram0973/djblog)

# About
This is simple Python/Django blog. Download last release [here](https://github.com/ram0973/djblog/releases/)
Designed to be a testing site for web/devops technologies.

## Features:

- Run dev/staging virtual machines easy with Vagrant
- Deploy via Ansible and Fabric
- Nginx with TLS 1.3, even on dev/staging (valid certificates for local development supplied)
- Https on production server via Let's Encrypt certbot, with subdomains support
- Run on dev: Nginx + Django runserver
- Run on staging/production: Nginx + Gunicorn + systemd
- Unit tests/Functional tests via Selenium & pytest (just few tests yet)
- Logs with Sentry (old configs format yet)
- Makefile for console commands
- Design with Bootstrap 4

### Modules:
- Blog: excerpt/content, post image, markdown editor
- Accounts: custom user model via AbstractBaseUser, Custom superuser create command

### Known bugs:
Sometimes Ansible throw apt or dns resolution errors.
If just play playbook again, error will gone.
Don't know how to cure yet.

## History:
1. First release on 30.09.2019
2. Moved to new config on Sentry

## TODO (in plans, may be changed):
- Docker version (add ansible-docker, fabfile-docker, Makefile)
- CI with CircleCI
- Add db backup/restore
- Add auto tests before git push on dev
- Add Linux development environment documentation
- Improvements in blog and accounts modules
- Move to WSL2 when it will be ready and worth it
- Make search in blog
- Make skin system (Bootstrap/Raw HTML)
- Make monitoring with Prometheus/Grafana
- Try LXD
- Translation to Russian
- Admin SPA with VueJS
- Add powershell bootstrap script for Windows
- Look to Traefic

# Prepare development environment on Windows 10

## Register at services
Register at [Sentry](https://sentry.io)
Register at [CircleCI](https://circleci.com)

## Install software

Manually:
1) Install [Virtualbox](https://www.virtualbox.org/)
2) Install [Vagrant](https://www.vagrantup.com/)
3) Install [WSL](https://docs.microsoft.com/ru-ru/windows/wsl/install-win10)
4) Install [Pycharm](https://www.jetbrains.com/pycharm/)
5) Install [PgAdmin](https://www.pgadmin.org/)
6) Install [MkCert](https://github.com/FiloSottile/mkcert) # local CA
7) [Optional] Install [Powershell Core](https://github.com/PowerShell/PowerShell)
8) [Optional] Install [OpenSSL](https://www.openssl.org/)

You can install all of this via [Choco](https://https://chocolatey.org/install/) and Powershell:
(But don't mix manual installed programs with programs installed with choco):

```powershell
# 1. Run Powershell with admin privileges
# 2. Install Choco:
PS> Set-ExecutionPolicy Bypass -Scope Process -Force; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
# 3. Install software:
PS> choco install virtualbox vagrant pycharm pgadmin4 powershell-core mkcert openssl
# 4. Check is WSL exists:
PS> wsl
# 5. Install WSL, if not installed:
PS> Enable-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux
PS> Invoke-WebRequest -Uri https://aka.ms/wsl-ubuntu-1804 -OutFile Ubuntu1804.appx -UseBasicParsing
PS> Add-AppxPackage .\Ubuntu1804.appx
```

## Prepare virtual machines with WSL, Vagrant, Virtualbox

### Explanation
If you develop on Windows for Linux, it's hard to setup environment. For example:
We have WSL v.1 now, but docker not working in WSL without some work.
Docker for windows depends on Hyper-V, Hyper-V conflicts with Virtualbox/Vagrant.
So we must setup dev VM, and configure Pycharm for deploy sources on save to this VM.
If we want to test Ansible/Fabric on clear system, it's better to store sources and ssh config in WSL,
so we can easily destroy and re-create the dev/staging VMs.

### Add local development root certificates to trusted store:
```powershell
# Look for local CA certificates path:
PS> mkcert -CAROOT
%USERPROFILE%\AppData\Local\mkcert
# Copy fabric\local_certs\rootCA-key.pem to %USERPROFILE%\AppData\Local\mkcert\rootCA-key.pem
# Copy fabric\local_certs\chain.pem to %USERPROFILE%\AppData\Local\mkcert\rootCA.pem
PS> mkcert -install
```

### Prepare source folder and run virtual machines
```powershell
PS> mkdir d:\webapps
PS> cd d:\webapps
PS> git clone https://github.com/ram0973/djblog/
PS> cd djblog
PS> vagrant box update
PS> vagrant up dev staging
# Useful commands:
# vagrant snapshot list
# vagrant snapshot save snapshot_name
# vagrant snapshot restore snapshot_name
# vagrant box prune - delete old boxes
```
Run another Powershell console and enter:
```
PS> wsl
```
## Prepare WSL environment
Next in WSL prompt:

```bash
# You must already setup your environment,
# for example, https://github.com/ram0973/dotfiles:
# sudo apt-get update
# sudo apt-get upgrade
# git clone https://github.com/ram0973/dotfiles ~/dotfiles

$ sudo ln -sf /mnt/d/webapps/ /webapps # only once, /mnt/d/webapps/ is path to d:\webapps in WSL
$ cd /webapps/djblog
# check existing ssh keys
$ ls -al ~/.ssh

# create key if needed or skip and copy your key to ~/.ssh/id_rsa, if existed
$ ssh-keygen -t rsa -b 4096 -C "your_mail@your_domain"
$ chmod 600 ~/.ssh/config
$ chmod 400 ~/.ssh/id_rsa

# Ssh-agent: add next two lines to ~/.bashrc
$ eval "$(ssh-agent -s)"
$ ssh-add ~/.ssh/id_rsa

$ source ~/.bashrc

# Go to github and paste contents of ~/.id_rsa.pub there https://github.com/settings/ssh/new
# Test key on github
$ ssh -T git@github.com
# change passphrase if desired: $ ssh-keygen -p
```

Write in ~/.ssh/config:
```
Host dev
  Hostname localhost
  Port 2222
  User vagrant
  IdentityFile ~/.ssh/id_rsa
  StrictHostKeyChecking no
Host staging
  Hostname localhost
  Port 2223
  User vagrant
  IdentityFile ~/.ssh/id_rsa
  StrictHostKeyChecking no
Host prod
  Hostname domain_name
  Port 22
  User user_name
  IdentityFile ~/.ssh/id_rsa
```

$ ./bootstrap.sh

At this point you can return to powershell console and save virtualbox snapshots :
PS> vagrant snapshot save snapshot_name

## Deploy with Ansible/Fabric to dev/staging:

Return to WSL prompt:

Fabric:
```
$ source venv/bin/activate
$ fab -l
$ fab -e -H dev deploy-local --env=dev
$ fab -e -H staging deploy-local --env=staging
$ fab -H dev,staging,prod -- uname -a # run some command oh host(s)
```
Ansible:
```
$ ansible-playbook ansible/deploy-local.yml -i ansible/hosts.ini --limit dev
$ ansible-playbook ansible/deploy-local.yml -i ansible/hosts.ini --limit staging
# -v with debug, --tags= with tags
```
## Run on dev:
Open new wsl prompt and run dev server:
```bash
$ ssh dev
$ cd /webapps/djblog
$ . venv/bin/activate
$ make runserver
```
Open your browser and go to https://localhost/

## Run on staging:

Open your browser and go to https://localhost:444/

## Deploy and run with Ansible/Fabric to production:
On WSL prompt:
```bash
$ ssh prod
$ sudo visudo
# At the end add:
# your_username ALL=(ALL) NOPASSWD: ALL
# Get SSL/TLS certificates on production, with wildcards
$ certbot certonly --manual --preferred-challenges=dns --email your@email --server https://acme-v02.api.letsencrypt.org/directory --agree-tos -d your_domain -d *.your_domain
$ sudo crontab -e
# add: @monthly certbot renew

Next on WSL prompt:
```bash
$ ssh-copy-id -i ~/.ssh/id_rsa.pub prod
```
Fabric:
```bash
$ fab -e -H prod deploy-prod
```
Ansible:
```bash
$ ansible-playbook ansible/deploy.yml -i ansible/hosts.ini --limit prod # one host
```

Open your browser and go to https://your_domain/

## Configure Pycharm

<details><summary>View screenshots</summary>
<img src="https://github.com/ram0973/djblog/blob/master/screenshots/vagrant_sftp_connection.png" width="597" height="504">
</details>

Pycharm: configure deployment to Vagrant virtual machine:

1. Check hosts in %USERPROFILE\.ssh\known_hosts or simply delete it.

**Tools - Deployment - Configuration**:

Connection type: SFTP;
SFTP host: 127.0.0.1; Port: 2222; User name: vagrant;
Authentication: key pair;
Deployment path: /webapps/djblog;
Excluded: venv, .idea, .vagrant

**Tools - Deployment - Automatic uploads**: always.

# Tests

```bash
$ source core/.env
$ pytest --cov=. # All tests, OR:
$ make tests # All tests
$ make unittests # Unittests only
$ make functests # Functional tests only
```
# Extras

## Flake8 checks
```bash
$ flake8 # Flake8
```

## Test gunicorn output
```bash
$ sudo curl --unix-socket /webapps/djblog/run/djblog.socket http://DOMAIN_NAME
```

## Database inspection with pgadmin4

1) Open [pgadmin4](https://www.pgadmin.org/)
2) Create server with settings:
Server: localhost
Port: 5432/5433 (dev/staging)
User: postgres
Password: postgres

## Postgresql psql console command
```bash
$ sudo -u postgres psql djblog
```
```psql
djblog=# \a # aligned/unaligned format
djblog=# \c database_name # connect to database
djblog=# \h # help
djblog=# \l # list databases
djblog=# \d # list relations (tables/sequnces)
djblog=# \du # list user roles
# IMPORTANT: user postgres MUST be SUPERUSER
djblog=# \z # list privileges
# IMPORTANT: CREATEDB - for tests, LOGIN - for migrations
# https://www.postgresql.org/docs/current/sql-grant.html
djblog=# select * from accounts_user; # show users
djblog=# \q # quit
```
TODO: make tests with in-memory sqlite db?

## Optional: How to create your own SSL certificates for local development
We will use https://github.com/FiloSottile/mkcert and openssl:
```
PS> choco install mkcert openssl
# Create and install root certificate
PS> mkcert -install
PS> mkdir d:\certs
PS> cd d:\certs
# Create localhost certificate
PS> mkcert localhost
# Create SSL-dhparams certificate:
# you can also add  C:\Program Files\OpenSSL-Win64\bin to PATH, restart shell
PS> C:\"Program Files"\OpenSSL-Win64\bin\openssl dhparam -out d:\certs\ssl-dhparams.pem 2048
```
Root certificate will be at c:\\Users\\%username%\\AppData\\Local\\mkcert\\
rootCA-key.pem -> copy to d:\certs
rootCA.pem -> copy to d:\certs and rename to chain.pem

Localhost certificates:
d:\certs\localhost-key.pem -> rename to privkey.pem
d:\certs\localhost.pem -> rename to fullchain.pem

## Installing local CA with certificates on other computer
Installing in the trust store does not require the CA key, so you can export the CA certificate and use mkcert to install it in other machines.

[Check this](https://github.com/FiloSottile/mkcert#installing-the-ca-on-other-systems)
- Look for the rootCA.pem file in mkcert -CAROOT
- Copy it to a different machine
- Set $CAROOT to its directory
- run mkcert -install

## Etc
```
sudo apt-get install --install-recommends linux-generic-hwe-18.04
```

## License
[MIT](http://opensource.org/licenses/MIT)
