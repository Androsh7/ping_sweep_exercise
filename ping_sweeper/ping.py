"""Logic for ping sweeping"""

# Standard libraries
import asyncio
import platform
import subprocess
from ipaddress import IPv4Address

# Third-party libraries
from attrs import define, field, validators
from loguru import logger
from tqdm import tqdm


@define
class PingProgress:
    """Progress tracking for ping operations"""

    total: int = field(validator=validators.and_(validators.instance_of(int), validators.gt(0)))
    _lock: asyncio.Lock = field(factory=asyncio.Lock, init=False)
    _progress_bar: tqdm = field(validator=validators.instance_of(tqdm), init=False)

    def __attrs_post_init__(self):
        self._progress_bar = tqdm(total=self.total, desc="Pinging", unit="IP")

    async def update(self):
        """Increment the progress by one"""
        async with self._lock:
            self._progress_bar.update(1)


async def ping(ip: IPv4Address, timeout_ms: int) -> bool:
    """Pings an IP address and returns the result

    Args:
        ip: The IP address to ping
        timeout_ms: The timeout in milliseconds
    Returns:
        Whether the ping was successful or not
    """
    if platform.system() == "Windows":
        command = ["ping", "-n", "1", "-w", str(timeout_ms), str(ip)]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout_ms), str(ip)]
    process = await asyncio.create_subprocess_exec(*command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    await process.wait()
    return process.returncode == 0


async def ping_worker(name: str, ip_queue: asyncio.Queue, reachable_ips: list, timeout_ms: int, progress: PingProgress):
    """Worker to ping IP addresses from the queue

    Args:
        name: The name of the worker
        ip_queue: The queue of IP addresses to ping
    """
    try:
        while True:
            ip = await ip_queue.get()
            if await ping(ip, timeout_ms=timeout_ms):
                logger.trace("{} - {} is reachable", name, ip)
                reachable_ips.append(ip)
            await progress.update()
            ip_queue.task_done()
    except asyncio.CancelledError:
        pass


async def ping_range(ip_set: set[IPv4Address], worker_count: int, timeout_ms: int) -> set[IPv4Address]:
    """Pings a set of IP addresses

    Args:
        ip_list: The IP addresses to ping
        workers: The number of concurrent workers
    Returns:
        A set of reachable IP addresses
    """
    # Create queue
    ip_queue = asyncio.Queue()
    reachable_ips = []

    # Initialize progress tracking
    progress = PingProgress(total=len(ip_set))

    # Build workers
    workers = []
    for i in range(1, worker_count + 1):
        workers.append(
            asyncio.create_task(
                ping_worker(
                    name=f"worker-{i}",
                    ip_queue=ip_queue,
                    reachable_ips=reachable_ips,
                    timeout_ms=timeout_ms,
                    progress=progress,
                )
            )
        )
    logger.debug("Started {} workers", worker_count)

    # Add IPs to queue
    for ip in ip_set:
        await ip_queue.put(ip)
    logger.debug("Added {} IPs to the queue", len(ip_set))

    # Wait until the queue is complete
    await ip_queue.join()

    # Cancel workers
    for worker in workers:
        worker.cancel()
    await asyncio.gather(*workers, return_exceptions=True)
    logger.debug("Stopped {} workers", worker_count)

    return set(reachable_ips)
