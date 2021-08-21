# ejabberd-automated-setup

## This is an automated script to install Ejabberd, and configure it to use PostgreSQL and LetsEncrypt

**Requirements** 
- A webserver running on port 80 for letsencrypt/certbot to request certificates
- Python3, wget

Currently Supported Linux Distributions: 
- Debian (Ubuntu should work as well)
---
### What this script does
- install the latest version of Ejabberd, using the .deb file at https://www.process-one.net/en/ejabberd/downloads/
- install PostgreSQL using the package manager
- create postgres user 'ejabberd'
- create database 'ejabberd'
- import the ejabberd schema into database 'ejabberd'
- generate ejabberd.yml config file based on the settings you enter in the .config file
- install snapd
- install letsencrypt/certbot using snapd
- request necessary certificates using the `--webroot` option of certbot
- create a letsencrypt `post-renew` hook which copies the cert files to ejabberd, automatically upon renewal
- registers an admin user in ejabberd
---
### Instructions
**1. Clone this repository to your server.**\
**2. Edit the `.config` file with your desired settings as follows:**

*default settings - only change if necessary*
- `distro=debian`: this option should work on Ubuntu servers as well
- `pgsql_username=ejabberd`: postgres username for ejabberd database
- `ejabberd_admin_username=admin`: admin username for ejabberd  

*required settings - set each of these*
- `use_existing_postgres`: set to true if you have postgres installed already
- `ejabberd_version`: get current version from https://www.process-one.net/en/ejabberd/downloads/ (ex: 21.07)
- `ejabberd_host`: name of ejabberd virtual host (examples: example.org, xmpp.example.org)
- `ejabberd_password`: set password for ejabberd linux user
- `ejabberd_admin_password`: set password of default admin user for ejabberd
- `pgsql_password`: set password for postgres user 'ejabberd'
- `server_ip`: set public IP address of your server
- `email`: contact email used for letsencrypt certificates
- `webroot`: set root dir of webserver listening on port 80 (used for letsencrypt/certbot)
  - `/var/www/html` is the default webroot of apache as is packaged with debian

**3. Run setup.py -** `sudo python3 ./setup.py`
**4. Delete this repository, or at least the .config file, so your credentials aren't kept on disk**

### DNS Configuration
You can either create a wildcard DNS A record to point all subdomains (*) to your server's IP,

Or alternatively, you could create individual DNS A records for each required subdomain:
- conference  
- proxy       
- pubsub    
- upload     

Ejabberd requires the following DNS SRV records for STUN/TURN (replace example.com with your domain):
- _xmpp-client._tcp  IN example.com 5 0 5222 example.com 3600
- _xmpp-server._tcp  IN example.com 5 0 5269 example.com 3600
- _xmpps-client._tcp IN example.com 5 0 5223 example.com 3600
- _xmpps-server._tcp IN example.com 5 0 5270 example.com 3600

Ejabberd requires the following ports to be opened in your firewall:
- 5222
- 5269
- 5443
- 1883
- 3478
- 5349

### Removal
**The following commands can be used to remove and undo everything this script does**

*Make sure you know what these do, and only run the ones you are sure will not result in the loss of any data you want to keep*

- stop ejabberd service `sudo systemctl stop ejabberd`
- disable ejabberd service `sudo systemctl disable ejabberd`
- remove postgres ejabberd database `echo "drop database ejabberd;" | sudo -u postgres psql`
- remove postgres user `echo "drop user ejabberd;" | sudo -u postgres psql`
- stop postgres service `sudo systemctl stop postgresql`
- disable postgres service `sudo systemctl disable postgresql`
- remove certbot post-renew hook `sudo rm /etc/letsencrypt/renewal-hooks/post/ejabberd`
- uninstall ejabberd package `sudo apt-get remove ejabberd`
- uninstall postgres package `sudo apt-get remove postgresql`
- uninstall certbot `sudo snap remove certbot`
- uninstall snap core `sudo snap remove core`
- uninstall snap `sudo apt-get remove snapd`
- remove ejabberd files `sudo rm -rf /opt/ejabberd`
- remove ejabberd files `sudo rm -rf /opt/ejabberd-*/`
