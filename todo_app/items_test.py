
from todo_app.data.ViewModel import ViewModel
from datetime import date, timedelta
from flask import Flask, request, render_template, redirect, url_for
import pytest
import requests
import os
from todo_app.data.ToDo import ToDo

# test to do list


def test_recent_done_items():

    to_do_items = []
    doing_items = []

    today_string = date.today().strftime('%Y-%m-%d')
    yesterday = (date.today() - timedelta(days=1))
    yesterday_string = yesterday.strftime('%Y-%m-%d')
    done_items = [
        ToDo('id', 'name', today_string), ToDo('id', 'name', yesterday_string),
    ]

    view_model = ViewModel(to_do_items, doing_items, done_items)
    today_item = view_model.recent_done_items()

    assert len(today_item) == 1

    # test suggested by  @JackMead


def test_show_all_done_items_true_if_1_done_item():
    to_do_items = []
    doing_items = []
    done_items = [
        ToDo('id', 'name', date.today()),
    ]
    view_model = ViewModel(to_do_items, doing_items, done_items)

    assert view_model.show_all_done_items() == True
