import json
import socket
import threading
import time
import ssl
import os
from typing import List, Optional, Dict
from lib.search_engine import search_alg_setup
from lib.configuration import load_reread_on_query_config, read_config
from metrics.metrics import set_metrics_data

# The size of the payload buffer for receiving search queries from clients.
PAYLOAD_SIZE = 4096

def get_config_path(filename: str) -> str:
    """Get the full path to the configuration file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        str: Full path to the configuration file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

def load_algorithms() -> List[str]:
    """Load the list of search algorithms from the algorithms list JSON file.

    Returns:
        List[str]: List of algorithm names.
    """
    # Getting the path to the JSON file that contains the list of algorithms.
    # The path to this file is specified inside the config.ini file.
    settings_config_file = get_config_path('config.ini')
    algorithms_list_settings = read_config(settings_config_file)
    try:
        with open(algorithms_list_settings['algorithms_list_json'], 'r') as file:
            data = json.load(file)
            return data['algorithms']
    except Exception as e:
        # Log any error encountered while loading algorithms.
        print(f"DEBUG: Failed to load algorithms: {e}")
        return []

# Load the list of algorithms at startup.
ALGORITHMS_LIST: List[str] = load_algorithms()

def check_algorithm_string(algorithm_string: str) -> bool:
    """Check if the provided algorithm string is valid.

    Args:
        algorithm_string (str): The algorithm string to validate.

    Returns:
        bool: True if the algorithm is valid, False otherwise.
    """
    return algorithm_string in ALGORITHMS_LIST

def search_in_file(file_path: str, query: Dict[str, str], reread_on_query: bool = False) -> bool:
    """Search for a string in a specified file using a specified algorithm.

    Args:
        file_path (str): Path to the file to search.
        query (Dict[str, str]): Query containing the search string and algorithm.
        reread_on_query (bool): Whether to re-read the file for each query.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    query_string: str = query['query_string']
    algorithm_string: str = query['algorithm']

    if check_algorithm_string(algorithm_string):
        # Perform the search using the specified algorithm.
        return search_alg_setup(algorithm_string, reread_on_query, file_path, query_string)

    # Log invalid algorithm string for debugging.
    print(f"DEBUG: Invalid algorithm: {algorithm_string}")
    return False

def handle_client(
    conn: socket.socket,
    addr: tuple,
    file_path: str,
    reread_on_query: bool,
    metrics_json_path: str
) -> None:
    """Handle client connections and perform search queries.

    Args:
        conn (socket.socket): The client connection socket.
        addr (tuple): The address of the client.
        file_path (str): Path to the file to search.
        reread_on_query (bool): Whether to re-read the file for each query.
        metrics_json_path (str): Path to save metrics data.
    """
    try:
        start_time = time.time()
        print(f"DEBUG: Connected with {addr}")

        # Receive the search query from the client.
        query = conn.recv(PAYLOAD_SIZE).decode('utf-8').rstrip('\x00')
        print(f"DEBUG: Search query received: '{query}'")

        # Parse the received query from JSON format.
        parsed_query = json.loads(query)

        # Check if the search string is empty or the algorithm is invalid.
        if not parsed_query.get('query_string') or parsed_query.get('algorithm') not in ALGORITHMS_LIST:
            # Set algorithm to 'tim' if the query string is empty or the algorithm is invalid.
            parsed_query['algorithm'] = 'tim'
            print(f"DEBUG: Using default algorithm: {parsed_query['algorithm']}")

        # Perform the search in the specified file.
        match_found = search_in_file(file_path, parsed_query, reread_on_query)

        # Send the search result back to the client.
        response = b'STRING EXISTS' if match_found else b'STRING NOT FOUND'
        conn.sendall(response)

        # Log execution time and save metrics.
        exec_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        set_metrics_data(exec_time, parsed_query['algorithm'], ALGORITHMS_LIST, metrics_json_path, reread_on_query)
        
        print(f"DEBUG: Query processed in {exec_time:.2f} ms")

    except json.JSONDecodeError as e:
        # Handle JSON parsing errors.
        print(f"DEBUG: Invalid JSON received from {addr}--{e}")
        # conn.sendall(b'ERROR: Invalid JSON')
    except Exception as e:
        # Handle any other exceptions that occur during processing.
        print(f"DEBUG: Error handling request from {addr}: {e}")
        conn.sendall(b'ERROR: An internal error occurred')
    finally:
        # Ensure the connection is closed after processing.
        conn.close()

def start_server(
    host: str,
    port: int,
    data_file_path: str,
    use_ssl: bool,
    ssl_certfile: Optional[str] = None,
    ssl_keyfile: Optional[str] = None,
    reread_on_query_config_path: Optional[str] = None,
    metrics_json_path: Optional[str] = None,
) -> None:
    """Start a TCP server that listens for incoming connections.

    Args:
        host (str): The hostname to bind to.
        port (int): The port number to listen on.
        data_file_path (str): Path to the file that will be searched.
        use_ssl (bool): Whether to use SSL for secure connections.
        ssl_certfile (Optional[str]): Path to the SSL certificate file.
        ssl_keyfile (Optional[str]): Path to the SSL key file.

    Raises:
        ValueError: If SSL configuration is incomplete.
    """
    try:
        # Set up the TCP socket.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"DEBUG: Server running on {host}:{port}")

        if use_ssl:
            # Load SSL certificates if configured to use SSL.
            if ssl_certfile and ssl_keyfile:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
                server_socket = context.wrap_socket(server_socket, server_side=True)
            else:
                raise ValueError("SSL configuration is incomplete")

        # Load re-read on query configuration.
        reread_on_query = load_reread_on_query_config(reread_on_query_config_path, data_file_path)

        # Main loop to accept client connections.
        while True:
            conn, addr = server_socket.accept()
            print(f"DEBUG: Connection established with {addr}")

            # Start a new thread to handle the client's search query.
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, data_file_path, reread_on_query, metrics_json_path)
            )
            client_thread.start()

    except ValueError as e:
        print(f"DEBUG: ValueError while starting server: {e}")
    except Exception as e:
        print(f"DEBUG: Unexpected error: {e}")
    finally:
        # Ensure the server socket is closed properly.
        if 'server_socket' in locals():
            server_socket.close()
            print("DEBUG: Server socket closed.")

if __name__ == "__main__":
    # Load configuration settings and start the server.
    config_file = get_config_path('config.ini')
    settings = read_config(config_file)
    file_path = settings['file_path']

    # Validate the file path before starting the server.
    if not file_path or not os.path.exists(file_path):
        print(f"DEBUG: File path '{file_path}' not found or does not exist.")
        exit(1)

    # Start the server with specified configurations.
    start_server(
        '0.0.0.0',
        44445,
        file_path,
        use_ssl=settings['use_ssl'],
        ssl_certfile=settings['ssl_certfile'],
        ssl_keyfile=settings['ssl_keyfile'],
        reread_on_query_config_path=settings['reread_on_query_config'],
        metrics_json_path=settings["metrics_json_path"]
    )
