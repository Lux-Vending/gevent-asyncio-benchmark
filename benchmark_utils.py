import psutil
import statistics
import time
from memory_profiler import profile

# Constants
N_REQUESTS = 5000
TEST_URL = "https://www.example.com"

def measure_memory():
    """Return memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def measure_cpu():
    """Return CPU usage percentage"""
    return psutil.cpu_percent()

def run_benchmark(benchmark_func, name, n_runs=3):
    results = []
    
    print(f"Running {n_runs} benchmarks for {name}...")
    print(f"Making {N_REQUESTS} concurrent requests per run")
    
    for i in range(n_runs):
        print(f"\nRun {i+1}/{n_runs}")
        results.append(benchmark_func())
    
    print("\n=== RESULTS ===")
    print(f"\n{name} averages:")
    print(f"Time: {statistics.mean([r['time'] for r in results]):.2f} seconds")
    print(f"Memory: {statistics.mean([r['memory'] for r in results]):.2f} MB")
    print(f"CPU: {statistics.mean([r['cpu'] for r in results]):.2f}%")
    
    return results 