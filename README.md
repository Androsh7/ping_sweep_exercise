# Ping Sweeper

A asynchronous ping sweeper that accepts individual IP addresses `127.0.0.1,1.1.1.1`, IP address ranges `1.1.1.1-1.1.1.255`, and IP networks `127.0.0.1/24` as arguments and includes functionality to read/write from/to files in various formats (csv, json, text)

## Usage

```
usage: Ping Sweeper [-h] [--ping PING] [--input INPUT] [--output OUTPUT] [--input-format {json,csv,text}] [--output-format {json,csv,text}] [-v] [--workers WORKERS] [--timeout TIMEOUT]
                    [--log-level {TRACE,DEBUG,INFO,WARNING,ERROR,CRITICAL}]

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
  --workers, -w WORKERS
                        The number of concurrent workers (default: 50)
  --timeout, -t TIMEOUT
                        The ping timeout in milliseconds (default: 1000 ms)
  --log-level, -ll {TRACE,DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level (default: INFO)
```

## Build

To install requirements run `pip install .` (`pip install .[dev]` for development requirements)

## Test

To test install dev requirements (`pip install .[dev]`) then run `pytest`
