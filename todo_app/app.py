
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item
from todo_app.data.Items import ToDo
import requests
import os



app = Flask(__name__)
app.config.from_object(Config)


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
 idList = toDoId
 responseTodo= getItems(idList)
 jsonResponse = responseTodo.json()
 idListDoing = doingId
 responseDoing = getItems(idListDoing)
 idListDone = doneId
 responseDone = getItems(idListDone)
 jsonResponseDoing = responseDoing.json()
 jsonResponseDone = responseDone.json()
 number = len(jsonResponse)
 numberTwo = len(jsonResponseDoing)
 numberThree = len(jsonResponseDone)
 
 my_objects = []
 
 for listNumber in range(number):
	
	 my_objects.append(ToDo(jsonResponse[listNumber]['id'],jsonResponse[listNumber]['name']))
	 
	 
 return render_template("index.html", jsonResponse = jsonResponse, jsonResponseDoing = jsonResponseDoing,jsonResponseDone = jsonResponseDone, number = number, numberTwo = numberTwo, numberThree = numberThree, my_objects = my_objects)

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




