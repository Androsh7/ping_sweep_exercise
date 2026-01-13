# Ping Sweeper

A simple ping sweeper that accepts individual IP addresses `127.0.0.1,1.1.1.1`, IP address ranges `1.1.1.1-1.1.1.255`, and IP networks `127.0.0.1/24` as arguments

## Usage

```
usage: Ping Sweeper [-h] --ping PING [-v]

A python program to ping a range of IP addresses

options:
-h, --help show this help message and exit
--ping, -p PING The range of IP addresses to scan
-v, -version show program's version number and exit
```

## Build

To install dev requirements run `pip install .[dev]`
