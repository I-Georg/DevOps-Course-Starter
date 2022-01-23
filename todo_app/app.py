
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
from flask_login import LoginManager
from oauthlib.oauth2 import WebApplicationClient
from flask_login import login_required
from urllib import parse
from flask import request
from flask_login import UserMixin, login_user, current_user
from todo_app.data.UserClass import User
import json


def create_app():
    app = Flask(__name__)
    githubId = os.environ['GITHUBID']
    webClient = os.environ['WEBAPPLICATIONCLIENT']
    clientSecret = os.environ['CLIENTSECRET']
    todoBoard = os.environ['TODOBOARD']
    doingBoard = os.environ['DOINGBOARD']
    doneBoard = os.environ['DONEBOARD']
    connectString = os.environ['CONNECTIONSTRING']
    app.secret_key = os.getenv('SECRET_KEY')
    app.config['LOGIN_DISABLED'] = os.getenv('LOGIN_DISABLED') == 'True'

    def connectDb():

        client = pymongo.MongoClient(
            connectString, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': todoBoard}, {"name": 1})
        for x in todo:
            print(x)

        doing = trello_collection.find(
            {'idBoard': doingBoard}, {"name": 1})
        for x in todo:
            print(x)

        done = trello_collection.find(
            {'idBoard': doneBoard}, {"name": 1})
        for x in doing:
            print(x)

    login_manager = LoginManager()
    login_manager.anonymous_user.role = 'writer'

    @login_manager.unauthorized_handler
    def unauthenticated():
        client = WebApplicationClient(webClient)
        full_redirect_url = client.prepare_request_uri(
            'https://github.com/login/oauth/authorize', redirect_uri='http://localhost:5000/callback')

        return redirect(full_redirect_url)

    @login_manager.user_loader
    def load_user(user_id):

        if user_id == githubId:
            role = "writer"
        else:
            role = "reader"
        id = User(user_id, role)
        print(role)

        return id

    login_manager.init_app(app)

    def create_items(name):

        client = pymongo.MongoClient(
            connectString, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        date_now = datetime.now().strftime('%Y-%m-%d')

        post = {"name": name, "idBoard": todoBoard,
                "last_modified": date_now}

        trello_collection = database["trello_collection"]
        result = trello_collection.insert_one(post)

    def update_item(id):
        client = pymongo.MongoClient(
            connectString, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        post = {"_id": ObjectId(id)}
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.update_one(
            post, {"$set": {"idBoard": doneBoard,
                            "last_modified": date_now}}
        )

    def return_todo(id):
        client = pymongo.MongoClient(
            connectString, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        post = {"_id": ObjectId(id)}
        trello_collection = database["trello_collection"]
        date_now = datetime.now().strftime('%Y-%m-%d')
        result = trello_collection.update_one(
            post, {"$set": {"idBoard": todoBoard,
                            "last_modified": date_now}}
        )

    @app.route('/')
    @login_required
    def index():
        connectDb()
        client = pymongo.MongoClient(
            connectString, ssl=True, ssl_cert_reqs='CERT_NONE')
        database = client["01"]
        trello_collection = database["trello_collection"]
        todo = trello_collection.find(
            {'idBoard': todoBoard}, {"name": 1})
        doing = trello_collection.find(
            {'idBoard': doingBoard}, {"name": 1})
        done = trello_collection.find(
            {'idBoard': doneBoard}, {"name": 1})

        my_items = []
        doing_objects = []
        done_objects = []

        for todo in trello_collection.find({'idBoard': todoBoard}):
            my_items.append(ToDo.from_mongo_db_entry(todo))
        for doing in trello_collection.find({'idBoard': doingBoard}):
            doing_objects.append(ToDo.from_mongo_db_entry(doing))
        for done in trello_collection.find({'idBoard': doneBoard}):
            done_objects.append(ToDo.from_mongo_db_entry(done))
        view_model = ViewModel(my_items, doing_objects, done_objects)
        view_model.show_all_done_items()
        user = current_user.role

        return render_template("index.html", my_items=my_items, doing_objects=doing_objects, done_objects=done_objects, view_model=view_model, user=user)

    @app.route('/create', methods=['POST'])
    @login_required
    def create():
        if app.config.get('LOGIN_DISABLED') or current_user.role == "writer":
            title = request.form.get('title')
            create_items(title)
        else:
            print('User does not have writer role.')

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

    @app.route('/callback')
    def login_callback():
        client = WebApplicationClient(webClient)
        code = request.args.get("code")
        client_secret = clientSecret
        (url, headers, body) = client.prepare_token_request(
            'https://github.com/login/oauth/access_token', code=code, client_secret=client_secret)
        get_token_request = requests.post(url, headers=headers, data=body)
        parse_body = client.parse_request_body_response(get_token_request.text)
        (url, headers, body) = client.add_token("https://api.github.com/user")

        request_text = requests.get(url, headers=headers, data=body).text

        json_data = json.loads(request_text)
        id = json_data["id"]
        if id == githubId:
            role = "writer"
        else:
            role = "reader"
        user = User(id, role)
        login_user(user)

        return redirect(url_for('index'))

    if __name__ == '__main__':

        app.run(debug=True, host='0.0.0.0', port=5001)

    return app
