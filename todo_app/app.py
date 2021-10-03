
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
from flask import LoginManager


def create_app():
    app = Flask(__name__)

    toDoId = os.environ['TOID']
    doingId = os.environ['DOINGID']
    doneId = os.environ['DONE']
    dbconnect = os.environ['CLIENT']

    def connectDb():
        client = pymongo.MongoClient(
            dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
        print(client.list_database_names())
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc3'}, {"name": 1})
        for x in todo:
            print(x)
            x
        doing = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc7'}, {"name": 1})
        for x in todo:
            print(x)
        done = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})
        for x in doing:
            print(x)

    login_manager = LoginManager()

    @login_manager.unauthorized_handler
    def unauthenticated():
        return redirect(url_for("https://github.com/login/oauth/authorize"))

    @login_manager.user_loader
    def load_user(user_id):
        return None

    login_manager.init_app(app)

    def create_items(name):
        client = pymongo.MongoClient(
            dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        date_now = datetime.now().strftime('%Y-%m-%d')

        post = {"name": name, "idBoard": "6005828032dafa5707bf5dc3",
                "last_modified": date_now}

        trello_collection = database["trello_collection"]
        result = trello_collection.insert_one(post)

    def update_item(id):
        client = pymongo.MongoClient(
            dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        post = {"_id": ObjectId(id)}
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.update_one(
            post, {"$set": {"idBoard": "6005828032dafa5707bf5dc5",
                            "last_modified": date_now}}
        )

    def return_todo(id):
        client = pymongo.MongoClient(
            dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        post = {"_id": ObjectId(id)}
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.update_one(
            post, {"$set": {"idBoard": "6005828032dafa5707bf5dc3",
                            "last_modified": date_now}}
        )

    # def show_done():
    #    client = pymongo.MongoClient(
    #        "mongodb+srv://admin:MongoAdmin1@cluster0.qtpde.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True, ssl_cert_reqs='CERT_NONE')
    #    database = client["01"]
    #    trello_collection = database["trello_collection"]
    #    date_now = datetime.now().strftime('%Y-%m-%d')
    #    result = trello_collection.find(
    #        {"idBoard": "6005828032dafa5707bf5dc5",
    #         "last_modified": date_now}
    #    )

    @app.route('/')
    def index():
        connectDb()
        # show_done()
        client = pymongo.MongoClient(
            dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc3'}, {"name": 1})
        doing = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc7'}, {"name": 1})
        done = trello_collection.find(
            {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})

        my_items = []
        doing_objects = []
        done_objects = []

        for todo in trello_collection.find({'idBoard': '6005828032dafa5707bf5dc3'}):
            my_items.append(ToDo.from_mongo_db_entry(todo))
        for doing in trello_collection.find({'idBoard': '6005828032dafa5707bf5dc7'}):
            doing_objects.append(ToDo.from_mongo_db_entry(doing))
        for done in trello_collection.find({'idBoard': '6005828032dafa5707bf5dc5'}):
            done_objects.append(ToDo.from_mongo_db_entry(done))
        view_model = ViewModel(my_items, doing_objects, done_objects)
        #todo_item = ToDo.from_mongo_db_entry(todo)
        view_model.show_all_done_items()

        return render_template("index.html", my_items=my_items, doing_objects=doing_objects, done_objects=done_objects, view_model=view_model)

    @app.route('/create', methods=['POST'])
    def create():
        title = request.form.get('title')

        create_items(title)
        # newToDoCard(title)

        return redirect(url_for('index'))

    @app.route('/complete_item', methods=['PUT'])
    def complete_item(id):

        print(id)

        update_item(id)
        return redirect(url_for('index'))

    @app.route('/update', methods=['POST'])
    def update():
        app.logger.info('Processing default request')
        id = request.form.get('id')
        print(id)

        update_item(id)

        return complete_item(id)

    @app.route('/return_item', methods=['PUT'])
    def return_item(n):
        app.logger.info('Processing default request')
        print(n)

        return_todo(n)
        return redirect(url_for('index'))

    @app.route('/update_back', methods=['POST'])
    def update_back():

        n = request.form.get('n')
        print(n)
        return return_item(n)

    if __name__ == '__main__':

        app.run(debug=True, host='0.0.0.0', port=5001)

    return app
