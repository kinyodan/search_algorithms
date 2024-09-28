import json
import os
import sys
import pytest
import socket
import ssl
from unittest import mock

from lib.configuration import read_client_config
from client import (
    SERVER_IP, create_socket, connect_to_server, send_request,
    close_connection
)

# Modify sys.path after imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
)

script_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(script_dir, 'client_config.ini')
settings = read_client_config(config_file)

# Mocking the environment variables


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch):
    monkeypatch.setenv('SERVER_IP', '127.0.0.1')
    monkeypatch.setenv('SERVER_PORT', '8080')
    monkeypatch.setenv('SSL_CERTFILE', settings['ssl_certfile'])
    monkeypatch.setenv('SSL_KEYFILE', settings['ssl_keyfile'])


# Mocking the SSL Context and Socket
@pytest.fixture
def mock_ssl_context():
    with mock.patch('ssl.create_default_context') as mock_context:
        yield mock_context


@pytest.fixture
def mock_socket():
    with mock.patch('socket.socket') as mock_sock:
        yield mock_sock


# Test create_socket without SSL
def test_create_socket_non_ssl(mock_socket):
    # Mock the configuration to not use SSL
    mock_socket_instance = mock_socket.return_value
    USE_SSL = False

    sock = create_socket()

    assert sock == mock_socket_instance
    mock_socket.assert_called_once_with(socket.AF_INET, socket.SOCK_STREAM)


# Test connect_to_server success case
def test_connect_to_server_success(mock_socket):
    # Mock the socket to simulate a successful connection
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.connect.return_value = True

    sock = connect_to_server()

    assert sock == mock_socket_instance


# Test connect_to_server connection retries
def test_connect_to_server_retry(mock_socket):
    # Mock socket to raise connection refused on first attempts
    mock_socket_instance = mock_socket.return_value
    mock_socket_instance.connect.side_effect = [ConnectionRefusedError, True]

    sock = connect_to_server()

    assert sock == mock_socket_instance
    assert mock_socket_instance.connect.call_count == 2


# Test send_request success case
def test_send_request_success():
    # Mock the socket instance returned by the context manager
    mock_sock_instance = mock.MagicMock()
    mock_sock_instance.recv.return_value = b'DEBUG: Connected to 0.0.0.0:44445'

    # Patch the socket object, specifically the context manager behavior
    with mock.patch('socket.socket') as mock_sock:
        # Make the mock return the mock_socket_instance when entering the
        # context
        mock_sock.return_value.__enter__.return_value = mock_sock_instance

        # Call the function to test
        response = send_request(json.dumps(
            {"query": "test_query", "algorithm": "test_algorithm"}))

        # Assert the expected response
        assert response == 'DEBUG: Connected to 0.0.0.0:44445'

# Test close_connection success case


def test_close_connection_success(mock_socket):
    mock_socket_instance = mock_socket.return_value
    close_connection(mock_socket_instance)

    mock_socket_instance.close.assert_called_once()
