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
    except:
        return  False
    return True

def getWPVersion(install_root_dir):
    """Retrieves Wordpress current version and return it as a string
    
    Args:
        install_root_dir (str): Path to public root direcotry for WP installation.

    Returns:
        version (str): WP version retrived by WP CLI, False if exception is raised
    """
    try:
        version = check_output(['wp', '--path='+install_root_dir, 'core', 'version'])
    except:
        print('Oooops seems like WP-CLI is not working properly in your Wordpress installation')
        return  False
    return version.decode('utf-8')[0:5]

def setWpVersionName(version):
    """Takes Wordpress current version and return it as a string with '-' instead of dots
    
    Args:
        version     (str): Current WP version.

    Returns:
        versionName (str): WP version name for directory naming
    """
    versionName = ''
    for item in version:
        if item == '.':
            versionName = versionName + '-'
        else:
            versionName = versionName + item
    return versionName

def deleteWpStuff(dir_path, files, directories):
    """Erases Wordpress files and directories within root directory path
    
    Args:
        dir_path    (str): Directory path to be cleaned from WP stuff.
        files       (str); Array of file names.
        directories (str); Array of directories names.

    Returns:
        bool: True after deleting list of files
    """
    for file in files:
        try:
            os.remove(dir_path+file)
        except:
            print(file+' file does not exist in current path')
    for directory in directories:
        try:
            rmtree(dir_path+directory)
        except:
            print(directory+' directory does not exist in current path')
    return True

def copyWpStuff(origin, destination, files, directories):
    """Copies selected Wordpress installation files and dirs from production
    env to back up location
    
    Args:
        origin      (str): Directory path to be copied.
        destination (str): Directory path where WP stuff is moved to.
        files       (str); Array of file names.
        directories (str); Array of directories names.

    Returns:
        bool: True after copying all list of files and dirs, False otherwise
    """
    for file in files:
        try:
            copyfile(origin+file, destination+file)
        except:
            print('Could not copy file: '+file)
            if file != 'licencia.txt' or file != 'license.txt':
                pass
            else:
                return False
    for direcotry in directories:
        try:
            copytree(origin+direcotry, destination+direcotry)
        except:
            print('Could not copy file: '+direcotry)
            return False
    return True

def backupFiles(production_path, backup_path, files, directories):
    """Prepare backup directory if needed and backs up WP files and directpries
    
    Args:
        production_path (str): Directory path to be copied.
        backup_path     (str): Directory path where WP stuff is moved to.
        files           (str); Array of file names.
        directories     (str); Array of directories names.

    Returns:
        bool: True after preparing directory and copying all list of files and dirs, False otherwise
    """
    print('Preparing directory for wordpress copy...')
    # Clean directory
    print('Searching dor WP files to be removed...')
    try:
        # deleteWpStuff(backup_path+sitename+'-wpV-'+versionName+'/')
        deleteWpStuff(backup_path, files, directories)
    except:
        print('Something went wrong while deleteing files in destination directory')
        return False
    # Populate directory
    print('Making a copy of WP files from production directory')
    try:
        # copyWpStuff(production_path, backup_path+sitename+'-wpV-'+versionName+'/')
        copyWpStuff(production_path, backup_path, files, directories)
    except:
        print('Something went wrong while copying files to destination directory')
        return False
    # Return success 
    print('Backup is done (⌐■_■)')
    return True