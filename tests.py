import unittest
import datetime
from wp_environment import *
from core_backup import *

# Tests
class TestCode(unittest.TestCase):
    def test_count(self):
        self.assertEqual(dumpDB(str(datetime.datetime.now()), wordpress_installation['production_path'], wordpress_installation['backup_path'], wordpress_installation['sitename']), True)
        self.assertEqual(getWPVersion('/vagrant/www/wordpress-default/'), '4.7.5')
if __name__ == '__main__':
    unittest.main()