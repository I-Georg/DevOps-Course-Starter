
from flask import Flask,request, render_template,redirect,url_for


from todo_app.flask_config import Config
from todo_app.data.session_items import get_items, add_item, get_item, save_item


app = Flask(__name__)
app.config.from_object(Config)


@app.route('/')
def index():
   
	return render_template("index.html",items = get_items())
	
@app.route('/create', methods =['POST'])
def create():
   
	title = request.form.get('title')
	added_item	= add_item(title)
	
	return redirect(url_for('index'))
	
@app.route('/save', methods =['POST'])
def save_item_as_completed():
   
    if request.method == 'POST':
	    get_id = request.form.get('itemId')
	
	    items = get_item(get_id)
	    updated = save_item(items)
		
   
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
