import collections

'''
Parser engine that takes in all the inputs, processes the log and creates an output file with the parsed log
'''


class LogParser:
    def __init__(self, protocol_mapper, log_file, lookup_table, tag_file, port_combination_file):
        self.lookup_table = lookup_table
        self.protocol_mapper = protocol_mapper
        self.log_file = log_file
        self.tag_file = tag_file
        self.port_combination_file = port_combination_file
        self.tag_count = collections.Counter()
        self.protocol_count = collections.Counter()
        self.parse_file()

    # current log line to extract dstport and protocol
    def get_dstport_and_protocol(self, log_line):
        try:
            log_list = log_line.split()
            dstport, protocol = log_list[6], log_list[7]
            return dstport, protocol
        except IndexError:
            raise ValueError(f"Log format is incorrect: {log_line}")

    # helper function to generate output from the stored dictionaries
    def generate_output(self, tag_file, port_combination_file):
        with open(tag_file, 'w') as file:
            file.write("Tag,Count\n")
            for key, value in self.tag_count.items():
                file.write(f"{key},{value}\n")
        with open(port_combination_file, 'w') as file:
            file.write("Port,Protocol,Count\n")
            for (dstport, protocol_name), value in self.protocol_count.items():
                file.write(f"{dstport},{protocol_name},{value}\n")

    # function to parse and process a file
    def parse_file(self):
        try:
            with open(self.log_file, "r") as file:
                for line in file:
                    dstport, protocol = self.get_dstport_and_protocol(line)
                    protocol_name = self.protocol_mapper.get_protocol_name(
                        protocol)
                    if (dstport, protocol_name) in self.lookup_table.lookup_table:
                        tag = self.lookup_table.get_tag(dstport, protocol_name)
                        if not tag:
                            print(
                                f"Skipping line. No tag available for dstport: {dstport} and protocol: {protocol}")
                            continue
                        self.tag_count[tag] += 1
                        self.protocol_count[(dstport, protocol_name)] += 1
                    elif dstport and protocol_name:
                        self.tag_count["Untagged"] += 1
                        self.protocol_count[(dstport, protocol_name)] += 1
                    else:
                        print(f"Skipping line: {line}. protocol_name is null")
            self.generate_output(self.tag_file, self.port_combination_file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Log file not found: {self.log_file}")
        except Exception as e:
            raise RuntimeError(f"An exception occured: {e}")
