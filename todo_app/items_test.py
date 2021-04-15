
from todo_app.data.ViewModel import ViewModel
from datetime import date,timedelta
from flask import Flask,request, render_template,redirect,url_for
import pytest
import requests
import os
from todo_app.data.ToDo import ToDo


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
def test_recent_done_items():

	 to_do_items = []
	 doing_items = []
	 yesterday = (date.today() - timedelta(days=1)).isoformat()

	 done_items = [
 	 ToDo('id', 'name', date.today().isoformat()),ToDo('id', 'name',yesterday),
	 ]
	 
	 view_model = ViewModel(to_do_items, doing_items, done_items)
	 today_item = view_model.recent_done_items()

	 assert len(today_item) == 1
	 




		#test suggested by  @JackMead 
def test_show_all_done_items_true_if_1_done_item():
	 to_do_items = []
	 doing_items = []
	 done_items = [
 	 ToDo('id', 'name', date.today()),
	 ]
	 view_model = ViewModel(to_do_items, doing_items, done_items)

	 assert view_model.show_all_done_items() == True