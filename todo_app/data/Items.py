from datetime import date
import os
import requests



class ViewModel:
   
  

  def __init__(self, id, name,dateLastActivity):
    self.id = id
    self.name = name
    self.dateLastActivity = dateLastActivity
	 
  @property
  def items(self):
     return self._name
 
  def getItem(idList):
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
  
  

  def show_all_done_items():
    today = date.today()
    idListDone = os.environ['DONE']
    #import pdb; pdb.set_trace()
    responseDone = getItem(idListDone)
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
    responseDone = getItem(idListDone)
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
    
  show_all_done_items()
  
  

  

