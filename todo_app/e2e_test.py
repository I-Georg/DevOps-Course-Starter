import os
import pytest
import requests
from threading import Thread
from selenium import webdriver
from flask import Flask
import os
from todo_app.app import create_app
from dotenv import load_dotenv, find_dotenv
import time
import pymongo


os.environ['LOGIN_DISABLED'] = 'True'


def create_trello_board():
    dbconnect = os.environ['CLIENT']
    client = pymongo.MongoClient(
        dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
    print(client.list_database_names())
    database = client["01"]
    test_collection = database["test_collection"]
    post = {"name": "titleTEST1", "idBoard": "6005828032dafa5707bf5dc3",
            "last_modified": "2021-09-11"}

    test_collection = database["trello_collection"]
    result = test_collection.insert_one(post)
    todo = test_collection.find(
        {'idBoard': '6005828032dafa5707bf5dc3'}, {"name": 1})
    doing = test_collection.find(
        {'idBoard': '6005828032dafa5707bf5dc7'}, {"name": 1})
    done = test_collection.find(
        {'idBoard': '6005828032dafa5707bf5dc5'}, {"name": 1})

    return test_collection
    # return application


def delete_trello_board(board_id):
    dbconnect = os.environ['CLIENT']
    client = pymongo.MongoClient(
        dbconnect, ssl=True, ssl_cert_reqs='CERT_NONE')
    print(client.list_database_names())
    database = client["01"]
    test_collection = database["test_collection"]
    test_collection.collection.drop()

os.environ['LOGIN_DISABLED'] = 'True'


@pytest.fixture(scope='module')
def app_with_temp_board():
    # Create the new board & update the board id environment variable
    os.environ['LOGIN_DISABLED'] = 'True'

    # construct the new application
    file_path = find_dotenv('.env')
    load_dotenv(file_path, override=True)
    application = create_app()
# start the app in its own thread.
    thread = Thread(target=lambda:
                    application.run(use_reloader=False))
    thread.daemon = True
    thread.start()
    time.sleep(1)
    yield application
# Tear Down
    thread.join(1)


@pytest.fixture(scope="module")
def driver():

    # Set proper profile
    profile = webdriver.FirefoxProfile()
    # disable Strict Origin Policy
    profile.set_preference("security.fileuri.strict_origin_policy", False)
    # disable Strict Origin Policy
    profile.set_preference("dom.webdriver.enabled", False)

    # Capabilities
    capabilities = webdriver.DesiredCapabilities.FIREFOX
    capabilities['marionette'] = True

    # Options
    options = webdriver.FirefoxOptions()
    options.add_argument("--log-level=OFF")

    # Using non Headless for debugging
    options.headless = True

    driver = webdriver.Firefox(service_log_path=os.devnull, options=options,
                               capabilities=capabilities, firefox_profile=profile)
    driver.set_window_size(1920, 1080)

    #driver = webdriver.Firefox()
    yield driver
    driver.close()


def test_task_journey(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    assert driver.title == 'To-Do App'


def test_create_new_item(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    create_test_task_input = '//*[@id="title"]'
    create_test_task_submit = '//*[@id="create"]'
    driver.find_element_by_xpath(create_test_task_input).click()
    driver.find_element_by_xpath(
        create_test_task_input).send_keys("titleTEST1")
    driver.find_element_by_xpath(create_test_task_submit).click()


def test_update_to_done_new_item(driver, app_with_temp_board):
    driver.get('http://localhost:5000/')
    submit_update_to_done = '//input[@type = "submit" and @value="Update to done!"]'
    driver.find_element_by_xpath(submit_update_to_done).click()
    undo_completion_input = '//input[@type = "submit" and @value="Return to To do!"]'
    assert driver.find_element_by_xpath(undo_completion_input) != None
