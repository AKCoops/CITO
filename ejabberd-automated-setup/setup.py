import os
import subprocess

from lib.config import Config
import lib.common as common
import lib.debian as debian


def main():
    print('********************************************************************************')
    print('*    Automated Installation and Config of Ejabberd, PostgreSQL, LetsEncrypt    *')
    print('********************************************************************************')

    # get parent of this script
    workDir = '/'.join(os.path.realpath(__file__).split('/')[:-1]) + '/' 
        
    # parse .config file
    with open(workDir + '.config', 'r') as f:
        settings = f.readlines()
    config = Config(workDir, settings)
    
    # create temp dir if doesn't exist
    if (not os.path.exists(config.tmpDir)):
        os.makedirs(config.tmpDir)

    # run procedure for selected linux distribution
    if (config.distro == 'debian'):
        debian.install(config)
    
    else:
        print(f'Installation for linux distribution {config.distro} is not implemented yet')
        return 0


    print('********************************************************************************')
    print('*                     Installation Completed Successfully                      *')
    print('********************************************************************************')
    
    
if __name__ == "__main__":
    main()
