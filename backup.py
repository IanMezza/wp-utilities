"""Do back up using env file"""
import datetime
from wp_environment import wordpress_installation as wp
from utility import *

def doBackup(wp_install, date):
    production_path = wp_install['production_path']
    backupPath = wp_install['backup_path']
    sitename = wp_install['sitename']
    files = wp_install['files']
    directories = wp_install['directories']
    version = setWpVersionName(getWPVersion(production_path))
    # print('Preparing directory for wordpress copy...')
    # Verify if backup directory already exists\
    if os.path.isdir(backupPath+sitename+'wpV'+version):
        print('Making a dump of the production database')
        if dumpDB(date, production_path, backupPath, sitename):
            print('SQL file has been exported')
            backupFiles(production_path, backupPath+sitename+'wpV'+version+'/', files, directories)
        else:
            print('Database could not be dumped, stoping the rest of the script')
            return False
    else:
        try:
            print('Creating new directory for backup')
            os.mkdir(backupPath+sitename+'wpV'+version)
            print('Making a dump of the production database')
            if dumpDB(date, production_path, backupPath, sitename):
                print('SQL file has been exported')
                backupFiles(production_path, backupPath+sitename+'wpV'+version+'/', files, directories)
            else:
                print('Database could not be dumped, stoping the rest of the script')
                return False
        except:
            print('Couldnt create backup directory')
            return False

doBackup(wp, str(datetime.datetime.now()))