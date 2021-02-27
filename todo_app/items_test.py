
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


	
	#test to do list
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
	
	
		
def test_getting_doing():
	
	idListDoing = doingId
	responseDoing = getItems(idListDoing)
	jsonResponseDoing = responseDoing.json()	
	numberTwo = len(jsonResponseDoing)
	doing_objects =[]
	
	for listNumberDoing in range(numberTwo):
		doing_objects.append(ViewModel(jsonResponseDoing[listNumberDoing]['id'],jsonResponseDoing[listNumberDoing]['name']))
		
	assert doing_objects[0].name == '✋🏿 Move anything that is actually started here'
	assert doing_objects[1].name == 'Doing'
	assert doing_objects[2].name == 'Doing Task'

def test_getting_done():
	idListDone = doneId
	responseDone = getItems(idListDone)
	jsonResponseDone = responseDone.json()
	numberThree = len(jsonResponseDone)
	done_objects = []
	for listNumberDone in range(numberThree):
	
		done_objects.append(ViewModel(jsonResponseDone[listNumberDone]['id'],jsonResponseDone[listNumberDone]['name']))	 
	assert done_objects[0].name == '✋🏿 Move anything from doing to done here'
	assert done_objects[2].name == 'Third Task'
	assert done_objects[3].name == 'title'
	assert done_objects[4].name == '✋🏿 Move anything ready here'
	assert done_objects[5].name == 'First task'

def test_show_all_done_items:	
	idListDone = doneId
	responseDone = getItems(idListDone)
	jsonResponseDone = responseDone.json()
	numberThree = len(jsonResponseDone)
	done_objects = []
	x=len(doing_objects)
	print(x)