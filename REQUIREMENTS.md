# Customer requirements

Create a python application that can ping a range of hosts, the application should not be a wrapper for an existing ICMP scanner like nmap, masscan, fping, nping, etc (NOTE: using cli commands like `ping` is permitted)

## Dev requirements (required)

- Functions, methods, modules, and classes should be properly documented with [docstrings](https://peps.python.org/pep-0257/)
- Project should comply with [Semantic Versioning 2.0.0](https://semver.org/)
- Project should include a [changelog](https://keepachangelog.com/en/1.1.0/)
- Project should have a descriptive README.md including how to build, run, and use the tool
- Project should comply with ruff formatting and linting suggestions
- Project should pass pylint linting with a score of at least 8
- All third-party libraries should be included in the pyproject.toml

## Beginner requirements

- ~~Program requires an interface (CLI interface is sufficient)~~ (This has already been done)
- ~~`--ping` argument should be able to accept a list of IP address, I.E: `--ping 192.168.1.1,127.0.0.1,1.1.1.1`~~
- ~~`--ping` argument should be able to accept a range of IP addresses, I.E: `--ping 127.0.0.1-127.0.0.255`~~
- ~~`--ping` argument should be able to accept a network as an argument, I.E: `--ping 127.0.0.1/23`~~
- ~~Scanner should return a summary including: total targets, reachable count, and list of reachable hosts~~

## Intermediate requirements

- ~~All beginner requirements~~
- ~~`--ping` argument should be able to accept a mix of individual IPs, IP ranges, and IP networks, I.E: `--ping 192.168.1.1,1.0.0.1-1.0.0.255,127.0.0.1/24`~~
- ~~Remove duplicate IPs before scanning~~
- ~~Add an argument to optionally read a list of IP addresses from a file (csv, json, and text)~~
- ~~Add an argument to optionally write the output to a file in a specified format (csv, json, and text)~~
- ~~Add a progress bar or progress indicator~~

## Advanced requirements

- All beginner and intermediate requirements
- OS cross-compatibility (Linux and Windows)
- Run pings simultaneously
- Add arguments to adjust concurrency and timeout
- Implement unit tests (80% coverage)
