"""Test file I/O functions"""

# Standard libraries
from ipaddress import IPv4Address, IPv4Network
from pathlib import Path
import os
import csv
import json

# Project libraries
from src.utils import save_results_to_csv, save_results_to_json, save_results_to_text, read_ip_list_from_csv_file, read_ip_list_from_json_file, read_ip_list_from_text_file, parse_ip_list

TEST_DIRECTORY = Path(__file__).parent
ALL_IPS = set(IPv4Network("127.0.0.0/16").hosts())
REACHABLE_IPS = set(IPv4Network("127.0.0.0/24").hosts())

def test_csv_input():
    input_file_path = TEST_DIRECTORY / Path("in.csv")

    # Write data to CSV file
    with open(file=input_file_path, mode="w", encoding="utf-8", newline="") as input_file:
        writer = csv.writer(input_file)
        writer.writerow(["IPs"])
        for ip in ALL_IPS:
            writer.writerow([str(ip)])

    # Read input data from CSV file
    assert read_ip_list_from_csv_file(input_file_path) == ALL_IPS
    os.remove(input_file_path)

def test_csv_output():
    output_file_path = TEST_DIRECTORY / Path("out.csv")
    save_results_to_csv(reachable_ips=REACHABLE_IPS, all_ips=ALL_IPS, output_file=output_file_path)

    # Read data from CSV file
    all_ips_from_file = []
    reachable_ips_from_file = []
    with open(file=output_file_path, mode="r", encoding="utf-8") as output_file:
        reader = csv.reader(output_file.readlines())
        next(reader) # Skip header
        for row in reader:
            if row[1] == "True":
                reachable_ips_from_file.append(IPv4Address(row[0]))
            all_ips_from_file.append(IPv4Address(row[0]))

    assert ALL_IPS == set(all_ips_from_file)
    assert REACHABLE_IPS == set(reachable_ips_from_file)
    os.remove(output_file_path)

def test_json_input():
    input_file_path = TEST_DIRECTORY / Path("in.json")
    
    # Write data to input file
    with open(file=input_file_path, mode="w", encoding="utf-8") as input_file:
        json.dump(list(map(str, ALL_IPS)), input_file)
    
    # Read data from input file
    ALL_IPS == read_ip_list_from_json_file(input_file_path)
    
    os.remove(input_file_path)

def test_json_output():
    output_file_path = TEST_DIRECTORY / Path("out.json")

    # Write data to output file
    save_results_to_json(reachable_ips=REACHABLE_IPS, all_ips=ALL_IPS, output_file=output_file_path)

    # Read data from output file
    with open(file=output_file_path, mode="r", encoding="utf-8") as output_file:
        data_from_file = json.load(output_file)
    all_ips_from_file = []
    reachable_ips_from_file = []
    for data in data_from_file:
        if data["reachable"]:
            reachable_ips_from_file.append(IPv4Address(data["ip_address"]))
        all_ips_from_file.append(IPv4Address(data["ip_address"]))

    assert ALL_IPS == set(all_ips_from_file)
    assert REACHABLE_IPS == set(reachable_ips_from_file)
    os.remove(output_file_path)

def test_text_input():
    input_file_path = TEST_DIRECTORY / Path("input.txt")

    # Write to input file
    with open(file=input_file_path, mode="w", encoding="utf-8") as input_file:
        for index, ip in enumerate(ALL_IPS):
            input_file.write(f"{ip}\n")
            if index % 1000 == 0:
                input_file.write("# Blah Blah Blah\n")

        input_file.write("\n")

    # Read from input file
    assert ALL_IPS == read_ip_list_from_text_file(input_file_path)
    os.remove(input_file_path)

def test_text_output():
    output_file_path = TEST_DIRECTORY / Path("output.txt")

    save_results_to_text(reachable_ips=REACHABLE_IPS, all_ips=ALL_IPS, output_file=output_file_path)
    os.remove(output_file_path)

def test_ip_parser():
    ip_addresses = ["1.1.1.1", "1.1.1.2", "1.1.1.3", "1.1.1.4", "4.4.4.4"]
    ip_addresses.extend(list(map(str, IPv4Network("127.0.0.0/24").hosts())))
    result_ip_list = parse_ip_list("1.1.1.1-1.1.1.4,4.4.4.4,127.0.0.0/24")
    assert ip_addresses.sort() == list(map(str, result_ip_list)).sort()
