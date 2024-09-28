import json
import socket
import threading
import time
import ssl
import os
import mmap
from typing import List, Optional, Dict
from lib.preload_data import DataPreloader
from lib.search_engine import SearchEngine, search_alg_setup
from lib.configuration import load_reread_on_query_config, read_config
from metrics.metrics import set_metrics_data
import pyinotify
from lib.event_handler import EventHandler
from lib.optimized_file_reader import FileReader
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# The size of the payload buffer for receiving search queries from clients.
PAYLOAD_SIZE = 4096
shared_file_content = ""  # This will hold the content of the watched file


def monitor_file(file_path: str):
    """Monitor the specified file for modifications
    and reload content when changes occur.

    Args:
        file_path (str): The path to the file to be monitored.
    """
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)
    wm.add_watch(file_path, pyinotify.ALL_EVENTS)

    logging.debug("DEBUG: Starting to monitor file...")
    notifier.loop()


def get_config_path(filename: str) -> str:
    """Retrieve the absolute path of the given configuration file.

    Args:
        filename (str): The name of the configuration file.

    Returns:
        str: The full absolute path to the configuration file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)


def load_algorithms() -> List[str]:
    """Load and return the list of search algorithms
    from the JSON configuration.

    Returns:
        List[str]: A list of available algorithms for searching.
    """
    settings_config_file = get_config_path('config.ini')
    algorithms_list_settings = read_config(settings_config_file)
    try:
        with open(algorithms_list_settings['algorithms_list'], 'r') as file:
            data = json.load(file)
            return data['algorithms']
    except FileNotFoundError as e:
        logging.error(f"DEBUG: Configuration file not found: {e}")
    except json.JSONDecodeError as e:
        logging.error(f"DEBUG: Error decoding JSON: {e}")


# Load the list of algorithms at startup.
ALGORITHMS_LIST: List[str] = load_algorithms()


def check_algorithm_string(algorithm_string: str) -> bool:
    """Check if the provided algorithm string
    is valid based on the loaded algorithms.

    Args:
        algorithm_string (str): The name of the search algorithm.

    Returns:
        bool: True if the algorithm is valid, False otherwise.
    """
    return algorithm_string in ALGORITHMS_LIST


def search_in_file(file_path: str,
                   query: Dict[str, str],
                   reread_on_query: bool = False) -> bool:
    """Search for a query string in the specified file
    using the provided algorithm.

    Args:
        file_path (str): The file path to search in.
        query (Dict[str, str]): A dictionary containing
        'query_string' and 'algorithm'.
        reread_on_query (bool): Whether the file should
        be re-read before each query.

    Returns:
        bool: True if the query string is found, False otherwise.
    """

    query_string: str = query['query_string']
    algorithm_string: str = query['algorithm']

    if check_algorithm_string(algorithm_string):
        return search_alg_setup(
            algorithm_string,
            reread_on_query,
            file_path,
            query_string,
            shared_file_content)

    logging.debug(f"DEBUG: Invalid algorithm: {algorithm_string}")
    return False


def handle_client(
        conn: socket.socket,
        addr: tuple,
        file_path: str,
        reread_on_query: bool,
        metrics_json_path: str,
        shared_file_content: str) -> None:
    """Handle incoming client requests for search operations.

    Args:
        conn (socket.socket): The client connection socket.
        addr (tuple): The address of the client.
        file_path (str): The path to the file for search.
        reread_on_query (bool): If true, the file is re-read for each query.
        metrics_json_path (str): The path to the JSON file to record metrics.
    """
    start_time = time.time()
    logging.debug(f"Connected with {addr}")

    try:
        # Receive the search query from the client.
        query = conn.recv(PAYLOAD_SIZE).decode('utf-8').rstrip('\x00')
        logging.debug(f"Search query received: '{query}'")

        # Parse the received query from JSON format.
        parsed_query = json.loads(query)

        # Check if the search string is empty or the algorithm is invalid.
        if not parsed_query.get('query_string') or parsed_query.get(
                'algorithm') not in ALGORITHMS_LIST:
            parsed_query['algorithm'] = 'default'
            logging.debug(
                f"Using default algorithm. REREAD_ON_QUERY: {reread_on_query}")
        else:
            logging.debug(
                f"Using Custom algorithm. REREAD_ON_QUERY: {reread_on_query}")

        # Perform the search in the shared file content.
        match_found = search_in_file(file_path, parsed_query, reread_on_query)

        # Send the search result back to the client.
        response = b'STRING EXISTS' if match_found else b'STRING NOT FOUND'
        conn.sendall(response)

        # Log execution time and save metrics.
        exec_time = (time.time() - start_time) * 1000
        set_metrics_data(
            exec_time,
            parsed_query['algorithm'],
            ALGORITHMS_LIST,
            metrics_json_path,
            reread_on_query)
        logging.debug(f"Query processed in {exec_time:.2f} ms")

    except json.JSONDecodeError as e:
        logging.error(f"Failed to parse query: {e}")
    except Exception as e:
        logging.error(f"Error handling client: {e}")
    finally:
        conn.close()


def start_server(
        host: str,
        port: int,
        data_file_path: str,
        use_ssl: bool,
        ssl_certfile: Optional[str] = None,
        ssl_keyfile: Optional[str] = None,
        reread_on_query_config_path: Optional[str] = None,
        metrics_json_path: Optional[str] = None) -> None:
    """Start the TCP server that listens for search queries.

    Args:
        host (str): Host IP address.
        port (int): Port number to listen on.
        data_file_path (str): The file path used for search operations.
        use_ssl (bool): Whether to use SSL for secure connections.
        ssl_certfile (Optional[str]): Path to the SSL certificate file.
        ssl_keyfile (Optional[str]): Path to the SSL key file.
        reread_on_query_config_path (Optional[str]): Path to the
        configuration file for re-reading settings.
        metrics_json_path (Optional[str]): Path to the JSON file
        for saving metrics.
    """
    try:
        # Set up the TCP socket.
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        logging.debug(f"DEBUG: Server running on {host}:{port}")

        if use_ssl:
            if ssl_certfile and ssl_keyfile:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                context.load_cert_chain(
                    certfile=ssl_certfile, keyfile=ssl_keyfile)
                server_socket = context.wrap_socket(
                    server_socket, server_side=True)
            else:
                raise ValueError("SSL configuration is incomplete")

        # Load re-read on query configuration.
        reread_on_query = load_reread_on_query_config(
            reread_on_query_config_path, data_file_path)

        # Preload file data from the source file
        # in this case 200k.txt at start up and
        # passing it to handle_client() since
        # event handlers will check for any file changes,
        # and read file data again, data is loading to
        # FileServer class object that is accessible in
        # all FileServer instances.
        file_preloader = DataPreloader()
        shared_file_content = file_preloader.preload_file_data(data_file_path)

        # Start file monitoring in a separate thread.
        monitor_thread = threading.Thread(
            target=monitor_file, args=(
                data_file_path,))
        # Ensure thread exits when the main program exits
        monitor_thread.daemon = True
        monitor_thread.start()

        # Main loop to accept client connections.
        while True:
            conn, addr = server_socket.accept()
            logging.debug(f"DEBUG: Connection established with {addr}")

            # Start a new thread to handle the client's search query.
            client_thread = threading.Thread(
                target=handle_client,
                args=(
                    conn,
                    addr,
                    data_file_path,
                    reread_on_query,
                    metrics_json_path,
                    shared_file_content))
            client_thread.start()

    except ValueError as e:
        logging.debug(f"DEBUG: ValueError while starting server: {e}")
    except Exception as e:
        logging.debug(f"DEBUG: Unexpected error: {e}")
    finally:
        if 'server_socket' in locals():
            server_socket.close()
            logging.debug("DEBUG: Server socket closed.")


if __name__ == "__main__":
    config_file = get_config_path('config.ini')
    settings = read_config(config_file)
    file_path = settings['file_path']

    if not file_path or not os.path.exists(file_path):
        logging.debug(
            f"DEBUG: File path '{file_path}' not found or does not exist.")
        exit(1)

    start_server(
        '0.0.0.0',
        44445,
        file_path,
        use_ssl=settings['use_ssl'],
        ssl_certfile=settings['ssl_certfile'],
        ssl_keyfile=settings['ssl_keyfile'],
        reread_on_query_config_path=settings['reread_on_query_config'],
        metrics_json_path=settings["metrics_path"]
    )
