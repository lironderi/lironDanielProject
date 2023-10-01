from app.main import app
from modules.db_config import TestConfig
import pytest
from pymongo import MongoClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    rv = client.get('/home')
    assert rv.status_code == 200

def test_about_page(client):
    rv = client.get('/about_page')
    assert rv.status_code == 200


def test_login_page(client):
    """Test if the login page is accessible."""
    response = client.get('/login_page')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_failed_login(client):
    """Test login with wrong credentials."""
    response = client.post('/login', data={'username': 'wrong', 'password': 'wrong'}, follow_redirects=True)
    assert response.status_code == 401

def test_fake_page(client):
    rv = client.get('/fake_page')
    assert rv.status_code == 404


def test_db():
    try:
        db = TestConfig.db
        users = "users"
        db.create_collection(users)
        db.users.insert_one({"name": "test_name", "email": "test@email", "password": 12345})
        assert db.users.find({"name": "test_name"})
    finally:
        db.users.drop()
        client = TestConfig.client
        client.drop_database('Temp_db')
