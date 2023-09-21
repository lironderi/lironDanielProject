from flask import Flask, render_template, request, url_for, redirect, session, jsonify
from pymongo import MongoClient
import hashlib 
import os
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'fakekey'
MONGO_URI=os.environ.get('MONGO_URI')
try:
    client = MongoClient(MONGO_URI)  
    db = client['Website_db']
    print("mongo connect")
except Exception:
    print("enable to connect mongodb")


#route to home page
@app.route('/', methods=('GET', 'POST'))
@app.route('/home', methods=('GET', 'POST'))
def home_page():
    return render_template('index.html')


# about page
@app.route('/about_page')
def about_page():
        return render_template('about.html')

# registeration page
@app.route('/create-accont')
def create_account():
    return render_template('create-account.html')


# registeration function!
@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    email = request.form.get('email')

    # Hash the password for security
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    existing_user = db.users.find_one({"username": username})
    if existing_user:
        return render_template('create-account.html', message='Username already exists.')
    # Insert new user into database
    try:
        db.users.insert_one({"username": username, "email": email, "password": password})
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred", 400
    
    # Validate inserted data
    user = db.users.find_one({"username": username, "password": password})
    if user:
        user['_id'] = str(user['_id'])
        session['first_login'] = user  # Add the username to the session
        return redirect(url_for('login_page'))

    return "Invalid username or password", 401


# login page
@app.route('/login_page')
def login_page():
    return render_template('login.html')

# function that check if user exist and create a session
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    
    password = hashlib.sha256(request.form.get('password').encode()).hexdigest()

    
    user = db.users.find_one({"username": username, "password": password})

    if user:
        user['_id'] = str(user['_id'])  # Convert ObjectId to string
        if user['_id'] in db.list_collection_names():
            session['login_user'] = user  
        else: 
            session['first_login'] = user
        return redirect(url_for('new_list_page'))
    else:
        return "Invalid username or password", 401


@app.route('/new_list', methods=('GET', 'POST'))
def new_list_page():
    user = session.get('login_user')
    first = session.get('first_login')
    if first:
        if request.method == 'POST':
            return redirect(url_for('my_list'))  
        user_items_collection = db[first['_id']] 
        items = user_items_collection.find() 
        return render_template('new_list.html', user=first, items=items)
    elif user:
        if request.method == 'POST':
            return redirect(url_for('my_list'))  
        user_items_collection = db[user['_id']]  
        items = user_items_collection.find()
        return render_template('new_list.html', user=user, items=items)
    else:
        return redirect(url_for('login_page'))
    
    
# create temporary collection

@app.route('/my_list', methods=['GET'])
def my_list():
    user = session.get('login_user')
    first = session.get('first_login')
    if first:
        user_items_collection = db[first['_id']]  # Use the user's id as collection name
        items = user_items_collection.find()
        return render_template('my_list.html', items=items)
    elif user:
        user_items_collection = db[user['_id']]  # Use the user's id as collection name
        items = user_items_collection.find()
        return render_template('my_list.html', items=items)
    else:
        # Handle the case where the user is not logged in or does not exist
        return redirect('/login')


@app.route('/get-items', methods=['GET'])
def get_items():
    user = session.get('login_user')
    first = session.get('first_login')
    if first:
        user_items_collection = db[first['_id']]
        items = list(user_items_collection.find())
        # Convert ObjectId to string
        for item in items:
            item['_id'] = str(item['_id'])
        return jsonify(items)
    elif user:
        user_items_collection = db[user['_id']]
        items = list(user_items_collection.find())
        # Convert ObjectId to string
        for item in items:
            item['_id'] = str(item['_id'])
        return jsonify(items)
    else:
        return jsonify([]), 401


#insert items to the DB to a collection called by the user id
@app.route('/save-items', methods=['POST'])
def save_items():
    first = session.get('first_login')
    login_user = session.get('login_user')
    
    if first:
        data = request.json
        items = data.get('items')
        if items:
            user_items_collection = db[first['_id']]
            user_items_collection.insert_many(items)
            session.pop('first_login')
            session['login_user'] = first
            return redirect(url_for('my_list'))
        
    elif login_user:
        data = request.json
        current_items = list(db[login_user['_id']].find())
        items = data.get('items')
        if items:
            user_items_collection = db[login_user['_id']]
            if current_items:
                db.drop_collection(user_items_collection)
                user_items_collection = db[login_user['_id']]
                user_items_collection.insert_many(current_items)
            user_items_collection.insert_many(items)
            return redirect(url_for('my_list'))
    
    return "Something went wrong"


@app.route('/delete_item/<string:rowId>', methods=['DELETE'])
def delete_item(rowId):
    user = session.get('login_user')
    if user :
        collection = db[user['_id']]
        collection.delete_one({'_id':ObjectId(rowId)})
        return "deleted"
    else:
        return "not deleted"

# function that taking the user out of the session
@app.route('/logout')
def logout():
    user = session.get('login_user')
    if user:
        session.pop('login_user', None)
    return redirect(url_for('home_page'))


@app.route('/create_list')
def create_list():
    return render_template('create_list.html')

def create_app(app):
    if __name__ == '_main_':
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host="0.0.0.0", port=port)
