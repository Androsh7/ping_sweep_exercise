"""Main logic"""

# Standard libraries
import argparse

# Project libraries
from ping_sweeper.ping import parse_ip_list, ping_range

PROGRAM_NAME = "Ping Sweeper"
VERSION = "0.1.0"


def main():
    """Main function"""
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="A python program to ping a range of IP addresses")
    parser.add_argument("--ping", "-p", required=True, type=str, help="The range of IP addresses to scan")
    parser.add_argument("-v", "-version", action="version", version=f"{PROGRAM_NAME} v{VERSION}")
    args = parser.parse_args()
    if args.ping:
        ip_set = parse_ip_list(args.ping)
        ping_range(ip_set)


if __name__ == "__main__":
    main()
