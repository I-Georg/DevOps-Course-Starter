import pytest
import dotenv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from dotenv import find_dotenv
#from todo_app import create_app
#from flask import create_app
from todo_app.app import create_app
from unittest.mock import patch
import responses
import requests

@pytest.fixture
def client():
# Use our test integration config instead of the'real' version
    file_path = find_dotenv('.env.test')
    print(file_path)
    load_dotenv(file_path, override=True)
# Create the new app.
#test_app = app.create_app()
    test_app = create_app()
# Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client
#def test_client():
#    flask_app = create_app()
# 
#    # Flask provides a way to test your application by exposing the Werkzeug test Client
#    # and handling the context locals for you.
#    testing_client = flask_app.test_client()
# 
#    # Establish an application context before running the tests.
#    ctx = flask_app.app_context()
#    ctx.push()
# 
#    yield testing_client  # this is where the testing happens!
 
  #  ctx.pop()
#def test_index_page(client):
    #response = client.get('/')

@patch('requests.get')
def test_index_page(mock_get_requests, client):
# Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    url = f'https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/lists'
    response = client.get(url)
    
    

def mock_get_lists(url, params):
    test_board_id = '6052828032dafa5707bf5reg'
    if url == f'https://api.trello.com/1/boards/{test_board_id}/lists':
        response = Mock()
# sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response
        assert response.json() == { "id": "431228032dafa5707bf5de1",
        "dateLastActivity": "2021-03-05T15:04:16.124Z",
        "name": "test data"}
      
        return response
    return None