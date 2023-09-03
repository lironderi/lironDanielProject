from flask import Flask, render_template, request, url_for, redirect, session
from pymongo import MongoClient
import hashlib  # for password hashing
import os

app = Flask(__name__)

app.secret_key = 'fakekey'
MONGO_URI=os.environ.get('MONGO_URI')
#create DB
print(MONGO_URI)
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

#first list to create after registeration
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
            user_items_collection = db[user['_id']]  # Use the user's id as collection name
            user_items_collection.insert_one({"item": item, "quantity": quantity})

    user_items_collection = db[user['_id']]  # Use the user's id as collection name
    items = user_items_collection.find()

    return render_template('first-list.html', user=user, items=items)


#insert items to the DB to a collection called by the user id
@app.route('/save-items', methods=['POST'])
def save_items():
    user = session.get('user')
    if not user:
        return "User not in session", 401

    data = request.json
    items = data.get('items')

    if items:
        user_items_collection = db[user['_id']]  # Use the user's id as collection name
        user_items_collection.insert_many(items)
        session['login_user'] = user
        return redirect(url_for('new_list'))
    else:
        return {"message": "No items provided"}, 400


# create new list when you already have an account
@app.route('/new_list', methods=('GET', 'POST'))
def new_list_page():
    user = session.get('login_user')
    if user:
        user_items_collection = db[user['_id']]  # Use the user's id as collection name
        items = user_items_collection.find()  # Retrieve all items from the collection
        return render_template('new_list.html', items=items)
    else:
        return redirect(url_for('login_page'))
   
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
        session['user'] = user  # Add the username to the session
        return redirect(url_for('first_list_page'))

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
        session['login_user'] = user  # Store the entire user document in the session
        return redirect(url_for('my_list'))
    else:
        return "Invalid username or password", 401
    
# create temporary collection

@app.route('/my_list', methods=['GET'])
def my_list():
    user = session.get('login_user')
    if user:
        user_items_collection = db[user['_id']]  # Use the user's id as collection name
        items = user_items_collection.find()
        return render_template('my_list.html', items=items)
    else:
        # Handle the case where the user is not logged in or does not exist
        return redirect('/login')

@app.route('/temp_col', methods=['POST'])
def temp_col():
    user = session.get('login_user')
    data = request.json
    if user:
        temp_collection_name = f"temp_{user['username']}"  # Use the string ID to create collection name

        print(temp_collection_name)
        if not temp_collection_name in db.list_collection_names():
            temp_collection = db.create_collection(temp_collection_name)
        else:
            temp_collection = db[temp_collection_name]

        items = data.get('items')

        if items:
            documents = [{"item": item["item"], "quantity": item["quantity"]} for item in items]
            temp_collection.insert_many(documents)
            return {"message": "Items added to temporary collection"}
        else:
            return {"message": "No items provided"}, 400
    else:
        return redirect(url_for('login_page'))
    
    # function that taking the user out of the session
@app.route('/logout')
def logout():
    user = session.get('login_user')
    if user:
        temp_collection_name = f"temp_{user['username']}"    
        db.drop_collection(temp_collection_name)  # Delete the temporary collection
    session.pop('login_user', None)
    return redirect(url_for('home_page'))

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host="0.0.0.0", port=port)
