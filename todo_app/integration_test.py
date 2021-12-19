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

        test_app = create_app()
        with test_app.test_client() as client:
            objects = {"name": "test", "idBoard": "test",
                       "last_modified": "2021-03-15"}
            db_client = pymongo.MongoClient('fakemongo.com')
            db_client.db.collection.insert_one(objects)
            yield client


@patch('requests.get')
def test_index_page(mock_get_requests, client):
    # Replace call to requests.get(url) with our own function
    url = f'/'
    response = client.get(url)
    assert response.status_code == 200
