
from flask import Flask, request, render_template, redirect, url_for


from todo_app.flask_config import Config
from todo_app.data.ViewModel import ViewModel
from todo_app.data.ToDo import ToDo
from datetime import date
import requests
import os
import pymongo
from bson.objectid import ObjectId


from datetime import datetime


def create_app():
    app = Flask(__name__)

    toDoId = os.environ['TOID']
    doingId = os.environ['DOINGID']
    doneId = os.environ['DONE']

    def connectDb():
        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        print(client.list_database_names())
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})
        for x in todo:
            # print(x)
            x
        doing = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})
        for x in todo:
            print(x)
        done = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc7'}, {"name": 1})
        for x in doing:
            print(x)
        #post= {"id": "6005828032dafa5707bf5dc5", "name": "","id": "6005828032dafa5707bf5dc6","name": "DOING ", "idBoard": "6005828032dafa5707bf5dc3","id": "6005828032dafa5707bf5dc7", "name": "DONE!"}
        # result=trello_collection.insert_many(post)
        # result.inserted_id
#
        # result.acknowledged
#
        # trello_collection.find_one()
     # get doing
        # cursor=trello_collection.find({'idBoard': '6005828032dafa5707bf5dc5'},{"name": 1})
        # for x in cursor:
        # 	print(x)

    def createItems(name):
        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        dateNow = datetime.now()
        post = {"name": name, "idBoard": "6005828032dafa5707bf5dc3",
                "dateCreated": dateNow}
        trello_collection = database["trello_collection"]
        result = trello_collection.insert_one(post)
        app.logger.info("Result acknowledged" + result.acknowledged)

    def updateItem(id):
        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        dateNow = datetime.now()
        post = {"_id": ObjectId(id), "dateCreated": dateNow}
        trello_collection = database["trello_collection"]
        result = trello_collection.update_one(
            post, {"$set": {"idBoard": "6005828032dafa5707bf5dc7"}})
        app.logger.info("Result acknowledged" + result.acknowledged)

    def getItems(idList):
        url = f"https://api.trello.com/1/lists/{idList}/cards"
        headers = {
            "Accept": "application/json"
        }
        query = {
            'id': idList,
            'key': os.environ['KEY'],
            'token': os.environ['TOKEN'],
            'fields': 'all'
        }
        response = requests.get(

            url,
            headers=headers,
            params=query
        )

        return response

    def newToDoCard(name):
        url = "https://api.trello.com/1/cards"
        query = {
            'key': os.environ['KEY'],
            'token': os.environ['TOKEN'],
            'idList': toDoId,
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
            'token': os.environ['TOKEN'],
            'idList': doneId,
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
            'token': os.environ['TOKEN'],
            'idList': toDoId,
        }
        response = requests.request(
            "PUT",
            url,
            headers=headers,
            params=query
        )

    @app.route('/')
    def index():
        connectDb()
        client = pymongo.MongoClient(
            "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc3'}, {"name": 1})
        doing = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})
        done = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc7'}, {"name": 1})

        idList = toDoId
        responseTodo = getItems(idList)
        jsonResponse = responseTodo.json()
        idListDoing = doingId
        responseDoing = getItems(idListDoing)
        jsonResponseDoing = responseDoing.json()
        idListDone = doneId
        responseDone = getItems(idListDone)
        jsonResponseDone = responseDone.json()
        number = len(jsonResponse)
        number = len(jsonResponse)
        numberTwo = len(jsonResponseDoing)
        numberThree = len(jsonResponseDone)

        my_objects = []
        doing_objects = []
        done_objects = []

        for listNumber in range(len(jsonResponse)):
            my_objects.append(ToDo(jsonResponse[listNumber]['id'], jsonResponse[listNumber]
                              ['name'], jsonResponse[listNumber]['dateLastActivity']))
        for listNumberDoing in range(len(jsonResponseDoing)):
            doing_objects.append(ToDo(jsonResponseDoing[listNumberDoing]['id'], jsonResponseDoing[listNumberDoing]
                                 ['name'], jsonResponseDoing[listNumberDoing]['dateLastActivity']))
        for listNumberDone in range(len(jsonResponseDone)):
            done_objects.append(ToDo(jsonResponseDone[listNumberDone]['id'], jsonResponseDone[listNumberDone]
                                ['name'], jsonResponseDone[listNumberDone]['dateLastActivity']))
        view_model = ViewModel(my_objects, doing_objects, done_objects)
        #view_model1 = ViewModel(todo,doing,done)
        view_model.show_all_done_items()

        return render_template("index.html", view_model=view_model, todo=todo, doing=doing, done=done)

    @app.route('/create', methods=['POST'])
    def create():
        title = request.form.get('title')

        createItems(title)
        newToDoCard(title)

        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['PUT'])
    def complete_item(id):
        app.logger.info('Processing default request')
        print(id)
        updateCardToDone(id)

        return redirect(url_for('index'))

    @app.route('/update', methods=['POST'])
    def update():
        app.logger.info('Processing default request')
        id = request.form.get('id')
        print(id)
        updateItem(id)
        return complete_item(id)

    @app.route('/return_item', methods=['PUT'])
    def return_item(n):
        app.logger.info('Processing default request')
        print(n)
        returnCardToDo(n)
        return redirect(url_for('index'))

    @app.route('/update_back', methods=['POST'])
    def update_back():
        app.logger.info('Processing default request')
        n = request.form.get('n')
        print(n)
        return return_item(n)

    if __name__ == '__main__':

        app.run(debug=True, host='0.0.0.0', port=5001)

    return app
