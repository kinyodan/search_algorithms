import os
import pytest
from unittest.mock import patch, mock_open
from lib.algorithms.binary_search import BinarySearch
from lib.algorithms.inverted_index_search import InvertedIndexSearch
from lib.search_engine import SearchEngine, search_alg_setup

# Constants for file paths and search terms
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))  # Current directory of the test file
FILE_PATH = os.path.join(CURRENT_DIR, "test_200k.txt")  # Path to the test file
SEARCH_TERM = "10;0;1;26;0;8;3;0;"  # Valid search term for testing
NON_EXISTENT_TERM = "orange"  # Search term that does not exist in the file

@pytest.fixture
def mock_binary_search():
    # Mock the BinarySearch class for testing
    with patch('lib.search_engine.BinarySearch') as MockBinarySearch:
        instance = MockBinarySearch.return_value
        instance.search.return_value = (True, 'mock_result')  # Mock search result
        yield instance

@pytest.fixture
def mock_inverted_index_search():
    # Mock the InvertedIndexSearch class for testing
    with patch('lib.search_engine.InvertedIndexSearch') as MockInvertedIndexSearch:
        instance = MockInvertedIndexSearch.return_value
        instance.search.return_value = True  # Mock search result
        yield instance

@pytest.fixture
def mock_file_content():
    # Mock reading the content of '200k.txt' for testing
    with open(FILE_PATH, 'r') as file:
        file_content = file.read()  # Read file content
    return file_content

@pytest.fixture
def search_engine():
    # Create a SearchEngine instance for testing with reread_on_query set to 'False'
    return SearchEngine(reread_on_query='False', file_path=FILE_PATH)

@pytest.fixture
def search_engine_reread_on_query_true():
    # Create a SearchEngine instance for testing with reread_on_query set to True
    return SearchEngine(reread_on_query=True, file_path=FILE_PATH)

def test_binary_search(search_engine, mock_binary_search):
    # Test binary search method in SearchEngine
    result = search_engine.binary_search(SEARCH_TERM)
    mock_binary_search.search.assert_called_once_with(SEARCH_TERM)  # Ensure the search method was called
    assert result == (True, 'mock_result')  # Assert the expected result

def test_inverted_index_search(search_engine, mock_inverted_index_search):
    # Test inverted index search method in SearchEngine
    result = search_engine.inverted_index_search(SEARCH_TERM)
    mock_inverted_index_search.search.assert_called_once_with(SEARCH_TERM)  # Ensure the search method was called
    assert result is True  # Assert the expected result

def test_search_alg_setup_binary_search(mock_binary_search):
    # Test the setup for binary search algorithm
    result = search_alg_setup("binary", 'False', FILE_PATH, SEARCH_TERM)
    mock_binary_search.search.assert_called_once_with(SEARCH_TERM)  # Ensure the search method was called
    assert result == (True, 'mock_result')  # Assert the expected result

def test_search_alg_setup_inverted_index_search(mock_inverted_index_search):
    # Test the setup for inverted index search algorithm
    result = search_alg_setup("inverted_index", 'False', FILE_PATH, SEARCH_TERM)
    mock_inverted_index_search.search.assert_called_once_with(SEARCH_TERM)  # Ensure the search method was called
    assert result is True  # Assert the expected result

def test_inverted_index_search_class(mock_file_content):
    # Test the InvertedIndexSearch class directly
    search_instance = InvertedIndexSearch(FILE_PATH, mock_file_content)
    assert search_instance.search(SEARCH_TERM) is True  # Assert search term found
    assert search_instance.search(NON_EXISTENT_TERM) is False  # Assert non-exis
