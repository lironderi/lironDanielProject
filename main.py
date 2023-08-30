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
    if request.method == 'POST':
        item = request.form.get('data-row', placeholder=item)
        quantity = request.form.get('data-row', placeholde=quantity)
        db.items.insert_one({"item": item, "quantity": quantity})
    return render_template('first-list.html')


@app.route('/list', methods=('GET', 'POST'))
def list_page():
    items = [
       
    ]
    return render_template('list.html', items=items)

@app.route('/create-accont')
def create_account():
    return render_template('create-account.html')

@app.route('/login_page')
def login_page():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')

    # Hash the password for security
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    # Insert into MongoDB
    db.users.insert_one({"username": username, "email": email, "password": password})

    return redirect(url_for('home_page'))

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    # Hash the password for comparison
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    # Query MongoDB to find the user
    user = db.users.find_one({"username": username, "password": password})

    if user:
        session['username'] = username  # Add the username to the session
        return redirect(url_for('first_list_page'))
    else:
        # User not found or password did not match
        # Redirect back to login page or show an error
        return "Invalid username or password", 401

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('home_page'))


if __name__ == '__main___':
  app.run(debug=True, host="0.0.0.0")
