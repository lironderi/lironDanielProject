from flask import Flask, render_template, request, url_for, redirect
from pymongo import MongoClient
from bson import json_util
from bson import ObjectId
app = Flask(__name__)
try:
    client = MongoClient('mongodb://localhost:27017/')  

    db = client['Website_db']
    print("mongo connect")
except Exception:
    print("enable to connect mongodb")

db.users.insert_one({"name": "John", "email": "john@example.com"})

@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def home_page():
    return render_template('index.html')

@app.route('/list', methods=('GET', 'POST'))
def list_page():
    items = [
       
    ]
    return render_template('list.html', items=items)

@app.route('/create-accont')
def create_account():
    return render_template('create-account.html')

if __name__ == '__main___':
  app.run(debug=True, host="0.0.0.0")
