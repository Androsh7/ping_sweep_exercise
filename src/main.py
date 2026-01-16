"""Main logic"""

# Standard libraries
import asyncio
import argparse
import sys
from pathlib import Path

# Third-party libraries
from loguru import logger

# Project libraries
from ping import ping_range
from utils import (
    parse_ip_list,
    read_ip_list_from_csv_file,
    read_ip_list_from_json_file,
    read_ip_list_from_text_file,
    save_results_to_csv,
    save_results_to_json,
    save_results_to_text,
)

PROGRAM_NAME = "Ping Sweeper"
VERSION = "0.3.0"


async def main():
    """Main function"""
    parser = argparse.ArgumentParser(prog=PROGRAM_NAME, description="A python program to ping a range of IP addresses")
    parser.add_argument("--ping", "-p", type=str, help="The range of IP addresses to scan")
    parser.add_argument("--input", "-i", type=Path, help="The input file to read IP addresses from")
    parser.add_argument("--output", "-o", type=Path, help="The output file to write results to")
    parser.add_argument(
        "--input-format", "-if", type=str, choices=["json", "csv", "text"], default="json", help="The input file format"
    )
    parser.add_argument(
        "--output-format",
        "-of",
        type=str,
        choices=["json", "csv", "text"],
        default="json",
        help="The output file format",
    )
    parser.add_argument("-v", "-version", action="version", version=f"{PROGRAM_NAME} v{VERSION}")
    parser.add_argument("--workers", "-w", type=int, default=50, help="The number of concurrent workers (default: 50)")
    parser.add_argument("--timeout", "-t", type=int, default=1000, help="The ping timeout in milliseconds (default: 1000 ms)")
    parser.add_argument("--log-level", "-ll", type=str, choices=["TRACE", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], default="INFO", help="Set the logging level (default: INFO)")
    args = parser.parse_args()

    # Set logging level
    logger.remove()
    logger.add(sink=sys.stderr, level=args.log_level)

    if args.input and args.ping:
        parser.error("Cannot use --input and --ping together. Please choose one.")

    # Grab the input
    if args.ping:
        ip_set = parse_ip_list(args.ping)
    elif args.input:
        if args.input_format == "json":
            ip_set = read_ip_list_from_json_file(Path(args.input))
        elif args.input_format == "csv":
            ip_set = read_ip_list_from_csv_file(Path(args.input))
        elif args.input_format == "text":
            ip_set = read_ip_list_from_text_file(Path(args.input))
        else:
            parser.error("Invalid input format. Please choose from json, csv, or text.")
    else:
        parser.error("No input provided. Please use --ping or --input to provide IP addresses.")

    # Ping the IPs
    reachable_ips = await ping_range(ip_set, worker_count=args.workers, timeout_ms=args.timeout)

    # Return the output
    if args.output:
        if args.output_format == "json":
            save_results_to_json(reachable_ips, ip_set, Path(args.output))
        elif args.output_format == "csv":
            save_results_to_csv(reachable_ips, ip_set, Path(args.output))
        elif args.output_format == "text":
            save_results_to_text(reachable_ips, ip_set, Path(args.output))
        else:
            parser.error("Invalid output format. Please choose from json, csv, or text.")
    else:
        print("---- Ping Sweep Complete ----")
        print(f"Reached {len(reachable_ips)}/{len(ip_set)} IP addresses:")
        print(f' - {", ".join(map(str, reachable_ips))}')


if __name__ == "__main__":
    asyncio.run(main())
