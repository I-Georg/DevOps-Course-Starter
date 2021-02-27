
from todo_app.data.Items import ViewModel
from flask import Flask,request, render_template,redirect,url_for
import pytest
import os





toDoId = os.environ['TOID']
doingId = os.environ['DOINGID']
doneId = os.environ['DONE']

@pytest.fixture
def getItems(idList):
	url = f"https://api.trello.com/1/lists/{idList}/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
	    'id' : idList,
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	response = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	
    
	return response
	
