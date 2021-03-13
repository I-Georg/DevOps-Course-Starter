import pytest
import dotenv
from dotenv import load_dotenv
import os
from os.path import join, dirname
from dotenv import find_dotenv
#from todo_app import create_app
#from flask import create_app
from todo_app.app import create_app

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
def test_index_page(client):
    response = client.get('/')