import unittest
import os
import sys
from unittest.mock import patch
from io import StringIO

class TestCLI(unittest.TestCase):
    def setUp(self):
        # Remove data files before each test
        data_dir = os.path.join(os.path.dirname(__file__), '../data')
        for fname in ['users.json', 'projects.json', 'tasks.json']:
            fpath = os.path.join(data_dir, fname)
            if os.path.exists(fpath):
                os.remove(fpath)

    @patch('sys.argv', ['main.py', 'add-user', '--name', 'Alex', '--email', 'alex@example.com'])
    def test_add_user(self):
        from main import main
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn('Alex <alex@example.com>', fake_out.getvalue())

    @patch('sys.argv', ['main.py', 'add-user', '--name', 'Sam', '--email', 'sam@example.com'])
    def test_add_another_user(self):
        from main import main
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            self.assertIn('Sam <sam@example.com>', fake_out.getvalue())

if __name__ == "__main__":
    unittest.main()
