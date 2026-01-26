"""Tests for ping"""

# Standard libraries
import asyncio
from ipaddress import IPv4Address

import pytest

# Project libraries
from src.ping import ping, ping_range, ping_worker


class MockProgressBar:
    async def update(input: any):
        print(f"Update worker {input}")


@pytest.mark.asyncio
async def test_ping():
    await ping(IPv4Address("127.0.0.1"), timeout_ms=1000) == True


@pytest.mark.asyncio
async def test_ping_worker():
    ip_queue = asyncio.Queue()
    await ip_queue.put(IPv4Address("127.0.0.1"))
    reachable_ips = []
    progress_bar = MockProgressBar()
    task = asyncio.create_task(
        ping_worker(name="test", ip_queue=ip_queue, reachable_ips=reachable_ips, timeout_ms=1000, progress=progress_bar)
    )
    await ip_queue.join()
    task.cancel()
    await task
    assert reachable_ips == [IPv4Address("127.0.0.1")]


@pytest.mark.asyncio
async def test_ping_range():
    ip_address_range = (
        IPv4Address("127.0.0.1"),
        IPv4Address("127.0.0.2"),
        IPv4Address("127.0.0.3"),
        IPv4Address("127.0.0.4"),
        IPv4Address("127.0.0.5"),
    )
    await ping_range(ip_set=ip_address_range, worker_count=2, timeout_ms=1000) == ip_address_range
