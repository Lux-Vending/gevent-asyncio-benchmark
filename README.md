# Python Async Framework Benchmarks

A benchmarking suite comparing different Python async frameworks (currently asyncio and gevent) under high concurrency loads.

## Overview

This project provides tools to benchmark and compare the performance characteristics of:

- asyncio (with uvloop)
- gevent

The benchmarks measure:

- Execution time
- Memory usage 
- CPU utilization

## Setup

Install dependencies:
```
pip install -r requirements.txt
```


## Usage

To run the benchmarks:
```
python benchmark_asyncio.py
python benchmark_gevent.py
```

The results will be printed to the console.

* N_REQUESTS: The number of requests to make
* TEST_URL: The URL to send requests to
