from flask import Flask, render_template
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
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/list')
def list_page():
    items = [
        {'id': 1, 'type':'Phone','mark':'869767869', 'price':500},
        {'id': 2, 'type': 'Laptop', 'mark': '764754q34234', 'price': 700},
        {'id': 3, 'type': 'Keyboard', 'mark': '4354545', 'price': 300}
    ]
    return render_template('list.html', items=items)

@app.route('/create-accont')
def create_account():
    return render_template('create-account.html')

if __name__ == '__main___':
  app.run(debug=True, host="0.0.0.0")
