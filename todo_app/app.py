
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items
from todo_app.data.session_items import add_item
from todo_app.data.session_items import get_item
from todo_app.data.session_items import save_item

app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   
	return render_template("index.html",items = get_items())
	
@app.route('/create', methods =['POST','GET'])
def create():
   
	title = request.form.get('title')
	added_item	= add_item(title)
	
	return redirect(url_for('index'))
	
@app.route('/save', methods =['POST','GET'])
def update():
   #if item is saved then item.status= completed
    if request.method == 'POST':
	    get_id = request.form.get('itemId')
	
	    items = get_item(get_id)
	    updated = save_item(items)
   
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
