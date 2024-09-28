from server import (
    get_config_path,
    load_algorithms,
    read_config,
    check_algorithm_string,
    search_in_file,
    start_server,
    handle_client
)
import sys
import pytest
import os
import socket
import ssl
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__),
                                 '..')))
# Constants for tests
# Example valid algorithm;
# ensure it exists in your algorithm list
VALID_ALGORITHM = "default"
# Example invalid algorithm for testing purposes
INVALID_ALGORITHM = "invalid_algo"

# Fixture to point to the real test_200k.txt file


@pytest.fixture
def test_200k_file():
    """Fixture to provide the path to the actual test_200k.txt file."""
    test_file_path = os.path.join(os.path.dirname(__file__),
                                  'test_200k.txt')
    # Ensure the test file exists
    assert os.path.exists(test_file_path), f"File not found: {test_file_path}"
    return test_file_path


@pytest.fixture
def config_file(tmp_path, test_200k_file):
    """Fixture to create a temporary config file."""
    config_file_path = tmp_path / 'config.ini'
    config_file_path.write_text(
        f"[default]\n"
        f"linuxpath={test_200k_file}\n"  # Path to the test file
        f"use_ssl=true\n"  # Enable SSL for testing
        f"ssl_certfile=/path/to/certfile\n"  # Mock SSL cert file path
        f"ssl_keyfile=/path/to/keyfile\n"  # Mock SSL key file path
        # Mock PSK key file path
        f"ssl_psk_keyfile=/path/to/pskfile\n"
        # Configuration for rereading on query
        f"reread_on_query_config=true\n"
        # Path for metrics JSON
        f"metrics_json_path=/path/to/metrics.json\n"
        # Path for algorithms list JSON
        f"algorithms_list_json=/path/to/algorithms.json\n"
    )
    return str(config_file_path)


def test_get_config_path():
    """Test whether the configuration file path is constructed correctly."""
    filename = 'config.ini'
    config_path = get_config_path(filename)  # Get the path for the config file
    # Check if it ends with the correct filename
    assert config_path.endswith(filename)
    assert os.path.isabs(config_path)  # Ensure the path is absolute


def test_load_algorithms(test_200k_file, tmp_path):
    """Test loading algorithms from the configuration."""
    config_file = tmp_path / 'config.ini'
    config_file.write_text(
        # Set algorithms list JSON
        f"[Settings]\nalgorithms_list_json=algorithms.json\n"
    )

    # Create a mock algorithms file
    algorithms_file = tmp_path / 'algorithms.json'
    # Write valid algorithms to JSON
    algorithms_file.write_text(json.dumps({"algorithms": [VALID_ALGORITHM]}))
    # Load algorithms from the mock file
    algorithms = load_algorithms()
    # Ensure the valid algorithm is recognized
    assert VALID_ALGORITHM in algorithms
    # Ensure the invalid algorithm is not recognized
    assert INVALID_ALGORITHM not in algorithms


def test_check_algorithm_string():
    """Test if the provided algorithm string
    is recognized as valid or invalid."""
    # Ensure algorithms are loaded for testing
    load_algorithms()  # Ensure this updates the ALGORITHMS_LIST
    assert check_algorithm_string(
        VALID_ALGORITHM) is True  # Check valid algorithm
    assert check_algorithm_string(
        INVALID_ALGORITHM) is False  # Check invalid algorithm


def test_read_config(config_file, test_200k_file):
    """Test the function that reads from the config file
    and returns settings as a dictionary."""
    settings = read_config(config_file)  # Read settings from the config file
    # Check the file path in settings
    assert settings['file_path'] == test_200k_file
    assert settings['use_ssl'] is True  # Verify SSL usage is enabled


def test_search_in_file_found(test_200k_file):
    """Test the search_in_file function
    to check if it finds an existing string."""
    query = {'query_string': '9;0;1;11;0;8;5;0;',
             'algorithm': VALID_ALGORITHM}  # Define the search query
    search_result = search_in_file(test_200k_file, query)  # Perform the search
    # Check if the result matches the expected output
    assert search_result


def test_search_in_file_not_found(test_200k_file):
    """Test the search_in_file function
    to ensure it returns False for a missing string.
    """
    query = {'query_string': 'nonexistent_string',
             'algorithm': VALID_ALGORITHM}  # Define a non-existing query
    result = search_in_file(test_200k_file, query)  # Perform the search
    assert result is False  # Ensure the search result is False
