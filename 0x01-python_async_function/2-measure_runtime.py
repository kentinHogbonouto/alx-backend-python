#!/usr/bin/env python3
""" Measure runtime """
import asyncio
import time


wait_n = __import__('1-concurrent_coroutines').wait_n


def measure_time(n: int, max_delay: int) -> float:
    """
    Time taken to complete an async call
    """
    time_before = time.perf_counter()
    asyncio.run(wait_n(n, max_delay))
    time_after = time.perf_counter()
    return((time_after - time_before) / n)
