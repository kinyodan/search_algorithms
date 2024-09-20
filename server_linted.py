import socket
import threading
import time
import ssl
import configparser
import os
from typing import Optional

# Utility function to get the path to the configuration file
def get_config_path(filename: str):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(script_dir, filename)

# Function to read the configuration file and fetch the file path
def read_config(config_file: str) -> Optional[str]:
    config = configparser.ConfigParser()
    config.read(config_file)
    
    # Look for the 'linuxpath' in the config file
    for section in config.sections():
        linuxpath = config.get(section, 'linuxpath', fallback=None)
        if linuxpath:
            return linuxpath
    
    return None

# Search the file based on the REREAD_ON_QUERY 
def search_in_file(file_path: str, search_string: str, reread_on_query: bool = False):
    if reread_on_query:
        return search_each_time(file_path, search_string)
    else:
        return search_once_in_memory(file_path, search_string)

# Search the file by re-reading it every time a query is made
def search_each_time(file_path: str, search_string: str):
    try:
        with open(file_path, 'r') as f:
            for line in f:
                print(line)
                if line.strip() == search_string:
                    return True
    except Exception as e:
        print(f"DEBUG: Error reading file: {e}")
    
    return False

# Load the file once and search in memory
def search_once_in_memory(file_path: str, search_string: str):
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            print(lines)
        return search_string in (line.strip() for line in lines)
    except Exception as e:
        print(f"DEBUG: Error reading file: {e}")
        return False

# client connections, search the string, and respond
def handle_client(conn: socket.socket, addr, file_path: str, reread_on_query: bool):
    try:
        start_time = time.time()
        print(f"DEBUG: Connected with {addr}")

        query = conn.recv(1024).decode('utf-8').rstrip('\x00')
        print(f"DEBUG: Search query received: '{query}'")

        # Perform the search
        match_found = search_in_file(file_path, query, reread_on_query)

        if match_found:
            conn.sendall(b'STRING EXISTS')
        else:
            conn.sendall(b'STRING NOT FOUND')

        # get the execution time
        exec_time = (time.time() - start_time) * 1000  ## Convert to milliseconds
        print(f"DEBUG: Query processed in {exec_time:.2f} ms")
    
    except Exception as e:
        print(f"DEBUG: Error handling request from {addr}: {e}")
    
    finally:
        conn.close()

# Function to initialize and start the TCP server
def start_server(host: str, port: int, file_path: str, reread_on_query: bool):
    try:
        # Set up the TCP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen()
        print(f"DEBUG: Server running on {host}:{port}")

        # Listen for client connections
        while True:
            conn, addr = server_socket.accept()
            # Use threading to handle multiple client connections
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, file_path, reread_on_query))
            client_thread.start()
    
    except Exception as e:
        print(f"DEBUG: Error starting server: {e}")
    finally:
        server_socket.close()

# Main entry point
if __name__ == "__main__":
    config_file = get_config_path('config.ini')
    file_path = read_config(config_file)
    
    # Validate the file path from config
    if not file_path or not os.path.exists(file_path):
        print(f"DEBUG: File path '{file_path}' not found or does not exist.")
        exit(1)

    # Start the server
    start_server('0.0.0.0', 44445, file_path, reread_on_query=True)
