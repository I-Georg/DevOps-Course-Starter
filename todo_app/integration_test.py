import pytest
import dotenv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from dotenv import find_dotenv
from todo_app.app import create_app
from unittest.mock import patch
import responses
import requests
import vcr

#SECRET_KEY=os.environ['SECRET_KEY']
@pytest.fixture
def client():
# Use our test integration config instead of the'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
# Create the new app.
#test_app = app.create_app()
    test_app = create_app()
# Use the app to create a test_client that can be used in our tests.
    with test_app.test_client() as client:
        yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
# Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    test_board_id = '6052828032dafa5707bf5reg'
   # url = f'http://localhost:5000/'
    url = f'https://api.trello.com/1/boards/{test_board_id}/lists'
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
        assert response.status_code == 200
      
        return response
    return None
def mock_get_cards(url, params):
    test_cardid = '6052828032dafa5707bf3reg'
    if url == f'"https://api.trello.com/1/lists/{test_cardid}/cards"':
        response = Mock()
# sample_trello_lists_response should point to some test response data
        response.json.return_value = sample_trello_lists_response
        assert response.json() == { "id": "551238032dafa5707bf5de1",
        "dateLastActivity": "2021-03-23T15:04:16.124Z",
        "name": "test card"}
        assert response.status_code == 200
      
        return response
    return None
#@pytest.mark.vcr()
#def test_get():
    #response = requests.get('http://localhost:5000/')
    #assert 'body' in response == ''