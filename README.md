# DevOps Apprenticeship: Project Exercise

## System Requirements

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```

### Poetry installation (PowerShell)

```powershell
(Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

## Dependencies

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:

```bash
$ poetry install
```

You'll also need to clone a new `.env` file from the `.env.template` to store local configuration options. This is a one-time operation on first setup:

```bash
$ cp .env.template .env  # (first time only)
```

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

## Running the App

Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.


## Configuring Trello API
First you need to create an account https://trello.com/signup
Then you need to generate API key and token (explained here https://trello.com/app-key). The link will display your key and you need to generate manually a token.
Put the variables to .env template as variables TOKEN = {Your token} and KEY = {Your key}.
In app.py you need to import os and you can call them as 'key': os.environ['KEY'] and 'token' : os.environ['TOKEN']
In order to access the id of the lists on the board: first - you need to put them to .env template as:
toDoId = {listId}
doingId = { listId}
doneId = {listId}
Those are the ones that should be assigned in the code rather than variable names.
In app. py they get called the following way:
toDoId = os.environ['TOID']
doingId = os.environ['DOINGID']
doneId = os.environ['DONE']


## Pytest
To add Pytest to the project, run: poetry install pytest

Unit Tests are in item_test.py
To run unit tests: cd into the app: cd todo_app and run:poetry run pytest items_test.py
To run integration tests: cd into the app: cd todo_app and run:poetry run pytest integration_test.py

## Selenium tests: 
For selenium tests to work:
Run: poetry install selenium
Depending on the browser(here is used Firefox): download the browser https://pypi.org/project/selenium/ , for Firefox you need latest version of gheko browser and  make sure it’s in your PATH. For Windows 10, if you keep getting error  Message: 'geckodriver' executable needs to be in PATH., add the geckodriver.exe under /Python/Scripts/ 
To run: poetry run pytest e2e_test.py


## Docker:  
docker build --target development --tag todo-app:dev .
docker build --target production --tag todo-app:prod .
docker run -p 5001:5001 --env-file .env  --mount=type=bind,source={source on your machine},target="/todo-app"  -d  todo-app

## Running test stage image in Docker:
docker build --target test --tag my-test-image .
docker run my-test-image todo_app/items_test.py    
docker run my-test-image todo_app/integration_test.py  
docker run --env-file .env my-test-image  todo_app/e2e_test.py 

## Vagrant:
You can run the app inside VM
