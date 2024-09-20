import pytest
import os
import socket
import ssl
from server import (
    get_config_path,
    read_config,
    search_each_time,
    search_once_in_memory,
    check_algorithm_string,
    start_server,
    handle_client
)

# Fixture to point to the real test_200k.txt file
@pytest.fixture
def test_200k_file():
    """Fixture to provide the path to the actual test_200k.txt file."""
    # Get the directory of the current test file and resolve the path to test_200k.txt
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_200k.txt')

    # Ensure the file exists before returning the path
    assert os.path.exists(test_file_path), f"File not found: {test_file_path}"
    
    return test_file_path

@pytest.fixture
def config_file(tmp_path):
    """Fixture to create a temporary config file."""
    config_file_path = tmp_path / 'config.ini'
    config_file_path.write_text(
        f"[Settings]\nlinuxpath={test_200k_file}\nuse_ssl=true\nssl_certfile=server.cert\nssl_keyfile=server.key\n"
    )
    return str(config_file_path)

@pytest.fixture
def config_path_in_tests():
    """Fixture to provide the path to the config file inside the tests folder."""
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    return config_file_path

def test_get_config_path():
    """Test whether the configuration file path is constructed correctly."""
    filename = 'config.ini'
    config_path = get_config_path(filename)
    assert config_path.endswith(filename)
    assert os.path.isabs(config_path)

def test_read_config(test_200k_file, tmp_path):
    """Test the function that reads from the config file and returns settings as a dictionary."""
    config_file = tmp_path / 'config.ini'
    
    # Write a sample configuration file
    config_file.write_text(
        f"""
        [default]
        linuxpath={test_200k_file}
        use_ssl=true
        ssl_certfile=/path/to/certfile
        ssl_keyfile=/path/to/keyfile
        ssl_psk_keyfile=/path/to/psk_keyfile
        """
    )
    
    # Call the updated read_config function
    settings = read_config(str(config_file))
    
    # Assert that the settings dictionary is correctly populated
    assert settings['file_path'] == test_200k_file
    assert settings['use_ssl'] is True
    assert settings['ssl_certfile'] == '/path/to/certfile'
    assert settings['ssl_keyfile'] == '/path/to/keyfile'
    assert settings['ssl_psk_keyfile'] == '/path/to/psk_keyfile'


def test_read_config_missing_key(tmp_path):
    """Test the behavior when the config file is missing the linuxpath key."""
    config_file = tmp_path / 'config.ini'
    config_file.write_text("[default]\ninvalidkey=/not/real/path\n")

    # Call the updated read_config function
    settings = read_config(str(config_file))
    
    # Assert that 'file_path' is None and other settings have their default values
    assert settings['file_path'] is None
    assert settings['use_ssl'] is False
    assert settings['ssl_certfile'] is None
    assert settings['ssl_keyfile'] is None
    assert settings['ssl_psk_keyfile'] is None


def test_search_each_time_found(test_200k_file):
    """Test the search_each_time function to check if it finds an existing string."""
    # Assuming '3;0;1;28;0;7;5;0;' exists in the test_200k.txt file
    result = search_each_time(test_200k_file, '9;0;1;11;0;8;5;0;')
    assert result is True

def test_search_each_time_not_found(test_200k_file):
    """Test the search_each_time function to ensure it returns False for a missing string."""
    # Searching for a string that doesn't exist in test_200k.txt
    result = search_each_time(test_200k_file, 'nonexistent_string')
    assert result is False

def test_search_once_in_memory_found(test_200k_file):
    """Test search_once_in_memory for finding a string stored in memory."""
    result = search_once_in_memory(test_200k_file, '9;0;1;11;0;8;5;0;')
    assert result is True

def test_search_once_in_memory_not_found(test_200k_file):
    """Test search_once_in_memory to verify it returns False for a string not present in memory."""
    result = search_once_in_memory(test_200k_file, 'nonexistent_string')
    assert result is False

def test_check_algorithm_string():
    """Test if the provided algorithm string is recognized as valid or invalid."""
    valid_algorithm = "binary"
    invalid_algorithm = "invalid_algo"
    assert check_algorithm_string(valid_algorithm) is True
    assert check_algorithm_string(invalid_algorithm) is False

def test_ssl_config_error(tmp_path, test_200k_file):
    """Test server startup with missing SSL files."""

    # Create a temporary configuration file
    config_file = tmp_path / 'config.ini'

    # Write a sample configuration file
    config_content = f"""
    [default]
    linuxpath={test_200k_file}
    use_ssl=true
    ssl_certfile=/path/to/certfile
    ssl_keyfile=/path/to/keyfile
    ssl_psk_keyfile=/path/to/psk_keyfile
    """
    
    # Write the content to the config file
    config_file.write_text(config_content.strip())

    # Ensure the config file exists at the specified location
    assert config_file.exists(), f"Config file not found at {config_file}"

    # Simulate missing SSL certificate and keyfile
    with pytest.raises(ValueError, match="SSL configuration is incomplete"):
        start_server(
            '0.0.0.0', 
            44445, 
            test_200k_file,  # Use the config file_linuxpath value from the temporary file
            reread_on_query=True, 
            use_ssl=True, 
            ssl_certfile=None, 
            ssl_keyfile=None
        )

def test_handle_client_execution_time(mocker, test_200k_file):
    """Test execution time for a small file."""
    mock_conn = mocker.Mock()
    mock_conn.recv.return_value = b'3;0;1;28;0;7;5;0;'
    mocker.patch('server.time.time', side_effect=[0, 0.5])  # Simulate 500 ms execution
    mocker.patch('server.search_each_time', return_value=True)
    handle_client(mock_conn, ('127.0.0.1', 5000), test_200k_file, reread_on_query=True)
    mock_conn.sendall.assert_called_with(b'STRING EXISTS')

@pytest.mark.parametrize('file_size, expected_time', [(10000, 0.5), (100000, 1.0), (1000000, 3.0)])
def test_execution_time_for_different_file_sizes(mocker, file_size, expected_time, test_200k_file):
    """Test how execution time varies with different file sizes."""
    mock_conn = mocker.Mock()
    mock_conn.recv.return_value = b'3;0;1;28;0;7;5;0;'
    mocker.patch('server.time.time', side_effect=[0, expected_time])
    mocker.patch('server.search_each_time', return_value=True)
    handle_client(mock_conn, ('127.0.0.1', 5000), test_200k_file, reread_on_query=True)
    mock_conn.sendall.assert_called_with(b'STRING EXISTS')
