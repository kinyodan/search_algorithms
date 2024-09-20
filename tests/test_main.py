import os
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app, SearchRequest

# Setting up environment variables for testing. This helps the app know where to find the server.
os.environ['SERVER_IP'] = '127.0.0.1'
os.environ['SERVER_PORT'] = '8000'

# Create a TestClient instance to interact with the FastAPI app
client = TestClient(app)

# This fixture mocks the send_string_to_server function for our tests.
@pytest.fixture
def mock_send_string_to_server():
    with patch('main.send_string_to_server') as mock:
        yield mock

def test_search_string_success(mock_send_string_to_server):
    """Test that a successful search returns the expected response."""
    # Arrange: Set up the mock response
    mock_send_string_to_server.return_value = "Mock server response"
    request_data = {"query_string": "test query", "alg": "mock_algorithm"}

    # Act: Make a POST request to the /search/ endpoint
    response = client.post("/search/", json=request_data)

    # Assert: Check the response status and content
    assert response.status_code == 200
    assert response.json() == {
        "query_string": "test query",
        "result": "Mock server response"
    }
    # Verify that our mock function was called with the correct arguments
    mock_send_string_to_server.assert_called_once_with(SearchRequest(**request_data))

def test_search_string_connection_error(mock_send_string_to_server):
    """Test how the API handles a connection error."""
    # Arrange: Simulate a ConnectionError from the mock
    mock_send_string_to_server.side_effect = ConnectionError("Connection failed")
    request_data = {"query_string": "test query", "alg": "mock_algorithm"}

    # Act: Make a POST request
    response = client.post("/search/", json=request_data)

    # Assert: Check that a 500 error is returned with the expected message
    assert response.status_code == 500
    print(response.json)
    assert response.json() == {"ConnectionError: Connection failed"}

def test_search_string_invalid_request():
    """Test the API's response to an invalid request."""
    # Arrange: Omit the 'alg' field in the request
    request_data = {"query_string": "test query"}

    # Act: Make a POST request
    response = client.post("/search/", json=request_data)

    # Assert: Check for a validation error (422 Unprocessable Entity)
    assert response.status_code == 422
    assert "alg" in response.json()["detail"][0]["loc"]

def test_search_string_server_error(mock_send_string_to_server):
    """Test how the API responds to a generic server error."""
    # Arrange: Simulate a generic Exception from the mock
    mock_send_string_to_server.side_effect = Exception("Server error")
    request_data = {"query_string": "test query", "alg": "mock_algorithm"}

    # Act: Make a POST request
    response = client.post("/search/", json=request_data)

    # Assert: Check that a 500 error is returned
    assert response.status_code == 500
    assert response.json() == {"detail": "Server error"}
