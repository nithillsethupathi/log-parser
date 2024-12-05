import argparse
from parser import LogParser
from helper import ProtocolMapper
from helper import LookupMapper

'''
Parse logs to identify flows based on lookup table

Arguments:
    <log-file>: a txt log file that will be parsed
    <lookup-file>: a csv lookup file that consists of 3 columns (dstport, protocol, tag)
    <output-file>: txt file that will record our parsed output

Usage: python main.py --log_file resources/<log-file>.log --lookup_file resources/<lookup-file>.csv
'''


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--log_file", required=True)
    parser.add_argument("--lookup_file", required=True)

    args = parser.parse_args()

    try:
        if not args.log_file.endswith(".log"):
            raise ValueError(
                "Log file format not supported. Only log is supported")
        if not args.lookup_file.endswith(".csv"):
            raise ValueError(
                "Lookup file format not supported. Only csv is supported")
        print(f"Parsing log file: {args.log_file}")
        protocol_mapping = ProtocolMapper('resources/protocol-numbers.csv')
        lookup_table = LookupMapper(args.lookup_file)
        LogParser(protocol_mapping, args.log_file, lookup_table,
                  "output/tag_results.csv", "output/port_combination_results.csv")
        print(
            f"Successfully parsed the log file: {args.log_file}. Output files can be found under the output directory")
    except Exception as e:
        print(f"Unable to parse logs: {e}")


if __name__ == "__main__":
    main()
