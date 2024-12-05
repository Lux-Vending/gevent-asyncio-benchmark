from gevent import monkey
monkey.patch_all()

import gevent
import requests
from benchmark_utils import measure_memory, measure_cpu, run_benchmark, N_REQUESTS, TEST_URL
from memory_profiler import profile
import time

def gevent_fetch(url, session):
    # Create a large payload
    payload = {'data': 'x' * 1000000}  # 1MB of data
    try:
        return session.post(url, json=payload, timeout=(10, 30))
    except Exception as e:
        print(f"Error in gevent_fetch: {e}")

@profile
def benchmark_gevent():
    # Remove the monkey.patch_all() from here since we moved it to the top
    
    start_mem = measure_memory()
    start_cpu = measure_cpu()
    start_time = time.time()
    
    # Create a session with connection pooling
    session = requests.Session()
    adapter = requests.adapters.HTTPAdapter(
        pool_connections=200,
        pool_maxsize=200,
        pool_block=False
    )
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    
    # Create and run jobs with the session
    jobs = [gevent.spawn(gevent_fetch, TEST_URL, session) for _ in range(N_REQUESTS)]
    gevent.joinall(jobs, timeout=60)
    
    # Clean up
    session.close()
    
    end_time = time.time()
    end_cpu = measure_cpu()
    end_mem = measure_memory()
    
    return {
        'time': end_time - start_time,
        'memory': end_mem - start_mem,
        'cpu': (end_cpu + start_cpu) / 2
    }

if __name__ == "__main__":
    run_benchmark(benchmark_gevent, "Gevent") 