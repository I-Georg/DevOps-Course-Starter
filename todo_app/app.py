
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item
import requests
import json
import os
import logging


app = Flask(__name__)
app.config.from_object(Config)


toDoId = os.environ['TOID']
doingId = os.environ['DOINGID']
doneId = os.environ['DONE']
def getToDo():
     
	url = f"https://api.trello.com/1/lists/{toDoId}/cards"
	
	headers = {
		"Accept": "application/json"
	}
     
	query = {
	    'id' : toDoId,
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
		
	}
	

	response = requests.request(
		"GET",
		url,
		headers=headers,
		params=query,
		
	)
	
	
    
	return response

def getDoing():
	url = f"https://api.trello.com/1/lists/{doingId}/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
	    'id' : doingId,
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	responseDoing = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	
    
	return responseDoing
	
def getDone():
	url = f"https://api.trello.com/1/lists/{doneId}/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
	    'id' : doneId,
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	responseDone = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	
    
	return responseDone
	
def newToDoCard(name):
	url = "https://api.trello.com/1/cards"

	query = {
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN'],
		'idList': '6005828032dafa5707bf5dc5',
		'name': name
	}

	response = requests.request(
		"POST",
		url,
		params=query
	)
def updateCardToDone(i):
	url = f"https://api.trello.com/1/cards/{i}"

	headers = {
		"Accept": "application/json"
	}

	query = {
	    'id': i,
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN'],
		'idBoard': '6005828032dafa5707bf5dc3',
		'idList': '6005828032dafa5707bf5dc7'
		
	}

	response = requests.request(
		"PUT",
		url,
		headers=headers,
		params=query
	)

def returnCardToDo(i):
		url = f"https://api.trello.com/1/cards/{i}"

		headers = {
			"Accept": "application/json"
		}

		query = {
			'id': i,
			'key': os.environ['KEY'],
			'token' : os.environ['TOKEN'],
			'idBoard': '6005828032dafa5707bf5dc3',
			'idList': '6005828032dafa5707bf5dc5'
		
		}

		response = requests.request(
			"PUT",
			url,
			headers=headers,
			params=query
	)



@app.route('/')

def index():
 response = getToDo()
 responseDoing = getDoing()
 responseDone = getDone()
 jsonResponse = response.json()
 jsonResponseDoing = responseDoing.json()
 jsonResponseDone = responseDone.json()
 number = len(jsonResponse)
 numberTwo = len(jsonResponseDoing)
 numberThree = len(jsonResponseDone)

 
 for listNumber in range(number):
	 print(jsonResponse[listNumber]['name'])
	 print(jsonResponse[listNumber]['id'])

 return render_template("index.html", jsonResponse = jsonResponse, jsonResponseDoing = jsonResponseDoing,jsonResponseDone = jsonResponseDone, number = number, numberTwo = numberTwo, numberThree = numberThree)

@app.route('/create', methods =['POST'])
def create():
 title = request.form.get('title')
 
 newToDoCard(title)
 return redirect(url_for('index'))

@app.route('/complete_item', methods =['PUT'])
def complete_item(id):
 app.logger.info('Processing default request')
 print(id)
 updateCardToDone(id)
 return redirect(url_for('index'))
 
@app.route('/update', methods =['POST'])
def update():
 app.logger.info('Processing default request')
 id = request.form.get('id')
 print(id)
 return complete_item(id)
 
@app.route('/return_item', methods =['PUT'])
def return_item(n):
 app.logger.info('Processing default request')
 print(n)
 returnCardToDo(n)
 return redirect(url_for('index'))
 
@app.route('/update_back', methods =['POST'])
def update_back():
 app.logger.info('Processing default request')
 
 n = request.form.get('n')
 print(n)
 return return_item(n)

 
if __name__ == '__main__':
                             
	app.run()




