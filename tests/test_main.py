import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, SearchRequest

client = TestClient(app)

@pytest.fixture
def mock_send_string_to_server():
    """Fixture to mock the send_string_to_server function."""
    with patch('main.send_string_to_server') as mock:
        yield mock

def test_search_string_success(mock_send_string_to_server):
    """Test successful search string request."""
    mock_send_string_to_server.return_value = "success response"  # Mocked response from server
    request_data = {"query_string": "test query", "alg": "mock_algorithm"}  # Request data for the API call

    response = client.post("/search/", json=request_data)  # Make the API call

    assert response.status_code == 200  # Check for successful response
    assert response.json() == {"query_string": "test query", "result": "success response"}  # Validate response content

def test_search_string_empty_request():
    """Test handling of empty request body."""
    
    # Act: Make a POST request with an empty JSON body
    response = client.post("/search/", json={})  # Send empty JSON
    
    # Assert: Check that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422  # Validate error response status
    
    # Assert: Verify the detail in the response matches the expected error structure
    assert response.json() == {
        'detail': [
            {
                'type': 'missing',
                'loc': ['body', 'query_string'],
                'msg': 'Field required',
                'input': {}
            },
            {
                'type': 'missing',
                'loc': ['body', 'alg'],
                'msg': 'Field required',
                'input': {}
            }
        ]
    }

def test_search_string_invalid_request():
    """Test handling of invalid request body."""
    
    # Act: Make a POST request with a missing 'alg' field
    response = client.post("/search/", json={"query_string": "test query"})  # Send request missing 'alg'
    
    # Debug: Print the response JSON for inspection
    print(response.json())  # Print response for debugging purposes
    
    # Assert: Check that the response status code is 422 (Unprocessable Entity)
    assert response.status_code == 422  # Validate error response status
    
    # Assert: Verify the detail in the response matches the expected error structure
    assert response.json() == {
        'detail': [
            {
                'type': 'missing',
                'loc': ['body', 'alg'],
                'msg': 'Field required',
                'input': {'query_string': 'test query'}
            }
        ]
    }
