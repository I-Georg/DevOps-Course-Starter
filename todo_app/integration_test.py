import pytest
import dotenv
from dotenv import load_dotenv, find_dotenv
import os
from os.path import join, dirname
from dotenv import find_dotenv
from todo_app.app import create_app
from unittest.mock import patch, Mock
#import responses
import requests
#import vcr
import mongomock
from flask import Flask
import pymongo


@pytest.fixture
def client():
    # Use our test integration config instead of the'real' version
    file_path = find_dotenv('.env.test')
    load_dotenv(file_path, override=True)
    with mongomock.patch(servers=(('fakemongo.com', 27017),)):

        test_app = app.create_app()
    with test_app.test_client() as client:
        objects = {"name": "test", "idBoard": "test",
                   "last_modified": "2021-03-15"}
        client = pymongo.MongoClient('fakemongo.com')
        client.db.collection.insert_many(objects)
        yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    mock_get_requests.side_effect = mock_get_lists
    url = f'/'
    response = client.get(url)
    assert "test data" in response.data.decode()


def mock_get_lists(url, headers, params):
    test_board_id = 'test'
    if url == f'fakemongo.com':
        response = Mock()

# sample_mongo_response should point to some test response data
        sample_mongo_response = [{"id": "test",
                                  "dateLastActivity": "2021-03-15",
                                  "name": "test"}]
        response.json.return_value = sample_mongo_response

        return response
    if url == f'fakemongo.com':
        response = Mock()
        sample_mongo_response = [{"id": "test",
                                  "dateLastActivity": "2021-03-15",
                                  "name": "test"}]
        response.json.return_value = sample_mongo_response

        return response
    if url == f'fakemongo.com':
        response = Mock()
        sample_mongo_response = [{"id": "test",
                                  "dateLastActivity": "2021-03-15",
                                  "name": "test"}]
        response.json.return_value = sample_mongo_response
        return response

    return None


def mock_get_cards(url, params):
    test_cardid = 'test'
    if url == f'/':
        response = Mock()
# sample_mongo_response should point to some test response data
        response.json.return_value = sample_mongo_response
        assert response.json() == {"id": "test",
                                   "dateLastActivity": "2021-03-15",
                                   "name": "test"}
        assert response.status_code == 200

        return response
    return None
# @pytest.mark.vcr()
# def test_get():
    #response = requests.get('http://localhost:5000/')
    #assert 'body' in response == ''
