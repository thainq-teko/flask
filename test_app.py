import pytest
from flask import json
import main


@pytest.fixture
def app():
    app = main.create_app()
    app.debug = True
    return app.test_client()


def test_get_home(app):
    res = app.get("/")
    assert res.status_code == 200
    assert "Hello, flask app works ! - Thainq" in res.data


def test_register(app):
    res = app.post('/register',
                   data=json.dumps({"username": "abc", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 200


def test_register_1(app):
    res = app.post('/register',
                   data=json.dumps({"username": "thainq05", "password": "1234", "email": "thainq00@gmail.com"}),
                   content_type='application/json')
    assert res.status_code == 200


def test_login(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq00", "password": "1"}),
        content_type='application/json'
    )
    data = res.get_json()
    assert res.status_code == 200
    assert data.get('code') == 200
    assert data.get('message') == 'login success'


def test_login_2(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01", "password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_3(app):
    res = app.post(
        '/login',
        data=json.dumps({"password": "123456"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_4(app):
    res = app.post(
        '/login',
        data=json.dumps({"username": "thainq01"}),
        content_type='application/json'
    )
    assert res.status_code == 400


def test_login_5(app):
    res = app.post(
        '/login',
        data=json.dumps({}),
        content_type='application/json'
    )
    assert res.status_code == 400
