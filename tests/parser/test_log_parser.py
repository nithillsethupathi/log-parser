import os
import unittest
import collections

current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, '..', 'resources')
log_file = os.path.join(resources_dir, 'logs_test.log')
empty_log_file = os.path.join(resources_dir, 'empty_log.log')
lookup_file = os.path.join(resources_dir, 'lookup_test.csv')
protocol_file = os.path.join(resources_dir, 'protocol_test.csv')

from src.parser import LogParser
from src.helper import LookupMapper
from src.helper import ProtocolMapper

class TestLogParser(unittest.TestCase):
    def setUp(self):
        self.lookup_table = LookupMapper(lookup_file)
        self.protcol_mapper = ProtocolMapper(protocol_file)
        self.tag_file = 'tag_results.csv'
        self.port_combination_file = 'port_combination_results.csv'
    
    def tearDown(self):
        if os.path.exists(self.port_combination_file):
            os.remove(self.port_combination_file)
        if os.path.exists(self.tag_file):
            os.remove(self.tag_file)
    
    def test_parse_file(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.tag_file, self.port_combination_file)
        tag_count = collections.Counter({'sv_p1': 1, 'sv_p2': 1})
        protocol_count = collections.Counter({('25', 'tcp'): 1, ('443', 'tcp'): 1})
        
        self.assertEqual(parser.tag_count, tag_count)
        self.assertEqual(parser.protocol_count, protocol_count)
    
    def test_parse_file_empty_file(self):
        parser = LogParser(self.protcol_mapper, empty_log_file, self.lookup_table, self.tag_file, self.port_combination_file)
        self.assertEqual(parser.tag_count, collections.Counter())
        self.assertEqual(parser.protocol_count, collections.Counter())

    def test_get_dstport_and_protocol_valid(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.tag_file, self.port_combination_file)
        line = '2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 25 6 25 20000 1620140761 1620140821 ACCEPT OK'
        dstport, protocol = parser.get_dstport_and_protocol(line)
        self.assertEqual(dstport, '25')
        self.assertEqual(protocol, '6')

    def test_get_dstport_and_protocol_invalid(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.tag_file, self.port_combination_file)
        line = 'test'
        with self.assertRaises(ValueError) as e:
            parser.get_dstport_and_protocol(line)
        self.assertIn('Log format is incorrect', str(e.exception))
    
    def test_generate_output(self):
        tag_file = 'tag_results.csv'
        port_file = 'port_combination_results.csv'
        LogParser(self.protcol_mapper, log_file, self.lookup_table, tag_file, port_file)
        with open(port_file, 'r') as file:
            lines = file.readlines()
            port_combination_output=['Port,Protocol,Count\n',
                      '25,tcp,1\n',
                      '443,tcp,1\n']
            self.assertEqual(lines, port_combination_output)
        with open(tag_file, 'r') as file:
            lines = file.readlines()
            tag_output = ['Tag,Count\n',
                      'sv_p1,1\n',
                      'sv_p2,1\n']
            self.assertEqual(lines, tag_output)


if __name__ == '__main__':
    unittest.main()