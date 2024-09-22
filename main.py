import json
import os
import time
import socket
import ssl
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()

app = FastAPI()
PAYLOAD_SIZE = 1024  # Max payload size is 1024 bytes

# Get and set Server address and port
SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = int(os.getenv('SERVER_PORT'))  # Convert to integer for socket connection
USE_SSL = os.getenv('USE_SSL', 'false').lower() == 'true'  # Check if SSL should be used
SSL_CERTFILE = os.getenv('SSL_CERTFILE')
SSL_KEYFILE = os.getenv('SSL_KEYFILE')

def send_string_to_server(request: str) -> str:
    """
    Sends a request string to the TCP server and returns the response.

    Args:
        request (str): The query string to send to the server.

    Returns:
        str: The response from the server.

    Raises:
        HTTPException: If unable to connect to the server after retries.
    """
    max_retries = 5  # Maximum number of retries
    for attempt in range(max_retries):
        try:
            # Create a TCP socket
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                # If using SSL, wrap the socket
                if USE_SSL:
                    context = ssl.create_default_context()
                    context.check_hostname = False  # Disable hostname checking
                    context.verify_mode = ssl.CERT_NONE  # Do not verify the certificate

                    client_socket = context.wrap_socket(client_socket, server_hostname=SERVER_IP)
                
                # Connect to the TCP server
                client_socket.connect((SERVER_IP, SERVER_PORT))
                print(f"DEBUG: Connected to {SERVER_IP}:{SERVER_PORT}")

                # Prepare the query string

                query_string =json.dumps({
                    "query_string": request.query_string ,
                    "algorithm": request.alg})

                # Send the search string to the server
                client_socket.sendall(query_string.encode('utf-8'))
                print(f"Sent: {query_string}")

                # Receive the response from the server
                response = client_socket.recv(PAYLOAD_SIZE).decode('utf-8')
                print(f"DEBUG: Received from server: {response}")

                return response

        except ConnectionRefusedError:
            print(f"DEBUG: Attempt {attempt + 1} failed. Connection refused. Retrying...")
            time.sleep(2)  # Wait before retrying
        except FileNotFoundError as fnf_error:
            raise HTTPException(status_code=500, detail=f"File not found error: {fnf_error}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error connecting to the TCP server: {e}")


# Define a model for the request body
class SearchRequest(BaseModel):
    query_string: str
    alg: str

# FastAPI route to handle requests
@app.post("/search/")
async def search_string_in_file(request: SearchRequest) -> dict:
    """
    API to send the search string to the TCP server
    and return the server's response.

    Args:
        request (SearchRequest): The search request containing the query string and algorithm.

    Returns:
        dict: A dictionary containing the query string and the result from the server.
    
    Raises:
        HTTPException: If an error occurs while processing the request.
    """
    print("Received request:", request)
    print(f"Server IP: {SERVER_IP}, Server Port: {SERVER_PORT}")

    # Send the query string to the TCP server
    result = send_string_to_server(request)
    if result is None:
        raise HTTPException(status_code=500, detail="No result returned from the server.")
    
    return {"query_string": request.query_string, "result": result}
