from flask import Flask, render_template
#from flaskext.mysql import MySQL
#from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
#app.config['MYSQL_DATABASE_USER'] = 'root'
#app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
#app.config['MYSQL_DATABASE_DB'] = 'EmpData'
#app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#app.config['MYSQL_DATABASE_URI'] = 'mysql://list.db'
#db = MySQL(app)
#db.init_app(app)

#class Item(db.Model):
   # id = db.Column(db.Integer(), primary_key=True)
   # item = db.Column(db.Integer(), nullable=False)
   # type = db.Column(db.String(length=30), nullable=False, unique=True)
   # quantity = db.Column(db.Integer(), nullable=False)

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
if __name__ == '__main___':
    app.run()
