import urllib.request
import urllib.error
import concurrent.futures
import time

URL = "http://localhost:8080/api/orders/" # Through Nginx LB (Port 8080)
CONCURRENT_REQUESTS = 10
TOTAL_REQUESTS = 100

def make_request():
    try:
        start_time = time.time()
        with urllib.request.urlopen(URL, timeout=5) as response:
            status_code = response.getcode()
            duration = time.time() - start_time
            return status_code, duration
    except urllib.error.HTTPError as e:
        return e.code, time.time() - start_time
    except Exception as e:
        return str(e), 0

def run_simulation():
    print(f"Starting load simulation on {URL}...")
    print(f"Concurrent: {CONCURRENT_REQUESTS}, Total: {TOTAL_REQUESTS}")
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CONCURRENT_REQUESTS) as executor:
        futures = [executor.submit(make_request) for _ in range(TOTAL_REQUESTS)]
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
            
    success_count = sum(1 for res in results if res[0] == 200)
    avg_duration = sum(res[1] for res in results if isinstance(res[1], (int, float))) / len(results) if results else 0
    
    print("\n--- Results ---")
    print(f"Total Requests: {len(results)}")
    print(f"Successful Requests: {success_count}")
    print(f"Failed Requests: {len(results) - success_count}")
    print(f"Average Response Time: {avg_duration:.4f}s")

if __name__ == "__main__":
    run_simulation()
