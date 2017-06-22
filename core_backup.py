# Wordpress utility for backing up core files before updating version.

from subprocess import call, check_output
import os
from shutil import rmtree, copyfile, copytree

# Strings -> Bool
# Executes wp cli dump database command and return OK/FAIL status
def dumpDB(datetime, install_root_dir, backup_dir, sitename):
    """Executes wp cli dump database command

    Args:
        date                (str): String representation of date object.
        install_root_dir    (str): Path to public root direcotry for WP installation.
        sitename            (str): The name of the site to be backed up
    
    Returns:
        bool: The return value. True for success, False otherwise
    """
    date = datetime[0:10]
    time = datetime[11:19]
    try:
        call(['wp', '--path='+install_root_dir, 'db', 'export', backup_dir+sitename+'-'+date+'-at-'+time[0:2]+'-'+time[3:5]+'-'+time[6:]+'.sql'])
        # call(['wp', '--path=/vagrant/www/wordpress-default/', 'db', 'export', '../bkp/sinembargo-'+date+'-at-'+time[0:2]+'-'+time[3:5]+'-'+time[6:]+'.sql'])
    except:
        print('Oooops seems like WP-CLI is not working properly in your Wordpress installation')
        return  False
    return True