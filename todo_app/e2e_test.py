import os
import pytest
import requests
from threading import Thread
from selenium import webdriver
from flask import Flask
import os
from todo_app.app import create_app
from dotenv import load_dotenv,find_dotenv




def create_trello_board():
    
    key = os.environ['KEY']
    token = os.environ['TOKEN']
    board_response = requests.post(f'https://api.trello.com/1/boards/?name=test&key={key}&token={token}')
    board_id = board_response.json()["id"]
    response =  requests.get(f'https://api.trello.com/1/boards/{board_id}/lists?key={key}&token={token}')
    
	
    lists = response.json()
    
    for list in lists:
        
        if list['name'] == "TODO":
            os.environ['TOID'] = list['id']
        elif list['name'] == "DOING":
            os.environ['DOINGID'] = list['id']
        elif list['name'] == "DONE":
            os.environ['DONE'] = list['id']
    return board_id
    #return application

def delete_trello_board(board_id):
     key = os.environ['KEY']
     token = os.environ['TOKEN']
     board_delete = requests.delete(f'https://api.trello.com/1/boards/{board_id}?key={key}&token={token}')
   
    
@pytest.fixture(scope='module')
def app_with_temp_board():
# Create the new board & update the board id environment variable
    
   
# construct the new application
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board()
    
    application = create_app()
# start the app in its own thread.
    thread = Thread(target=lambda:
    application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    yield application
# Tear Down
    thread.join(1)
    delete_trello_board(board_id)

@pytest.fixture(scope="module")
def driver():
    #with webdriver.Firefox() as driver
    driver = webdriver.Firefox()
    yield driver
    driver.close()

def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'

def test_create_new_item(driver, app_with_temp_board):
     driver.get('http://localhost:5000/')
     create_test_task_input = '//*[@id="title"]'
     create_test_task_submit = '/html/body/p[20]/input[2]'
     update_to_done = '/html/body/p[18]/input[1]'
     submit_update_to_done = '/html/body/p[18]/input[2]'
     driver.find_element_by_xpath(create_test_task_input).click()
     driver.find_element_by_xpath(create_test_task_input).send_keys("testTASk")
     driver.find_element_by_xpath(create_test_task_submit).click()

def test_update_to_done_new_item(driver, app_with_temp_board):
     driver.get('http://localhost:5000/')
     submit_update_to_done ='//input[@type = "submit" and @value="Update to done"]'
     driver.find_element_by_xpath(submit_update_to_done).click()
     undo_completion_input = '//input[@type = "submit" and @value="Return to To do"]'
     assert driver.find_element_by_xpath(undo_completion_input ) != None


 