import json
import socket
import threading
import time
import ssl
import configparser
import os
from typing import Optional, Dict, Any
from lib.search_engine import search_alg_setup

PAYLOAD_SIZE = 1024


def load_algorithms() -> list[str]:
    """Load the list of search algorithms from the algorithms list JSON file.

    Returns:
        list[str]: List of algorithms.
    """
    with open('lib/algorithms_list.json', 'r') as file:
        data = json.load(file)
        return data['algorithms']


ALGORITHMS_LIST = load_algorithms()


def get_config_path(filename: str) -> str:
    """Get the full path to the configuration file.

    Args:
        filename (str): Name of the configuration file.

    Returns:
        str: Full path to the configuration file.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)


def read_config(config_file: str) -> Optional[Dict[str, Any]]:
    """Read the configuration file and fetch settings.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        Optional[Dict[str, Any]]: Dictionary containing the configuration settings.
    """
    config = configparser.ConfigParser()
    config.read(config_file)

    settings: Dict[str, Any] = {
        'file_path': None,
        'use_ssl': False,
        'ssl_certfile': None,
        'ssl_keyfile': None,
        'ssl_psk_keyfile': None
    }

    for section in config.sections():
        settings['file_path'] = config.get(section, 'linuxpath', fallback=settings['file_path'])
        settings['use_ssl'] = config.getboolean(section, 'use_ssl', fallback=settings['use_ssl'])
        settings['ssl_certfile'] = config.get(section, 'ssl_certfile', fallback=settings['ssl_certfile'])
        settings['ssl_keyfile'] = config.get(section, 'ssl_keyfile', fallback=settings['ssl_keyfile'])
        settings['ssl_psk_keyfile'] = config.get(section, 'ssl_psk_keyfile', fallback=settings['ssl_psk_keyfile'])

    return settings


def check_algorithm_string(algorithm_string: str) -> bool:
    """Check if the algorithm string is valid.

    Args:
        algorithm_string (str): The algorithm string to check.

    Returns:
        bool: True if the algorithm is valid, False otherwise.
    """
    return algorithm_string in ALGORITHMS_LIST


def search_in_file(file_path: str, search_string: str, reread_on_query: bool = False) -> bool:
    """Search for a string in a specified file.

    Args:
        file_path (str): Path to the file to search.
        search_string (str): The string to search for.
        reread_on_query (bool): Whether to re-read the file for each query.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    formatted_search_string = search_string.split("-@alg!-", 1)
    query_string = formatted_search_string[0].rstrip('\x00')
    algorithm_string = formatted_search_string[1]
    algorithm_is_set = check_algorithm_string(algorithm_string)

    if algorithm_is_set:
        return search_alg_setup(algorithm_string,reread_on_query, file_path, query_string)

    return search_each_time(file_path, search_string) if reread_on_query else search_once_in_memory(file_path, search_string)


def search_each_time(file_path: str, search_string: str) -> bool:
    """Search the file by re-reading it for each query.

    Args:
        file_path (str): Path to the file.
        search_string (str): The string to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    try:
        with open(file_path, 'r') as f:
            for line in f:
                if line.strip() == search_string:
                    return True
    except Exception as e:
        print(f"DEBUG: Error reading file: {e}")
    return False


def search_once_in_memory(file_path: str, search_string: str) -> bool:
    """Load the file once and search in memory.

    Args:
        file_path (str): Path to the file.
        search_string (str): The string to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
        return search_string in (line.strip() for line in lines)
    except Exception as e:
        print(f"DEBUG: Error reading file: {e}")
        return False


def handle_client(conn: socket.socket, addr: tuple, file_path: str, reread_on_query: bool) -> None:
    """Handle client connections and search the string.

    Args:
        conn (socket.socket): The client connection socket.
        addr (tuple): The address of the client.
        file_path (str): Path to the file to search.
        reread_on_query (bool): Whether to re-read the file for each query.
    """
    try:
        start_time = time.time()
        print(f"DEBUG: Connected with {addr}")

        query = conn.recv(PAYLOAD_SIZE).decode('utf-8').rstrip('\x00')
        print(f"DEBUG: Search query received: '{query}'")

        # Perform the search
        match_found = search_in_file(file_path, query, reread_on_query)

        response = b'STRING EXISTS' if match_found else b'STRING NOT FOUND'
        conn.sendall(response)

        # Get the execution time
        exec_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        print(f"DEBUG: Query processed in {exec_time:.2f} ms")
    
    except Exception as e:
        print(f"DEBUG: Error handling request from {addr}: {e}")
    
    finally:
        conn.close()

def start_server(
    host: str,
    port: int,
    file_path: str,
    reread_on_query: bool,
    use_ssl: bool,
    ssl_certfile: Optional[str] = None,
    ssl_keyfile: Optional[str] = None,
) -> None:
    """
    Start a TCP server that listens for incoming connections.

    Args:
        host (str): The hostname to bind to.
        port (int): The port number to listen on.
        file_path (str): Path to the file that will be searched.
        reread_on_query (bool): Should we re-read the file for each query?
        use_ssl (bool): Are we using SSL for secure connections?
        ssl_certfile (Optional[str]): Path to the SSL certificate file. Defaults to None.
        ssl_keyfile (Optional[str]): Path to the SSL key file. Defaults to None.

    Raises:
        ValueError: If SSL configuration is incomplete or any unexpected error occurs.
    """
    try:
        # Set up the TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"DEBUG: Server running on {host}:{port}")

        # If we're using SSL, we need to set it up
        if use_ssl:
            if ssl_certfile and ssl_keyfile:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                print("DEBUG: Loading SSL certificate and key...")
                context.load_cert_chain(certfile=ssl_certfile, keyfile=ssl_keyfile)
                print("DEBUG: SSL certificate and key loaded successfully.")
            else:
                raise ValueError("SSL configuration is incomplete")

            server_socket = context.wrap_socket(server_socket, server_side=True)

        # Now we can listen for client connections
        while True:
            conn, addr = server_socket.accept()
            print(f"DEBUG: Connection established with {addr}")
            # Handle each client in a new thread for responsiveness
            client_thread = threading.Thread(
                target=handle_client,
                args=(conn, addr, file_path, reread_on_query)
            )
            client_thread.start()

    except ValueError as e:
        error_message = f"DEBUG: ValueError while starting server: {e}"
        print(error_message)
        raise ValueError(error_message)  # Raise the ValueError with the detailed message

    except Exception as e:
        error_message = f"DEBUG: Unexpected error while starting server: {e}"
        print(error_message)

    finally:
        # Ensure the server socket is closed
        if 'server_socket' in locals():
            server_socket.close()
            print("DEBUG: Server socket closed.")

if __name__ == "__main__":
    config_file = get_config_path('config.ini')
    settings = read_config(config_file)
    file_path = settings['file_path']
    
    # Validate the file path from config
    if not file_path or not os.path.exists(file_path):
        print(f"DEBUG: File path '{file_path}' not found or does not exist.")
        exit(1)

    # Start the server with SSL settings from the config
    start_server(
        '0.0.0.0',
        44445,
        file_path,
        reread_on_query=True,
        use_ssl=settings['use_ssl'],
        ssl_certfile=settings['ssl_certfile'],
        ssl_keyfile=settings['ssl_keyfile'],
    )
