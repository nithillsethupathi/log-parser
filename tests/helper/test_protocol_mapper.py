from src.helper import ProtocolMapper
import os
import unittest

current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, '..', 'resources')
protocol_path = os.path.join(resources_dir, 'protocol_test.csv')


class TestProtocolMapper(unittest.TestCase):

    def test_load_mappings(self):
        mapper = ProtocolMapper(protocol_path)
        self.assertEqual(mapper.protocol_mapping['6'], 'tcp')
        self.assertEqual(mapper.protocol_mapping['4'], 'ipv4')

    def test_file_not_found(self):
        with self.assertRaises(FileNotFoundError) as e:
            ProtocolMapper('aa.csv')
        self.assertIn('Protocol mapper file not found', str(e.exception))

    def test_invalid_number(self):
        mapper = ProtocolMapper(protocol_path)
        self.assertIsNone(mapper.get_protocol_name('100'))

    def test_valid_number(self):
        mapper = ProtocolMapper(protocol_path)
        self.assertEqual(mapper.get_protocol_name('6'), 'tcp')


if __name__ == '__main__':
    unittest.main()
