from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import hashlib  # for password hashing
from bson import json_util
from bson import ObjectId
app = Flask(__name__)

app.secret_key = 'fakekey'

try:
    client = MongoClient('mongodb://localhost:27017/')  
    db = client['Website_db']
    print("mongo connect")
except Exception:
    print("enable to connect mongodb")

@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def home_page():
    return render_template('index.html')

@app.route('/first-list', methods=['GET','POST'])
def first_list_page():
    user = session.get('user')
    if not user:
        return redirect(url_for('register'))
    item = request.form.get('item')
    quantity = request.form.get('quantity')
    if request.method == 'POST':
        # ...
        if item and quantity:
            user_items_collection = db[user['_id']]  # Use the user's username as collection name
            user_items_collection.insert_one({"item": item, "quantity": quantity})

    user_items_collection = db[user['username']]  # Use the user's username as collection name
    items = user_items_collection.find()

    return render_template('first-list.html', user=user, items=items)


@app.route('/save-items', methods=['POST'])
def save_items():
    user = session.get('user')
    if not user:
        return "User not in session", 401

    data = request.json
    items = data.get('items')

    if items:
        user_items_collection = db[user['_id']]  # Use the user's username as collection name
        user_items_collection.insert_many(items)
        return redirect(url_for('new_list'))
    else:
        return {"message": "No items provided"}, 400


@app.route('/new_list', methods=('GET', 'POST'))
def new_list_page():
    return render_template('new_list.html')

@app.route('/create-accont')
def create_account():
    return render_template('create-account.html')



@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')

    # Hash the password for security
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    try:
        db.users.insert_one({"username": username, "email": email, "password": password})
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 400
    
    user = db.users.find_one({"username": username, "password": password})
    if user:
        user['_id'] = str(user['_id'])
        session['user'] = user # Add the username to the session
        return redirect(url_for('first_list_page'))
    else:
        return "Invalid username or password", 401
    # return redirect(url_for('login_page'))

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Hash the password for comparison
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    # Query MongoDB to find the user
    user = db.users.find_one({"username": username, "password": password})

    if user:
        session['username'] = username  # Add the username to the session
        return redirect(url_for('new_list_page'))
    else:
        return "Invalid username or password", 401

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home_page'))


if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0")
