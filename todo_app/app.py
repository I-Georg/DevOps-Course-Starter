
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item
import requests
import json
import os
import logging


app = Flask(__name__)
app.config.from_object(Config)


#@app.route('/')

#r= requests.get("https://api.trello.com/1/members/me/boards?fields=name,url&key=77f5ab920b78a542ed2fb7501190d22d&token=1b81c916acc9144aa57afc7decdd1249d033e0bf52d300c5587dd38aa3acc846")
#r.content

#r = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3"
#url = "https://api.trello.com/1/boards/{id}"
#url = "https://api.trello.com/1/members/me/boards?fields=name,url"
#&key=77f5ab920b78a542ed2fb7501190d22d&token=1b81c916acc9144aa57afc7decdd1249d033e0bf52d300c5587dd38aa3acc846"
#id = "6005828032dafa5707bf5dc3"
#url = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/lists" #get board lists
#url = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/cards/6012a4a01353064030144e40"
#url = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/cards"
#url = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/labels"
#url = "https://api.trello.com/1/cards/6005828032dafa5707bf5de4/list"
#url = "https://api.trello.com/1/members/me/board"
#url = "https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/cards"
#url="https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/cards"

def getToDo():
	url = "https://api.trello.com/1/lists/6005828032dafa5707bf5dc5/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	response = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	#yo= response.text
    
	return response

def getDoing():
	url = "https://api.trello.com/1/lists/6005828032dafa5707bf5dc6/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	responseDoing = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	#yo= response.text
    
	return responseDoing
	
def getDone():
	url = "https://api.trello.com/1/lists/6005828032dafa5707bf5dc7/cards"

	headers = {
		"Accept": "application/json"
	}

	query = {
		'key': os.environ['KEY'],
		'token' : os.environ['TOKEN']
	}

	responseDone = requests.request(
		"GET",
		url,
		headers=headers,
		params=query
	)
	#yo= response.text
    
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
	url = "https://api.trello.com/1/cards/id"

	headers = {
		"Accept": "application/json"
	}

	query = {
	    'id': id,
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

	



@app.route('/')

def index():
 response = getToDo()
 responseDoing = getDoing()
 responseDone = getDone()
 #yo= response.text
 jsonResponse = response.json()
 jsonResponseDoing = responseDoing.json()
 jsonResponseDone = responseDone.json()
 number = len(jsonResponse)
 numberTwo = len(jsonResponseDoing)
 numberThree = len(jsonResponseDone)
 #print(jsonResponse[1])
 
 for listNumber in range(number):
	 print(jsonResponse[listNumber]['name'])
	 print("AAAAAAAA")
	 print(jsonResponse[listNumber]['id'])

 return render_template("index.html", jsonResponse = jsonResponse, jsonResponseDoing = jsonResponseDoing,jsonResponseDone = jsonResponseDone, number = number, numberTwo = numberTwo, numberThree = numberThree)

@app.route('/create', methods =['POST'])
def create():
 title = request.form.get('title')
 
 newToDoCard(title)
 return redirect(url_for('index'))


 
@app.route('/update', methods =['POST'])
def update():
 app.logger.info('Processing default request')
 
 id = request.form.get('id')
 #id = request.args.get('id')
 updateCardToDone(id)
 print(id)
 print('oooooooo')
 #request.method == 'PUT'
 #updateCardToDone(id)
 return redirect(url_for('index'))
 
@app.route('/updated', methods =['PUT'])
def updated(input):
 #app.logger.info('Processing default request')
 #request.method == 'PUT'
 updateCardToDone(input)
 return redirect(url_for('index'))
 
if __name__ == '__main__':
                             
	app.run()
#print(response.json)

#get lists with all ids https://api.trello.com/1/lists/6005828032dafa5707bf5dc5/cards?key=77f5ab920b78a542ed2fb7501190d22d&token=1b81c916acc9144aa57afc7decdd1249d033e0bf52d300c5587dd38aa3acc846
#parse json data to get ids
#get ids of a task- print ids GET /1/cards/{id}/id
#add ids to a value
#print values name


#headers = {
  # "Accept": "application/json"
#}

#query = {
  # 'key': '77f5ab920b78a542ed2fb7501190d22d',
   #'token': '1b81c916acc9144aa57afc7decdd1249d033e0bf52d300c5587dd38aa3acc846'
#}

#response = requests.request(
  # "GET",
   # url,
  # headers=headers,
  # params=query
#)

#print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))
	#return render_template("index.html",items = get_items())
	
#@app.route('/create', methods =['POST'])
#def create():
   
	#title = request.form.get('title')
	#added_item	= add_item(title)
	
	#return redirect(url_for('index'))
	
#@app.route('/save', methods =['POST'])
#def save_item_as_completed():
   
    #if request.method == 'POST':
	    #get_id = request.form.get('itemId')
	
	   # items = get_item(get_id)
	    #updated = save_item(items)
		
   
    #return redirect(url_for('index'))



