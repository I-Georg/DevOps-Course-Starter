from datetime import date
import os
import requests
from todo_app.data.ToDo import ToDo
import datetime
from datetime import datetime



class ViewModel:
  def __init__(self, todolist, doinglist, donelist):
    
    self._todolist = todolist
    self._doinglist = doinglist
    self._donelist = donelist    
  
  @property
  def todolist(self):
     return self._todolist
     
  @property
  def doinglist(self):
     return self._doinglist
  
  @property
  def donelist(self):
     return self._donelist
 

  

  def show_all_done_items(self):
    today = date.today()
    
    number = len(self.donelist)
    if number < 5:
      return True
    else: 
      return False
   

  def recent_done_items(self):
    
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
    
    
    
    return [item for item in self.donelist if datetime.strptime(item.dateLastActivity,"%Y-%m-%dT%H:%M:%S.%fZ").date() == date_time ]
    
    

  def older_done_items(self):
   
    now = datetime.now()
    date_time = now.strftime("%Y-%m-%d")
	  
    
    
    return [item for item in self.donelist if datetime.strptime(item.dateLastActivity,"%Y-%m-%dT%H:%M:%S.%fZ").date() != date_time ]
    
  


  
