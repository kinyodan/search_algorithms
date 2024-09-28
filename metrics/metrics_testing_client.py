import socket
import json
import time
import os

PAYLOAD_SIZE = 4096
JSON_FILE = "test_client_metrics.json"


def send_query(host: str, port: int, query: dict) -> float:
    """Send a query to the TCP server and return the execution time.

    Args:
        host (str): The server hostname.
        port (int): The server port.
        query (dict): The search query (algorithm and query string).

    Returns:
        float: Time taken in milliseconds.
    """
    try:
        # Create a socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))
        query_json = json.dumps(query)

        # Record the time before sending the query
        start_time = time.time()

        # Send query
        client_socket.sendall(query_json.encode('utf-8'))

        # Receive response from server
        response = client_socket.recv(PAYLOAD_SIZE).decode('utf-8')

        # Calculate execution time
        exec_time = (time.time() - start_time) * \
            1000  # Convert to milliseconds

        print(f"DEBUG: Response: {response}")
        return exec_time

    except Exception as e:
        print(f"DEBUG: Error in client communication: {e}")
        return -1  # Return -1 on failure
    finally:
        client_socket.close()


def update_metrics(
        index: int,
        exec_times: list,
        reread_on_query: bool = False):
    """Update the test_client_metrics.json file with execution time data.

    Args:
        index (int): The index in the list representing different file sizes.
        exec_times (list): The list of execution times for this test run.
        reread_on_query (bool): Whether the file is reread on query.
    """
    json_file = JSON_FILE

    # Initialize the data structure
    if not os.path.exists(json_file):
        with open(json_file, 'w') as f:
            json.dump({}, f)

    with open(json_file, 'r+') as f:
        data = json.load(f)

        key = "execution_times"

        # Ensure 'execution_times' exists in the JSON
        if key not in data:
            data[key] = []

        # Ensure there are enough sublists for the index
        while len(data[key]) <= index:
            data[key].append([])

        # Append execution times for this index
        data[key][index].extend(exec_times)

        # Write the updated data back to the JSON file
        f.seek(0)  # Go to the start of the file
        json.dump(data, f, indent=4)
        f.truncate()  # Ensure the file is properly truncated after updating

    print(
        f"DEBUG: Execution times {exec_times} added to '{key}'.")


def run_tests(
        file_size: int,
        index: int,
        num_tests: int = 5,
        reread_on_query: bool = False):
    """Run tests to measure the server's execution time for a given file size.

    Args:
        file_size (int): The size of the test file (number of lines).
        index (int):
            Index corresponding to the file size in the JSON structure.
        num_tests (int): Number of test runs to average results.
        reread_on_query (bool):
            If the server is rereading the file on each query.
    """
    host = 'localhost'
    port = 44445
    query = {
        "query_string": "3;0;1;28;0;7;5;0"
    }

    exec_times = []

    for i in range(num_tests):
        exec_time = send_query(host, port, query)
        if exec_time != -1:
            exec_times.append(exec_time)
        else:
            print(f"DEBUG: Test failed for query {i+1}")

    # Update the metrics in the JSON file
    if exec_times:
        update_metrics(index, exec_times, reread_on_query)
    else:
        print(
            f"DEBUG: No valid execution times
            recorded for file size {file_size}.")


if __name__ == "__main__":
    # Define file sizes and their corresponding index
    file_sizes = [10000, 50000, 100000, 500000, 1000000]

    for index, file_size in enumerate(file_sizes):
        print(f"DEBUG: Running tests for file size: {file_size}")
        run_tests(file_size, index)
