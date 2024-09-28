import pytest
import socket
import ssl
import json
from unittest.mock import patch, MagicMock
from client import (
    create_socket,
    connect_to_server,
    send_request,
    close_connection,
    USE_SSL,
    SERVER_IP,
    SERVER_PORT
)
from lib.socket_exception import SocketCommunicationError

# Mock environment variables for SSL certificates
SSL_CERTFILE = "path/to/certfile"
SSL_KEYFILE = "path/to/keyfile"


@patch("client.ssl.create_default_context")
@patch("client.socket.socket")
def test_create_socket_non_ssl(mock_socket, mock_ssl_context):
    # Test non-SSL socket creation
    with patch("client.USE_SSL", False):
        sock = create_socket()
        assert mock_socket.called
        assert not mock_ssl_context.called


@patch("client.ssl.create_default_context")
@patch("client.socket.socket")
def test_create_socket_ssl(mock_socket, mock_ssl_context):
    # Test SSL socket creation
    with patch("client.USE_SSL", True):
        mock_ssl_context_instance = mock_ssl_context.return_value
        mock_ssl_context_instance.wrap_socket.return_value = (
            mock_socket.return_value
        )

        sock = create_socket()
        assert mock_socket.called
        assert mock_ssl_context.called
        assert mock_ssl_context_instance.wrap_socket.called


@patch("client.create_socket")
@patch("client.time.sleep", return_value=None)  # Prevent delay during test
def test_connect_to_server_success(mock_sleep, mock_create_socket):
    # Mock a successful connection
    mock_socket_instance = MagicMock()
    mock_create_socket.return_value = mock_socket_instance

    sock = connect_to_server()
    assert mock_create_socket.called
    assert mock_socket_instance.connect.called
    assert sock == mock_socket_instance


@patch("client.create_socket")
@patch("client.time.sleep", return_value=None)  # Prevent delay during test
def test_connect_to_server_failure(mock_sleep, mock_create_socket):
    # Mock a connection failure (ConnectionRefusedError)
    mock_socket_instance = MagicMock()
    mock_socket_instance.connect.side_effect = ConnectionRefusedError
    mock_create_socket.return_value = mock_socket_instance

    sock = connect_to_server()
    assert mock_create_socket.called
    assert sock is None


@patch("client.socket.socket")
@patch("client.ssl.create_default_context")
def test_send_request_success(mock_ssl_context, mock_socket):
    # Mock the SSL context wrapping (if needed)
    mock_ssl_context_instance = mock_ssl_context.return_value
    mock_ssl_context_instance.wrap_socket.return_value = (
         mock_socket.return_value
    )

    # Mock the socket instance and its methods
    mock_socket_instance = MagicMock()
    mock_socket.return_value.__enter__.return_value = mock_socket_instance
    mock_socket_instance.recv.return_value = "success".encode('utf-8')

    # Prepare the request data as a dictionary
    data = json.dumps({"query_string": "23;0;1;26;0;8;3;0;", "algorithm": ""})

    # Call the send_request function with SSL disabled
    with patch("client.USE_SSL", False):
        response = send_request(data)

    # Assertions
    assert mock_socket.called
    assert mock_socket_instance.connect.called
    assert mock_socket_instance.sendall.called
    assert response == "success"


@patch("client.socket.socket")
@patch("client.ssl.create_default_context")
def test_send_request_failure(mock_ssl_context, mock_socket):
    # Mock a request failure (ConnectionRefusedError)
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.connect.side_effect = ConnectionRefusedError

    data = {"query_string": "23;0;1;26;0;8;3;0;", "algorithm": ""}
    with patch("client.USE_SSL", False):
        with pytest.raises(SocketCommunicationError):
            send_request(data)


@patch("client.socket.socket")
def test_close_connection_success(mock_socket):
    # Mock successful socket closing
    mock_socket_instance = mock_socket.return_value

    close_connection(mock_socket_instance)
    mock_socket_instance.close.assert_called_once()


@patch("client.socket.socket")
def test_close_connection_failure(mock_socket):
    # Mock a failure when closing the socket
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.close.side_effect = Exception("Close error")

    close_connection(mock_socket_instance)
    mock_socket_instance.close.assert_called_once()


if __name__ == "__main__":
    pytest.main()
