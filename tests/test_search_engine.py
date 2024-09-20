import os
import pytest
from unittest.mock import patch, mock_open
from lib.search_engine import SearchEngine, search_alg_setup
from lib.binary_search import BinarySearch
from lib.inverted_index_search import InvertedIndexSearch

# Set values that remain constant throughout the test suite
current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "test_200k.txt")
search_term = "'9;0;1;11;0;8;5;0;'"  # Sample search term

# Mock BinarySearch and InvertedIndexSearch classes
@pytest.fixture
def mock_binary_search():
    with patch('lib.search_engine.BinarySearch') as MockBinarySearch:  
        instance = MockBinarySearch.return_value
        instance.search.return_value = (True, 'mock_result')
        yield instance

@pytest.fixture
def mock_inverted_index_search():
    with patch('lib.search_engine.InvertedIndexSearch') as MockInvertedIndexSearch:
        instance = MockInvertedIndexSearch.return_value
        instance.search.return_value = True  
        yield instance

@pytest.fixture
def mock_file_content():
    # Mock reading the content of '200k.txt'
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content

# Test the Binary Search algorithm using the SearchEngine
def test_binary_search(mock_binary_search):
    search_engine = SearchEngine()

    # Call the binary search function
    result = search_engine.binary_search(search_term, file_path)

    print(f"Result: {result}")  # Debugging output
    mock_binary_search.search.assert_called_once_with(search_term)  # Ensure correct call
    assert result == (True, 'mock_result')

# Test the Inverted Index Search algorithm using the SearchEngine
def test_inverted_index_search(mock_inverted_index_search):
    search_engine = SearchEngine()

    # Call the inverted index search function
    result = search_engine.inverted_index_search(search_term, file_path)

    # Ensure the search method is called with the correct arguments
    mock_inverted_index_search.search.assert_called_once_with(search_term)
    assert result == True

# Test the search_alg_setup function with Binary Search
def test_search_alg_setup_binary_search(mock_binary_search):
    algorithm = "binary"
    # Call the function to test
    result = search_alg_setup(algorithm, file_path, search_term)
    
    # Ensure the mock BinarySearch was used
    mock_binary_search.search.assert_called_once_with(search_term)
    assert result == (True, 'mock_result')

# Test the search_alg_setup function with Inverted Index Search
def test_search_alg_setup_inverted_index_search(mock_inverted_index_search):
    algorithm = "inverted_index"

    # Call the function to test
    result = search_alg_setup(algorithm, file_path, search_term)

    # Ensure the mock InvertedIndexSearch was used
    mock_inverted_index_search.search.assert_called_once_with(search_term)
    assert result == True

# Test the InvertedIndexSearch class directly
def test_inverted_index_search_class(mock_file_content):
    # Initialize the search instance class
    search_instance = InvertedIndexSearch(file_path)

    # Test searching for a term
    assert search_instance.search(search_term) is True
    assert search_instance.search("orange") is False

# Test the BinarySearch class directly
def test_binary_search_class(mock_file_content):
    # Mocking the open function to simulate reading from a file
    with patch("builtins.open", mock_open(read_data=mock_file_content)):

        search_instance = BinarySearch(file_path)

        # Test searching for a term that exists
        result = search_instance.search(search_term)
        assert result == (True, search_term)

        # Test searching for a term that does not exist
        result = search_instance.search("orange")
        assert result == (False, None)
