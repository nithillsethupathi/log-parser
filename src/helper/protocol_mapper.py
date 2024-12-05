import csv

'''
A parser to parse all the protocols from protocol-numbers.csv file. Will return a dictionary in the format {'6': 'tcp'}
'''


class ProtocolMapper:
    def __init__(self, protocol_file):
        self.protocol_file = protocol_file
        self.protocol_mapping = {}
        self.load_mappings()

    def load_mappings(self):
        try:
            with open(self.protocol_file, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    if any(field.strip() for field in row):
                        self.protocol_mapping[row[0]] = row[1].lower()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Protocol mapper file not found: {self.protocol_file}")

    # get protocol_mapping value (which is the name) given a key. will return None if key is not found
    def get_protocol_name(self, protocol_number):
        return self.protocol_mapping.get(protocol_number)
