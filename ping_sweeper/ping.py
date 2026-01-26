"""Logic for ping sweeping"""

# Standard libraries
import platform
import subprocess
from ipaddress import IPv4Address

# Third-party libraries
from tqdm import tqdm


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


def ping_range(ip_set: set[IPv4Address]) -> set[IPv4Address]:
    """Pings a set of IP addresses

    Args:
        ip_list: The IP addresses to ping

    Returns:
        A set of reachable IP addresses
    """
    reachable_ips = []
    for ip in tqdm(sorted(ip_set), desc="Pinging IPs", unit="host"):
        if ping(ip):
            reachable_ips.append(ip)

    return set(reachable_ips)
