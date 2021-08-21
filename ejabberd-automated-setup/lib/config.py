class Config():
    def __init__(self, rootDir, settings):
        for line in settings:
            if (line.startswith('#') or len(line) == 0 or not ':' in line):
                continue
            
            line = line.replace('\n', '')

            if (line.startswith('distro: ')):
                self.distro = line.replace('distro: ', '').strip()

            if (line.startswith('ejabberd_version: ')):
                self.ejabberd_version = line.replace('ejabberd_version: ', '').strip()

            elif (line.startswith('ejabberd_host: ')):
                self.ejabberd_host = line.replace('ejabberd_host: ', '').strip()

            elif (line.startswith('ejabberd_password: ')):
                self.ejabberd_password = line.replace('ejabberd_password: ', '').strip()
            
            elif (line.startswith('pgsql_username: ')):
                self.pgsql_username = line.replace('pgsql_username: ', '').strip()

            elif (line.startswith('pgsql_password: ')):
                self.pgsql_password = line.replace('pgsql_password: ', '').strip()

            elif (line.startswith('server_ip: ')):
                self.server_ip = line.replace('server_ip: ', '').strip()

            elif (line.startswith('webroot: ')):
                self.webroot = line.replace('webroot: ', '').strip()
            
            elif (line.startswith('ejabberd_admin_username: ')):
                self.ejabberd_admin_username = line.replace('ejabberd_admin_username: ', '').strip()

            elif (line.startswith('ejabberd_admin_password: ')):
                self.ejabberd_admin_password = line.replace('ejabberd_admin_password: ', '').strip()

            elif (line.startswith('use_existing_postgres: ')):
                self.use_existing_postgres = line.replace('use_existing_postgres: ', '').strip().lower() == 'true'


        self.rootDir = rootDir
        self.tmpDir = self.rootDir + 'temp/'
        self.config_file = self.rootDir + '.config'
        self.pgsql_schema = f'/opt/ejabberd-{self.ejabberd_version}/lib/ejabberd-{self.ejabberd_version}/priv/sql/pg.sql'
        self.ejabberdctl_path = f'/opt/ejabberd-{self.ejabberd_version}/bin/ejabberdctl'
