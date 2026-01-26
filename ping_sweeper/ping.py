"""Logic for ping sweeping"""

# Standard libraries
import platform
import re
import subprocess
from ipaddress import IPv4Address, IPv4Network

IP_REGEX = r"(\d{1,3}\.){3}\d{1,3}"
IP_RANGE_REGEX = rf"{IP_REGEX}-{IP_REGEX}"
IP_NETWORK_REGEX = rf"{IP_REGEX}\/\d{{1,2}}"


def ping(ip: IPv4Address) -> bool:
    """Pings an IP address and returns the result

    Args:
        ip: The IP address to ping

    Returns:
        Whether the ping was successful or not
    """
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", str(ip)]
    else:
        command = ["ping", "-c", "1", str(ip)]
    result = subprocess.run(command, check=False, capture_output=True)
    return result.returncode == 0


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


def ping_range(ip_set: set[IPv4Address]):
    """Pings a set of IP addresses

    Args:
        ip_list: The IP addresses to ping
    """
    reachable_ips = []
    for ip in sorted(ip_set):
        if ping(ip):
            reachable_ips.append(str(ip))
            print(f"{ip} is reachable")
        else:
            print(f"{ip} is not reachable")

    print("---- Ping Sweep Complete ----")
    print(f"Reached {len(reachable_ips)}/{len(ip_set)} IP addresses:")
    for ip in reachable_ips:
        print(f" - {ip}")
