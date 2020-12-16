
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
    #return 'Hello World!'
	#items = get_items()
	
	return render_template("index.html",items = get_items())
	
@app.route('/create', methods =['POST','GET'])
def create():
   
	title = request.form.get('title')
	lok = add_item(title)
	#print(lok)
    #print(lok)
	
	#return render_template("index.html")
	return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
