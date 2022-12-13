import pytest
from flask_login import current_user
from app import create_app, db


@pytest.fixture()
def app():
    app = create_app(config_name='test')

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture
def logined_user(client):
     with client:
            client.post('/auth/register', data={'username': 'test', 'email': 'test@test.com',  'password': '11111111Ab', "confirm_password": '11111111Ab'}, 
                follow_redirects=True)
            client.post('/auth/login', data={'email': 'test@test.com',  'password': '11111111Ab', 'remember': 'y'}, 
                follow_redirects=True)


@pytest.fixture
def create_cat(client, logined_user):
    client.post('/task/category/create', data={'name': 'homework'}, 
                follow_redirects=True)


@pytest.fixture
def create_task(client, logined_user, create_cat):
    data = {
        'title': 'Test task',  
        'description': 'task desc', 
        'deadline': '2022-12-15',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/create', data=data, 
                follow_redirects=True)


def test_setup(client):
    # assert app is not None
    assert client is not None
    

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'About' in response.data


def test_user_register_login(client):
    with client:
            resp = client.post('/auth/register', data={'username': 'test', 'email': 'test@test.com',  'password': '11111111Ab', "confirm_password": '11111111Ab'}, 
                follow_redirects=True)
            assert resp.status_code == 200
            assert 'Login' in resp.get_data(as_text=True)
            resp = client.post('/auth/login', data={'email': 'test@test.com',  'password': '11111111Ab', 'remember': 'y'}, 
                follow_redirects=True)
            assert resp.status_code == 200
            assert current_user.username == "test"
            resp = client.get('/auth/logout', follow_redirects=True)
            assert resp.status_code == 200
            assert current_user.is_anonymous       


# Testing Task model
def test_task_create(client, create_cat):
    data = {
        'title': 'Test task',  
        'description': 'task desc', 
        'deadline': '2022-12-15',
        'priority': 1,
        'progress': 1,
        'category': 1
    }
    resp = client.post('/task/create', data=data, 
                follow_redirects=True)
    
    assert "Task successfully added" in resp.get_data(as_text=True)

def test_list_tasks(client, create_task):
    resp = client.get('/task/', follow_redirects=True)

    assert 'Test task' in resp.get_data(as_text=True)
    assert 'task desc' not in resp.get_data(as_text=True)

def test_detail_task(client, create_task):
    resp = client.get('/task/1', follow_redirects=True)
    assert 'task desc' in resp.get_data(as_text=True)

def test_task_update(client, create_task):
    data = {
        'title': 'Test task2',  
        'description': 'task desc2', 
        'deadline': '2022-12-15',
        'priority': 2,
        'progress': 2,
        'category': 1
    }
    resp = client.post('/task/1/update', data=data, follow_redirects=True)
    assert 'task desc2' in resp.get_data(as_text=True)


def test_task_delete(client, create_task):
    resp = client.post('/task/1/delete', follow_redirects=True)
    assert 'Successfully deleted!' in resp.get_data(as_text=True)
