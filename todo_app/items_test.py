
from todo_app.data.Items import ViewModel
from flask import Flask,request, render_template,redirect,url_for
import pytest
import requests
import os


toDoId = os.environ['TOID']
doingId = os.environ['DOINGID']
doneId = os.environ['DONE']


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
	
def test_getting_todo():
	idList = toDoId
	responseTodo= getItems(idList)
	jsonResponse = responseTodo.json()
	number = len(jsonResponse)
	my_objects = []
	for listNumber in range(number):
	
		my_objects.append(ViewModel(jsonResponse[listNumber]['id'],jsonResponse[listNumber]['name']))
	assert my_objects[0].name == 'title'
	assert my_objects[1].name == 'title'
	assert my_objects[2].name == 'title'
	assert my_objects[3].name == 'title1'
	assert my_objects[4].name == 'title'
	assert my_objects[5].name == 'koala'
	
	
		
		