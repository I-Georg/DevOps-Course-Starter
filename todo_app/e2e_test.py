import os
import pytest
import requests
from threading import Thread
from selenium import webdriver
from flask import Flask
import os
#from todo_app.app import create_app
#os.path.dirname(r'todo_app\app.py')
from todo_app.app import create_app
from dotenv import load_dotenv,find_dotenv




def create_trello_board():
    #board_id = create_trello_board()
    #os.environ['TOID'] = board_id
    #application = create_app()
    response = f'https://api.trello.com/1/boards/6005828032dafa5707bf5dc3/lists'
    lists = response.json()
    for list in lists:
        if list['name'] == "To Do":
            os.environ['TOID'] = list['id']
    return board_id
    #return application
    
@pytest.fixture(scope='module')
def app_with_temp_board():
# Create the new board & update the board id environment variable
    
   
# construct the new application
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    board_id = create_trello_board()
    os.environ['TOID'] = board_id
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
     submit_update_to_done = '/html/body/p[18]/input[2]'
     driver.find_element_by_xpath(submit_update_to_done).click()

#def test_return_to_to_do(driver, app_with_temp_board):
     #driver.get('http://localhost:5000/')
     #submit_return_to_do = '/html/body/b/details/form[1]/input[2]'
     #driver.find_element_by_xpath(submit_return_to_do).click()if __name__ == '__main__':
 