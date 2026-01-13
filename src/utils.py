"""Utility functions for the ping sweeper"""

# Standard libraries
import csv
import json
import re
from pathlib import Path
from ipaddress import IPv4Address, IPv4Network


IP_REGEX = r"(\d{1,3}\.){3}\d{1,3}"
IP_RANGE_REGEX = rf"{IP_REGEX}-{IP_REGEX}"
IP_NETWORK_REGEX = rf"{IP_REGEX}\/\d{{1,2}}"


def parse_ip_list(ip_range: str) -> set[IPv4Address]:
    """Pings an IP address range

    Args:
        ip_range: The range of IP addresses to ping

    Returns:
        A set of IPv4 addresses to ping
    """

    # Parse the IP range
    ip_list = []
    for ip in ip_range.split(","):
        ip = ip.strip()
        if re.match(IP_RANGE_REGEX, ip):
            start_ip_str, end_ip_str = ip.split("-")
            for ip_int in range(int(IPv4Address(start_ip_str)), int(IPv4Address(end_ip_str)) + 1):
                ip_list.append(IPv4Address(ip_int))
        elif re.match(IP_NETWORK_REGEX, ip):
            network = IPv4Network(ip, strict=False)
            ip_list.extend(network.hosts())
        elif re.match(IP_REGEX, ip):
            ip_list.append(IPv4Address(ip))
        else:
            print(f"ERROR: Invalid IP address/range/network: {ip}")
    # Remove duplicates
    return set(ip_list)


def save_results_to_csv(reachable_ips: set[IPv4Address], all_ips: set[IPv4Address], output_file: Path):
    """Saves reachable IP addresses to a CSV file

    Args:
        reachable_ips: A set of reachable IP addresses
        all_ips: A set of all IP addresses in the network
        output_file: The output CSV file path
    """
    with open(file=output_file, mode="w", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["IP Address", "Reachable"])
        for ip in sorted(all_ips):
            writer.writerow([str(ip), ip in reachable_ips])


def save_results_to_json(reachable_ips: set[IPv4Address], all_ips: set[IPv4Address], output_file: Path):
    """Saves reachable IP addresses to a JSON file

    Args:
        reachable_ips: A set of reachable IP addresses
        all_ips: A set of all IP addresses in the network
        output_file: The output JSON file path
    """
    results = []
    for ip in sorted(all_ips):
        results.append({"ip_address": str(ip), "reachable": ip in reachable_ips})
    with open(file=output_file, mode="w", encoding="utf-8") as json_file:
        json.dump(results, json_file, indent=4)

def save_results_to_text(reachable_ips: set[IPv4Address], all_ips: set[IPv4Address], output_file: Path):
    """Saves reachable IP addresses to a text file

    Args:
        reachable_ips: A set of reachable IP addresses
        all_ips: A set of all IP addresses in the network
        output_file: The output JSON file path
    """
    with open(file=output_file, mode="w", encoding="utf-8") as text_file:
        for ip in sorted(all_ips):
            text_file.write(f'{ip} is {"reachable" if ip in reachable_ips else "not reachable"}\n')

def read_ip_list_from_text_file(input_file: Path) -> set[IPv4Address]:
    """Reads an IP address list from a text file

    Args:
        input_file: The file to read the IP addresses from

    Returns:
        A set of IPv4 addresses to ping
    """
    ip_list_str = ""
    with open(file=input_file, mode="r", encoding="utf-8") as text_file:
        for line in text_file.readlines():
            if line.startswith("#") or not line.strip():
                continue
            ip_list_str += line.strip() + ","
    return parse_ip_list(ip_list_str.rstrip(","))

def read_ip_list_from_csv_file(input_file: Path) -> set[IPv4Address]:
    """Reads an IP address list from a csv file

    Args:
        input_file: The file to read the IP addresses from

    Returns:
        A set of IPv4 addresses to ping
    """
    ip_list_str = ""
    with open(file=input_file, mode="r", encoding="utf-8") as csv_file:
        reader = csv.reader(csv_file)
        # Skip header
        next(reader)
        for row in reader:
            ip_list_str += row[0].strip() + ","
    return parse_ip_list(ip_list_str.rstrip(","))


def read_ip_list_from_json_file(input_file: Path) -> set[IPv4Address]:
    """Reads an IP address list from a json file

    Args:
        input_file: The file to read the IP addresses from

    Returns:
        A set of IPv4 addresses to ping
    """
    ip_list_str = ""
    with open(file=input_file, mode="r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        for ip in data:
            ip_list_str += ip.strip() + ","
    return parse_ip_list(ip_list_str.rstrip(","))
