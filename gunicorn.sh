#!/bin/sh

gunicorn -b 0.0.0.0:$PORT "todo_app.app:create_app()"
#gunicorn --chdir . /todo_app app:. /todo_app 
#-w 2 --threads 2 -b 0.0.0.0:8000