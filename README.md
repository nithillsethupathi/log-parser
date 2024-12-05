# log-parser

Python script to parse and process logs that will identify and categorize flows based on lookup table

## Prereq

Python3

## Usage

1. **Clone the repository**
2. **Navigate to src**
```cd src```
3. **Run the Script**. The files mentioned below are sample files. Can be replaced with your own file. 
```bash 
python main.py --log_file resources/logs_1.txt --lookup_file resources/lookup_1.csv --output_file output/output.txt
```
4. **Navigate to output.txt to read the parsed output** ```src/output/output.txt```

## Testing

1. Unit tests have been written and sample file was created and tested for the expected output (output.txt contains the output derived from the sample log file)
1. To run all the tests, from the root directory run the following command:
```bash
python -m unittest discover    
```

## Assumptions
- Utilized protocol-number from (https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) to convert decimal given in logs to keyword
- Supports only default log version 2 format (as per the version 2 format, going by 0 index dstport is at index 6 and protocol is at index 7)
- Supports only txt for log file. csv for lookup.
- Used this doc for flow log reference: https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html
- The first part of the output, marks the tag as "Untagged" if not in lookup table
- The second part of the output, displays all the port to protocol combination and its count. This is independent of tags.
- The matches are case insesitive. tags and port names are converted to lower case for comparison purpose, and is later stored in output in lower case