# Ping Sweeper

A simple ping sweeper that accepts individual IP addresses `127.0.0.1,1.1.1.1`, IP address ranges `1.1.1.1-1.1.1.255`, and IP networks `127.0.0.1/24` as arguments and includes functionality to read/write from/to files in various formats (csv, json, text)

## Usage

```
usage: Ping Sweeper [-h] [--ping PING] [--input INPUT] [--output OUTPUT] [--input-format {json,csv,text}] [--output-format {json,csv,text}] [-v]

A python program to ping a range of IP addresses

options:
  -h, --help            show this help message and exit
  --ping, -p PING       The range of IP addresses to scan
  --input, -i INPUT     The input file to read IP addresses from
  --output, -o OUTPUT   The output file to write results to
  --input-format, -if {json,csv,text}
                        The input file format
  --output-format, -of {json,csv,text}
                        The output file format
  -v, -version          show program's version number and exit
```

## Build

To install requirements run `pip install .` (`pip install .[dev]` for development requirements)
