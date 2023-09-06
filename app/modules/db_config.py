from pymongo import MongoClient
import os
class RunConfig:
    MONGO_URI=os.environ.get('MONGO_URI')
    try:
        client = MongoClient(MONGO_URI)  
        db = client['Website_db']
        print("mongo connect")
    except Exception:
        print("enable to connect mongodb")
class TestConfig:
    MONGO_URI=os.environ.get('MONGO_URI')
    try:
        client = MongoClient(MONGO_URI)  
        db = client['Test_db']
        print("mongo connect")
    except Exception:
        print("enable to connect mongodb")
    TESTING = True