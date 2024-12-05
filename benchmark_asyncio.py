import uvloop
import asyncio
import aiohttp
import time
from benchmark_utils import measure_memory, measure_cpu, run_benchmark, N_REQUESTS, TEST_URL, N_CONCURRENT_REQUESTS
from memory_profiler import profile

# Install uvloop
uvloop.install()

async def async_fetch(session, url):
    try:
        async with session.get(url) as response:
            await response.read()
    except Exception as e:
        print(f"Error in async_fetch: {e}")

async def run_asyncio_test():
    connector = aiohttp.TCPConnector(
        limit=0,  # No limit on simultaneous connections
        ttl_dns_cache=300,
        force_close=False  # Keep connections alive
    )
    timeout = aiohttp.ClientTimeout(
        total=60,        # Total timeout
        connect=10,      # Connection timeout
        sock_read=30     # Socket read timeout
    )
    
    sem = asyncio.Semaphore(N_CONCURRENT_REQUESTS)
    
    async def bounded_fetch(session, url):
        async with sem:
            return await async_fetch(session, url)
    
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        tasks = [bounded_fetch(session, TEST_URL) for _ in range(N_REQUESTS)]
        await asyncio.gather(*tasks)

@profile
def benchmark_asyncio():
    start_mem = measure_memory()
    start_cpu = measure_cpu()
    start_time = time.time()
    
    asyncio.run(run_asyncio_test())
    
    end_time = time.time()
    end_cpu = measure_cpu()
    end_mem = measure_memory()
    
    return {
        'time': end_time - start_time,
        'memory': end_mem - start_mem,
        'cpu': (end_cpu + start_cpu) / 2
    }

if __name__ == "__main__":
    run_benchmark(benchmark_asyncio, "Asyncio") 