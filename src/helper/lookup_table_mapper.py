import csv

'''
A Parser to parse the lookup table csv file. Stores the lookup_table as a dictionary in the format {(dstport, protocol): tag}
'''


class LookupMapper:
    def __init__(self, lookup_file):
        self.lookup_file = lookup_file
        self.lookup_table = {}
        self.parse_lookup()

    def parse_lookup(self):
        try:
            with open(self.lookup_file, "r") as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                for row in csv_reader:
                    if any(field.strip() for field in row) and (row[0], row[1].lower()) not in self.lookup_table:
                        self.lookup_table[(
                            row[0], row[1].lower())] = row[2].lower()
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Lookup file not found: {self.lookup_file}")

    # get dictionary value given a key
    def get_tag(self, dstport, protocol):
        return self.lookup_table.get((dstport, protocol))
