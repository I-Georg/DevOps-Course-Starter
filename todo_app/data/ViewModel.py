from datetime import date
import os
import requests
from todo_app.data.ToDo import ToDo
import datetime
from datetime import datetime
import pymongo


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

        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.find(
            {"idBoard": "6005828032dafa5707bf5dc5",
             "last_modified": date_now}
        )

        return [item for item in self.donelist if datetime.strptime(item.last_modified, '%Y-%m-%d').date() == now.date()]

    def older_done_items(self):

        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d")

        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.find(
            {"idBoard": "6005828032dafa5707bf5dc5", "last_modified": date_now})

        return [item for item in self.donelist if datetime.strptime(item.last_modified, "%Y-%m-%d").date() != now.date()]
