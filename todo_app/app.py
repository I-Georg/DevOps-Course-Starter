
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    #return 'Hello World!'
	#items = get_items()
	
	return render_template("index.html",items = get_items())
	
@app.route('/create', methods =['POST','GET'])
def create():
    #return 'Hello World!'
	#items = get_items()
	title = request.form.get('title')
	print(title)
	#return render_template("index.html")
	return redirect(url_for('index'),)


if __name__ == '__main__':
    app.run()
