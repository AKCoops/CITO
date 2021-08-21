import subprocess

def exec(command, shell=False):
    if (shell):
        return subprocess.run(command, shell=True)
    else:
        return subprocess.run(command.split(' '))


def configurePostgres(config):
    # create postgres user 'ejabberd'
    cmd = f'create user {config.pgsql_username} with password \'{config.pgsql_password}\';'
    exec(f'echo "{cmd}" | sudo -u postgres psql', True)

    # create database 'ejabberd'
    cmd = 'create database ejabberd;'
    exec(f'echo "{cmd}" | sudo -u postgres psql', True)

    # set database owner to 'ejabberd' user
    cmd = f'alter database ejabberd owner to {config.pgsql_username};'
    exec(f'echo "{cmd}" | sudo -u postgres psql', True)

    # import ejabberd database schema
    cmd = config.pgsql_schema
    exec(f'sudo -u ejabberd psql -d ejabberd -a -f {cmd}')


def configureEjabberd(config):
    # set password for ejabberd linux user
    exec(f'echo ejabberd:{config.ejabberd_password} | chpasswd', True)
    exec(f'sudo chsh -s /bin/bash ejabberd')
    
    # generate TLS DH parameters
    exec('openssl dhparam -out /opt/ejabberd/conf/dhparams.pem 2048')

    # generate ejabberd.yml
    exec('cp ejabberd-template.yml ejabberd.yml')
    exec(f'sed -i -e \"s/ejabberd_host/{config.ejabberd_host}/\" ./ejabberd.yml', True)
    exec(f'sed -i -e \"s/server_ip/{config.server_ip}/\" ./ejabberd.yml', True)
    exec(f'sed -i -e \"s/pgsql_username/{config.pgsql_username}/\" ./ejabberd.yml', True)
    exec(f'sed -i -e \"s/pgsql_password/{config.pgsql_password}/\" ./ejabberd.yml', True)    
    # replace default ejabberd.yml with generated version
    exec('rm /opt/ejabberd/conf/ejabberd.yml')
    exec('mv ./ejabberd.yml /opt/ejabberd/conf/ejabberd.yml')


def requestCertificates(config):
    # request required certificates using --webroot method of certbot
    host = config.ejabberd_host
    exec(f'certbot certonly --webroot -w {config.webroot} -d {host} -d conference.{host} -d proxy.{host} -d pubsub.{host} -d upload.{host} --non-interactive --agree-tos -m {config.email}')
    
    # create letsencrypt post-renew hook, in order to auto update ejabberd's certfile upon renewal
    script_path = '/etc/letsencrypt/renewal-hooks/post/ejabberd'
    cert_path = '/etc/letsencrypt/live/' + config.ejabberd_host
    ejd_certFile = '/opt/ejabberd/ejabberd.pem'
    exec('touch ' + script_path)
    exec('chmod +x ' + script_path)

    # write commands to file
    #   combine certs into one .pem
    cmd = f'cat {cert_path}/privkey.pem {cert_path}/fullchain.pem > /opt/ejabberd/ejabberd.pem'
    exec(f'echo "{cmd}" >> {script_path}', True)
    #   set owner to ejabberd user
    cmd = 'chown ejabberd ' + ejd_certFile
    exec(f'echo "{cmd}" >> {script_path}', True)
    #   set permissions
    cmd = 'chmod 640 ' + ejd_certFile
    exec(f'echo "{cmd}" >> {script_path}', True)
    #   reload ejabberd config with new cert
    exec(f'echo "sudo -u ejabberd $(sudo find /opt/ejabberd*/bin/ejabberdctl) reload-config" >> {script_path}', True)   

    # execute file to copy requested certs
    exec('sudo ' + script_path)


def registerAdminUser(config):
    exec(f'sudo -u ejabberd {config.ejabberdctl_path} register {config.ejabberd_admin_username} {config.ejabberd_host} {config.ejabberd_password}')