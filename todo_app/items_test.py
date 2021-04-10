
from todo_app.data.ViewModel import ViewModel
from datetime import date
from flask import Flask,request, render_template,redirect,url_for
import pytest
import requests
import os
from todo_app.data.ToDo import ToDo
from todo_app.app import create_app

#tried to fix no key error after poetry install pytest && selenium
#app = Flask(__name__)
#app.config.from_object('flask_config.TestingConfig')
#print(app.config)

#SECRET_KEY = os.environ.get('SECRET_KEY')
#def create_app(self):

	#app = Flask(__name__)
	#app.config['TESTING'] = True
	#app.secret_key = os.environ['SECRET_KEY']
	#return app

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


def recent_done_items():
     today = date.today()
     doneId = os.environ['DONE']
     idListDone = doneId
     responseDone = self.getItem(idListDone)
     jsonResponseDone = responseDone.json()
     if jsonResponseDone.dateLastActivity == today:
      	return jsonResponseDone
    	
	#test to do list
def test_getting_todo():

	idList = toDoId
	responseTodo= getItems(idList)
	jsonResponse = responseTodo.json()
	number = len(jsonResponse)
	my_objects = []
	
	for listNumber in range(number):
	
		my_objects.append(ToDo(jsonResponse[listNumber]['id'],jsonResponse[listNumber]['name'],jsonResponse[listNumber]['dateLastActivity']))
		
	assert my_objects[0].name == '✋🏿 Move anything from doing to done here!'
	assert my_objects[1].name == 'Inspiration for a Card 📝'
	assert my_objects[2].name == 'title'
	assert my_objects[3].name == '✋🏿 Move anything ready here'
	assert my_objects[4].name == 'title'
	assert my_objects[5].name == 'title'
	
	
		
def test_getting_doing():
	
	idListDoing = doingId
	responseDoing = getItems(idListDoing)
	jsonResponseDoing = responseDoing.json()	
	numberTwo = len(jsonResponseDoing)
	doing_objects =[]
	
	for listNumberDoing in range(numberTwo):
		doing_objects.append(ToDo(jsonResponseDoing[listNumberDoing]['id'],jsonResponseDoing[listNumberDoing]['name'],jsonResponseDoing[listNumberDoing]['dateLastActivity']))
		
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
	
		done_objects.append(ToDo(jsonResponseDone[listNumberDone]['id'],jsonResponseDone[listNumberDone]['name'],jsonResponseDone[listNumberDone]['dateLastActivity']) )
	assert done_objects[0].name == 'Task created today'
	assert done_objects[2].name == 'titlewwwwww'
	assert done_objects[3].name == 'title'
	assert done_objects[4].name == 'title'


def test_show_all_done_items():
	idListDone = doneId
	responseDone = getItems(idListDone)
	jsonResponseDone = responseDone.json()
	numberThree = len(jsonResponseDone)
	displayresponse = []
	done_objects = []
	today = date.today()
	for listNumberDone in range(numberThree):
		done_objects.append(ToDo(jsonResponseDone[listNumberDone]['id'],jsonResponseDone[listNumberDone]['name'],jsonResponseDone[listNumberDone]['dateLastActivity']))
		if numberThree < 5:	
			return True
			assert done_objects[1].name == 'Inspiration for a Card 📝'
		elif numberThree > 5:
			
			return 
			for listNumberDone in range(numberThree):
				displayresponse.append(ToDo(jsonResponseDone[listNumberDone]['id'],jsonResponseDone[listNumberDone]['name'],jsonResponseDone[listNumberDone]['dateLastActivity']== today))
	assert 	displayresponse[5] == ''
	
		#test suggested by  @JackMead 
	def test_show_all_done_items_true_if_1_done_item():
		 to_do_items = []
		 doing_items = []
		 done_items = [
			ToDo('id', 'name', date.today()),
		 ]
		 view_model = ViewModel(to_do_items, doing_items, done_items)

	 assert view_model.show_all_done_items() == True