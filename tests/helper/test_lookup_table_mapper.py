import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, '..', 'resources')
lookup_path = os.path.join(resources_dir, 'lookup_test.csv')

from src.helper import LookupMapper

class TestLookupMapper(unittest.TestCase):

    def test_load_mappings(self):
        mapper = LookupMapper(lookup_path)
        self.assertEqual(mapper.lookup_table[('25', 'tcp')], 'sv_p1')

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as e:
            LookupMapper('aa.csv')
        self.assertIn('Lookup file not found', str(e.exception))
    
    def test_invalid_key(self):
        mapper = LookupMapper(lookup_path)
        self.assertIsNone(mapper.get_tag('100', 'a'))
    
    def test_valid_key(self):
        mapper =  LookupMapper(lookup_path)
        self.assertEqual(mapper.get_tag('25', 'tcp'), 'sv_p1')

if __name__ == '__main__':
    unittest.main()