import sys
import os
import unittest
import collections

current_dir = os.path.dirname(os.path.abspath(__file__))
resources_dir = os.path.join(current_dir, '..', 'resources')
log_file = os.path.join(resources_dir, 'logs_test.txt')
empty_log_file = os.path.join(resources_dir, 'empty_log.txt')
lookup_file = os.path.join(resources_dir, 'lookup_test.csv')
protocol_file = os.path.join(resources_dir, 'protocol_test.csv')

from src.parser import LogParser
from src.helper import LookupMapper
from src.helper import ProtocolMapper

class TestLogParser(unittest.TestCase):
    def setUp(self):
        self.lookup_table = LookupMapper(lookup_file)
        self.protcol_mapper = ProtocolMapper(protocol_file)
        self.output_file = 'output_test.txt'
    
    def tearDown(self):
        if os.path.exists(self.output_file):
            os.remove(self.output_file)
    
    def test_parse_file(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.output_file)
        tag_count = collections.Counter({'sv_p1': 1, 'sv_p2': 1})
        protocol_count = collections.Counter({('25', 'tcp'): 1, ('443', 'tcp'): 1})
        
        self.assertEqual(parser.tag_count, tag_count)
        self.assertEqual(parser.protocol_count, protocol_count)
    
    def test_parse_file_empty_file(self):
        parser = LogParser(self.protcol_mapper, empty_log_file, self.lookup_table, self.output_file)
        self.assertEqual(parser.tag_count, collections.Counter())
        self.assertEqual(parser.protocol_count, collections.Counter())

    def test_get_dstport_and_protocol_valid(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.output_file)
        line = '2 123456789012 eni-0a1b2c3d 10.0.1.201 198.51.100.2 443 25 6 25 20000 1620140761 1620140821 ACCEPT OK'
        dstport, protocol = parser.get_dstport_and_protocol(line)
        self.assertEqual(dstport, '25')
        self.assertEqual(protocol, '6')

    def test_get_dstport_and_protocol_invalid(self):
        parser = LogParser(self.protcol_mapper, log_file, self.lookup_table, self.output_file)
        line = 'test'
        with self.assertRaises(ValueError) as e:
            parser.get_dstport_and_protocol(line)
        self.assertIn('Log format is incorrect', str(e.exception))
    
    def test_generate_output(self):
        output_file = 'output_test.txt'
        LogParser(self.protcol_mapper, log_file, self.lookup_table, output_file)
        with open(output_file, 'r') as file:
            lines = file.readlines()
            output = ['Tag Counts: \n',
                      'Tag,Count\n',
                      'sv_p1,1\n',
                      'sv_p2,1\n',
                      'Port/Protocol Combination Counts:\n',
                      'Port,Protocol,Count\n',
                      '25,tcp,1\n',
                      '443,tcp,1\n']
        self.assertEqual(lines, output)


if __name__ == '__main__':
    unittest.main()