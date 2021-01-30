
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item
import requests
import json
import os


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
yo= response.text
print(response.text)
print("áaa")
print(os.environ)


@app.route('/')

def index():
 
 print(os.environ['TOKEN'])
 yo= response.text
 jsonResponse = response.json()
 number = len(jsonResponse)
 print("Print each key-value pair from JSON response")
 #print(jsonResponse[1])
 
 for listNumber in range(number):
	 print(jsonResponse[listNumber]['name'])

 return render_template("index.html", jsonResponse = jsonResponse, number = number)

 
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



