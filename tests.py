import unittest
import datetime
from wp_environment import *
from utility import *

# Tests
class TestCode(unittest.TestCase):
    def test_count(self):
        self.assertEqual(dumpDB(str(datetime.datetime.now()), wordpress_installation['production_path'], wordpress_installation['backup_path'], wordpress_installation['sitename']), True)
        self.assertEqual(getWPVersion('/vagrant/www/wordpress-default/'), '4.7.5')
        self.assertEqual(setWpVersionName('4.7.5'), '4-7-5')
        self.assertEqual(deleteWpStuff('/home/vagrant/bkp/', wordpress_installation['files'], wordpress_installation['directories']), True)
        self.assertEqual(copyWpStuff('/vagrant/www/wordpress-default/', '/home/vagrant/bkp/', wordpress_installation['files'], wordpress_installation['directories']), True)
        self.assertEqual(deleteWpStuff('/home/vagrant/bkp/', wordpress_installation['files'], wordpress_installation['directories']), True)
        self.assertEqual(backupFiles('/vagrant/www/wordpress-default/', '/home/vagrant/bkp/sinembargo-wpV-4-7-5/', wordpress_installation['files'], wordpress_installation['directories']), True)
if __name__ == '__main__':
    unittest.main()