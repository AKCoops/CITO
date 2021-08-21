import os
import lib.common as common


def install(config):
    common.exec('apt update')
    installEjabberd(config)
    if (not config.use_existing_postgres):
        installPostgresql(config)
    common.configurePostgres(config)
    common.configureEjabberd(config)
    installCertbot(config)
    common.requestCertificates(config)
    startEjabberd()
    common.registerAdminUser(config)


def installEjabberd(config):
    # download ejabberd deb file from process-one
    package_url = f'https://www.process-one.net/downloads/downloads-action.php?file=/{config.ejabberd_version}/ejabberd_{config.ejabberd_version}-0_amd64.deb'
    filename = package_url.split('/')[-1]    
    common.exec(f'wget {package_url} -O {config.tmpDir + filename}')

    # install package
    common.exec('apt-get install ' + config.tmpDir + filename)


def installPostgresql(config):
    # install postgresql and start service
    common.exec('apt install postgresql erlang-p1-pgsql -y')
    common.exec('systemctl enable --now postgresql')


def installCertbot(config):
    common.exec('apt-get install snapd -y')
    common.exec('snap install core')
    common.exec('snap refresh core')
    common.exec('snap install --classic certbot')


def startEjabberd():
    common.exec('systemctl daemon-reload')
    common.exec('systemctl enable --now ejabberd')