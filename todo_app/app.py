
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
# import urllib.request
from flask import request
from flask_login import UserMixin, login_user, current_user
from todo_app.data.UserClass import User
import json


def create_app():
    app = Flask(__name__)

    toDoId = os.environ['TOID']
    doingId = os.environ['DOINGID']
    doneId = os.environ['DONE']
    dbconnect = os.environ['CLIENT']
    app.secret_key = os.getenv('SECRET_KEY')

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
        client = WebApplicationClient('89647e3bf34e5c0f2e50')
        full_redirect_url = client.prepare_request_uri(
            'https://github.com/login/oauth/authorize', redirect_uri='http://localhost:5000/callback')
        # x = request.args.get("code")
        # print(x)
        # for resp in request.args.get:
        #     print(resp.url)

        # print(request.url)
        # print(request.args.getlist)
        # redirect_uri = 'http://localhost:5000/callback?code=df0e4d5d057d32a13d4f'
        # code = client.parse_request_uri_response(full_redirect_url)
        # code = parse.urlsplit(full_redirect_url)
        # x = requests.head(full_redirect_url)
        # code = dict(parse.parse_qsl(parse.urlsplit(full_redirect_url).query))
        # print("AAAAAA")
        # print(x.url)
        # for resp in x.history:
        #     print(resp.status_code, resp.url)
        # res = urllib.request.urlopen(
        #     "https://github.com/login/oauth/authorize")
        # finalurl = res.geturl()
        # print(finalurl)
        # data = requests.request(
        #     "GET", "http://localhost:5000/callback")
        # url = data.url
        # print(url)
        # url_get = request.host_url
       # current_url = request.query_string

       # print(current_url)
        # print(code["redirect_uri"])

        return redirect(full_redirect_url)

    @login_manager.user_loader
    def load_user(user_id):
        # client = WebApplicationClient('89647e3bf34e5c0f2e50')
        # code = request.args.get("code")
        # client_secret = '50d6114064c16235db5973535c97b5d6cda6faaf'
        # (url, headers, body) = client.prepare_token_request(
        #     'https://github.com/login/oauth/access_token', code=code, client_secret=client_secret)
        # get_token_request = requests.post(url, headers=headers, data=body)
        # parse_body = client.parse_request_body_response(get_token_request.text)
        # (url, headers, body) = client.add_token("https://api.github.com/user")
        # user = requests.get(url, headers=headers, data=body)
        # login_user(user, remember=False, duration=None,
        #            force=False, fresh=True)
        user_id = User(id, role="reader")
        return user_id

    login_manager.init_app(app)

    # def callback_route():

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
    @login_required
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
        # todo_item = ToDo.from_mongo_db_entry(todo)
        view_model.show_all_done_items()
        user = current_user.role

        return render_template("index.html", my_items=my_items, doing_objects=doing_objects, done_objects=done_objects, view_model=view_model, current_user=current_user)

    @app.route('/create', methods=['POST'])
    @login_required
    def create():
        print(current_user.id)
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

    @app.route('/callback')
    def login_callback():
        client = WebApplicationClient('89647e3bf34e5c0f2e50')
        code = request.args.get("code")
        client_secret = '50d6114064c16235db5973535c97b5d6cda6faaf'
        (url, headers, body) = client.prepare_token_request(
            'https://github.com/login/oauth/access_token', code=code, client_secret=client_secret)
        get_token_request = requests.post(url, headers=headers, data=body)
        parse_body = client.parse_request_body_response(get_token_request.text)
        (url, headers, body) = client.add_token("https://api.github.com/user")

        request_text = requests.get(url, headers=headers, data=body).text

        json_data = json.loads(request_text)
        id = json_data["id"]
        if id == "I-Georg":
            role = "writer"
        else:
            role = "reader"
        user = User(id, role)
        login_user(user, remember=False, duration=None,
                   force=False, fresh=True)
        # load_user(user)

        return redirect(url_for('index'))

    if __name__ == '__main__':

        app.run(debug=True, host='0.0.0.0', port=5001)

    return app
