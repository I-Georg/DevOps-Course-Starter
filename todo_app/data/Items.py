from datetime import date
import os
import requests
from todo_app.data.ToDo import ToDo



class ViewModel:
  def __init__(self, items):
    self._items = items 
    
  @property
  def items(self):
     return self._items
 
  def getItem(self,idList):
	    url = f"https://api.trello.com/1/lists/{idList}/cards"

	    headers = {
	    	"Accept": "application/json"
	    }

	    query = {
	      'id' : idList,
		    'key': os.environ['KEY'],
		    'token' : os.environ['TOKEN'],
		    'fields': 'all'
      	}

	    response = requests.request(
	    	"GET",
	    	url,
		    headers=headers,
		    params=query
	    )
	
    
	    return response
  
  

  def show_all_done_items(self):
    today = date.today()
    idListDone = os.environ['DONE']
    #import pdb; pdb.set_trace()
    responseDone = self.getItem(idListDone)
    jsonResponseDone = responseDone.json()
    numberThree = len(jsonResponseDone)
    if numberThree < 5:
      return true
    else: 
      return recent_done_items
    

  def recent_done_items():
    today = date.today()
    doneId = os.environ['DONE']
    idListDone = doneId
    responseDone = self.getItem(idListDone)
    jsonResponseDone = responseDone.json()
    if jsonResponseDone.dateLastActivity == today:
      return jsonResponseDone
    

  def older_done_items():
    today = date.today()
    doneId = os.environ['DONE']
    idListDone = doneId
    responseDone = getItem(idListDone)
    jsonResponseDone = responseDone.json()
    if jsonResponseDone.dateLastActivity != today:
      return jsonResponseDone.dateLastActivity != today
    
  
  

  

