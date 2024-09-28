from http.client import HTTPException
import os
import socket
import ssl
import json
import time
from dotenv import load_dotenv
import logging
from lib.configuration import read_client_config, get_config_path
from lib.socket_exception import SocketCommunicationError

# Load environment variables from .env file
load_dotenv()

# Configuration parameters from environment variables
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))
PAYLOAD_SIZE = 1024  # Max payload size
SSL_CERTFILE = os.getenv('SSL_CERTFILE')  # Path to SSL certificate file
SSL_KEYFILE = os.getenv('SSL_KEYFILE')    # Path to SSL key file
MAX_RETRIES = 5  # Maximum number of retries for the connection
RETRY_DELAY = 2  # Delay between retries in seconds

# Setup logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load configuration settings and start the server.
script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'client_config.ini')
settings = read_client_config(config_file)

USE_SSL = settings["use_ssl"]

if USE_SSL:
    # Ensure SSL_CERTFILE and SSL_KEYFILE are set if SSL is enabled
    if not SSL_CERTFILE or not SSL_KEYFILE:
        logger.error(
            "DEBUG: SSL is enabled but SSL_CERTFILE or SSL_KEYFILE missing.")
        raise EnvironmentError(
            "Missing SSL certificate or key file in the environment.")
    else:
        # Resolve absolute paths to certificate and key files
        certfile_path = os.path.abspath(SSL_CERTFILE)
        keyfile_path = os.path.abspath(SSL_KEYFILE)

        try:
            context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            context.load_cert_chain(
                certfile=certfile_path,
                keyfile=keyfile_path)
            print("DEBUG: SSL certificates loaded successfully.")
        except FileNotFoundError as fnf_error:
            logger.error(f"DEBUG: SSL certificate file not found: {fnf_error}")
            raise
        except Exception as ssl_setting_error:
            print(
                f"DEBUG: Problem with SSL loading chaine: {ssl_setting_error}")
            print(
                f"DEBUG: certfile: {certfile_path} ,keyfile: {keyfile_path}")


def create_socket():
    """Creates a socket for SSL or non-SSL connection as per configuration."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    if USE_SSL:
        logger.debug("SSL connection enabled.")
        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)

        # Load certificates if they are provided
        if SSL_CERTFILE and SSL_KEYFILE:
            try:
                context.load_cert_chain(
                    certfile=SSL_CERTFILE, keyfile=SSL_KEYFILE)
                logger.debug(
                    f"SSL certificates loaded: {SSL_CERTFILE}, {SSL_KEYFILE}")
            except ssl.SSLError as ssl_error:
                logger.error(f"SSL certificate error: {ssl_error}")
                raise

        # Wrap the socket with SSL
        return context.wrap_socket(sock, server_hostname=SERVER_IP)
    else:
        logger.debug("Non-SSL connection.")
        return sock


def connect_to_server():
    """Attempts to connect to the server with retries and error handling."""

    for attempt in range(1, MAX_RETRIES + 1):
        logger.debug(f"Connecting to server (attempt {attempt})...")
        try:
            sock = create_socket()
            sock.connect((SERVER_IP, SERVER_PORT))
            logger.debug(
                f"Successfully connected to {SERVER_IP}:{SERVER_PORT}")
            return sock

        except ConnectionRefusedError:
            logger.warning(
                f"Attempt {attempt} failed: Connection refused. Retrying...")
            time.sleep(RETRY_DELAY)

        except FileNotFoundError as fnf_error:
            logger.error(f"File not found: {fnf_error}")
            break

        except Exception as e:
            logger.error(f"Error connecting to the server: {e}")
            break

    logger.error("Failed to connect to the server after multiple attempts.")
    return None


def send_request(data: dict) -> dict:
    """
    Send a request to the server and receive a response.

    Args:
        sock (socket.socket): The socket connection to the server.
        data (dict): The request data to send.

    Returns:
        dict: The server's response.
    """
    max_retries = 5  # Maximum number of retries
    for attempt in range(max_retries):
        try:
            # Create a TCP socket
            with socket.socket(socket.AF_INET,
                               socket.SOCK_STREAM) as client_sock:
                # If using SSL, wrap the socket
                if USE_SSL:
                    context = ssl.create_default_context()
                    # Disable hostname checking
                    context.check_hostname = False
                    # Do not verify the certificate
                    context.verify_mode = ssl.CERT_NONE

                    client_sock = context.wrap_socket(
                        client_sock, server_hostname=SERVER_IP)

                # Connect to the TCP server
                client_sock.connect((SERVER_IP, SERVER_PORT))
                print(f"DEBUG: Connected to {SERVER_IP}:{SERVER_PORT}")

                # Prepare the query string

                # Send the search string to the server
                client_sock.sendall(data.encode('utf-8'))
                print(f"DEBUG: Sent: {data}")

                # Receive the response from the server
                response = client_sock.recv(PAYLOAD_SIZE).decode('utf-8')
                print(f"DEBUG: Received from server: {response}")

                return response

        except ConnectionRefusedError:
            print(
                f"DEBUG: connect Attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)  # Wait before retrying
        except FileNotFoundError as fnf_error:
            raise SocketCommunicationError(
                f"File not found error: {fnf_error}")
        except Exception as e:
            raise SocketCommunicationError(
                f"Error connecting to the TCP server: {e}")


def close_connection(sock: socket.socket):
    """Close the socket connection."""
    try:
        sock.close()
        logger.debug("Connection closed successfully.")
    except Exception as e:
        logger.error(f"Error closing connection: {e}")


def main():
    """Main function to handle the client-server communication."""
    try:
        # Send a sample message
        query_string = json.dumps({
            "query_string": "23;0;1;26;0;8;3;0;",
            "algorithm": ''})
        response = send_request(query_string)
        logger.debug(f"Received from server: {response}")

    except Exception as e:
        logger.error(f"Error during communication: {e}")


if __name__ == "__main__":
    main()
