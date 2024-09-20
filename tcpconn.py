import socket

server_ip = "135.181.96.160"
server_port = 44445

try:
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((server_ip, server_port))

    message = "Hello, Server!"
    client_socket.send(message.encode())

    response = client_socket.recv(1024)
    print("Response from server:", response.decode())

except Exception as e:
    print(f"Error occurred: {e}")

finally:
    client_socket.close()
