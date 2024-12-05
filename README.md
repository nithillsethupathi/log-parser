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