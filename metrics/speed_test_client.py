import socket
import json
import time
import concurrent.futures
import os
import matplotlib.pyplot as plt

PAYLOAD_SIZE = 4096
JSON_FILE = "test_client_metrics.json"
MAX_CONCURRENT_QUERIES = 1000000  # Maximum number of concurrent queries
TEST_FILES_PATH = "./"  # Folder where the test files are stored

def send_query(host: str, port: int, query: dict) -> float:
    """Send a query to the TCP server and return the execution time in milliseconds."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        query_json = json.dumps(query)
        print(f"DEBUG: Sending query: {query_json}")  # Add this line
        start_time = time.time()
        client_socket.sendall(query_json.encode('utf-8'))
        response = client_socket.recv(PAYLOAD_SIZE).decode('utf-8')
        exec_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        client_socket.close()
        return exec_time
    except Exception as e:
        print(f"DEBUG: Error in client communication: {e}")
        return -1


def read_file_content(file_size: int) -> str:
    """Read content from a file corresponding to the given size."""
    file_path = os.path.join(TEST_FILES_PATH, f"test_file_{file_size}.txt")
    print(file_path)
    try:
        with open(file_path, 'r+') as f:
            content = f.read().strip()
        return content
    except FileNotFoundError:
        print(f"DEBUG: File for size {file_size} not found.")
        return ""
    
def test_file_size(file_size: int, num_queries: int) -> float:
    """Send multiple queries to the test server for a specific file size and record execution time."""
    host = '0.0.0.0'
    port = 44445
    file_content = read_file_content(file_size)

    if not file_content:
        print(f"DEBUG: Skipping test for file size {file_size}.")
        return -1

    # Prepare the query string
    query_string = {
        "query_string": file_content.splitlines()[0],  # Send the first line as query
        "algorithm": ''  # Add algorithm to the query
    }

    exec_times = []
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(send_query, host, port, query_string) for _ in range(num_queries)]
        for future in concurrent.futures.as_completed(futures):
            exec_time = future.result()
            if exec_time != -1:
                exec_times.append(exec_time)

    # Ignore first query execution (cold start)
    if len(exec_times) > 1:
        exec_times = exec_times[1:]

    avg_exec_time = sum(exec_times) / len(exec_times) if exec_times else 0
    return avg_exec_time


def performance_test(file_size):
    """Run performance tests across different file sizes and number of queries."""
    num_queries_list = [1, 50, 100, 200, 500, 1000, 10000]  # Varying the number of concurrent queries

    # Load existing performance data if the file exists
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            performance_data = json.load(f)
    else:
        performance_data = {}

    if file_size not in performance_data:
        performance_data[file_size] = {}

    print(f"DEBUG: Testing file size {file_size} lines.")
    
    for num_queries in num_queries_list:
        print(f"DEBUG: Running {num_queries} concurrent queries.")
        avg_exec_time = test_file_size(file_size, num_queries)
        if avg_exec_time != -1:
            performance_data[file_size][num_queries] = avg_exec_time
            print(f"DEBUG: Avg exec time for {num_queries} queries: {avg_exec_time:.2f} ms")

    # Save the updated performance data back to the JSON file
    with open(JSON_FILE, 'w') as f:
        json.dump(performance_data, f, indent=4)

    return performance_data

def plot_performance_chart(performance_data):
    """Plot the performance data and save it as a PDF."""
    for file_size, query_data in performance_data.items():
        num_queries = list(query_data.keys())
        exec_times = [query_data[q] for q in num_queries]
        
        # Ignore first element (first query count) in plotting
        if len(num_queries) > 1:
            num_queries = num_queries[1:]
            exec_times = exec_times[1:]
        
        plt.plot(num_queries, exec_times, label=f'File Size {file_size}')

    plt.xlabel('Number of Queries (log scale)')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.xscale('log')  # Use logarithmic scale for better visualization
    plt.legend()
    plt.grid(True)
    
    # Save plot as PDF
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'speed_test_report_{current_time}.pdf')
    plt.show()

def plot_bar_chart(performance_data):
    """Plot a bar chart of performance data."""
    num_queries = []
    execution_times = {key: [] for key in performance_data.keys()}

    for file_size, query_data in performance_data.items():
        for query_count, exec_time in query_data.items():
            if query_count not in num_queries:
                num_queries.append(query_count)
            execution_times[file_size].append(exec_time)

    bar_width = 0.15
    x_indices = range(len(num_queries))

    for i, (file_size, times) in enumerate(execution_times.items()):
        plt.bar([x + bar_width * i for x in x_indices], times, width=bar_width, label=f'File Size {file_size}')

    plt.xlabel('Number of Queries')
    plt.ylabel('Avg Execution Time (ms)')
    plt.title('Execution Time vs Number of Queries')
    plt.xticks([x + bar_width for x in x_indices], num_queries)
    plt.legend()
    plt.grid(axis='y')

    current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
    plt.savefig(f'bar_chart_report_{current_time}.pdf')
    plt.show()



if __name__ == "__main__":
    # Change the file_size as needed for each run
    file_size = 1000000  # For this example, testing with a file size of 10,000
    performance_data = performance_test(file_size)
    plot_performance_chart(performance_data)
