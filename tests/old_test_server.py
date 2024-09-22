import pytest
import os
from server import get_config_path, read_config, search_each_time, search_once_in_memory, check_algorithm_string

@pytest.fixture
def sample_file(tmp_path):
    """Creates a temporary test file with sample data."""
    file = tmp_path / "test_file.txt"
    file.write_text("apple\nbanana\ncherry\n")
    return str(file)

def test_get_config_path():
    """Test whether the configuration file path is constructed correctly."""
    filename = 'config.ini'
    config_path = get_config_path(filename)
    
    # Assert that the filename is appended at the end of the path and the path is absolute
    assert config_path.endswith(filename)
    assert os.path.isabs(config_path)

def test_read_config(sample_file, tmp_path):
    """Test the function that reads from the config file."""
    config_file = tmp_path / 'config.ini'
    
    # Simulate a configuration file with a sample linuxpath entry
    config_file.write_text(f"[default]\nlinuxpath={sample_file}\n")
    
    # Test if the linuxpath from the config file matches the provided sample file path
    file_path = read_config(str(config_file))
    assert file_path == sample_file

def test_read_config_missing_key(tmp_path):
    """Test the behavior when the config file is missing the linuxpath key."""
    config_file = tmp_path / 'config.ini'
    config_file.write_text("[default]\ninvalidkey=/not/real/path\n")
    
    # Test if the function returns None when the expected key is not found
    file_path = read_config(str(config_file))
    assert file_path is None

def test_search_each_time_found(sample_file):
    """Test the search_each_time function to check if it finds an existing string."""
    # Searching for 'banana', which exists in the sample file
    result = search_each_time(sample_file, 'banana')
    assert result is True

def test_search_each_time_not_found(sample_file):
    """Test the search_each_time function to ensure it returns False for a missing string."""
    # Searching for 'grape', which is not in the file
    result = search_each_time(sample_file, 'grape')
    assert result is False

def test_search_once_in_memory_found(sample_file):
    """Test search_once_in_memory for finding a string stored in memory."""
    # Searching for 'cherry', which exists in the file
    result = search_once_in_memory(sample_file, 'cherry')
    assert result is True

def test_search_once_in_memory_not_found(sample_file):
    """Test search_once_in_memory to verify it returns False for a string not present in memory."""
    # Searching for 'grape', which doesn't exist
    result = search_once_in_memory(sample_file, 'grape')
    assert result is False

def test_check_algorithm_string():
    """Test if the provided algorithm string is recognized as valid or invalid."""
    # 'binary' should be a valid algorithm
    valid_algorithm = "binary"
    # 'invalid_algo' should be flagged as invalid
    invalid_algorithm = "invalid_algo"
    
    # Ensure valid algorithm passes and invalid one fails
    assert check_algorithm_string(valid_algorithm) is True
    assert check_algorithm_string(invalid_algorithm) is False
