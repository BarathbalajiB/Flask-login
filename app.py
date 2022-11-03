from functools import wraps
from flask import Flask, flash, render_template, request, url_for, redirect, session
from flask_session import Session
from flask_login import LoginManager, login_manager, login_required, UserMixin, login_user, current_user, logout_user
import bcrypt
import pymongo

app = Flask(__name__)
app.secret_key = 'secretkey'
'''app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
'''
client = pymongo.MongoClient("mongodb+srv://moo1-student:m001-mongodb-basics@sandbox.pmgteep.mongodb.net/?retryWrites=true&w=majority")
db = client.login_users # database name = login_users
#users = db.users_data # collection name = user_data

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'Login_page'

@login_manager.user_loader      
def load_user(name):
    users = db.user_data
    data = users.find_one({'name':name})
    if data:
        return User(name=data['name'],password=data['password'])
    else:
        return None

class User(UserMixin):
    def __init__(self,name=None,password=None):
        self.name = name
        self.password = password

    def get_id(self):
        return self.name

'''def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if 'name' in session:
            return func(*args,**kwargs)
        else:
            return "This is protucted  page You need to login again !"
            #return redirect(url_for('login'))
    return wrap    
'''

@app.route('/', methods=['POST','GET'])
@login_required
def Home():
    return render_template('index.html')


@app.route('/login', methods = ['POST', 'GET'])
def Login_page():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        data = db.users_data.find_one({'name': name})
    
        if data:
            if bcrypt.hashpw(password.encode('utf-8'), data['password']) == data['password']:
                logged_user = User(data['name'], data['password'])
                login_user(logged_user)
                session["name"] = name
                return redirect(url_for('dashboard'))
            
        return 'Invaild username or password'
    return render_template('index.html')


@app.route('/dashboard', methods=['POST','GET'])
def dashboard():
    return render_template('dashboard.html')
    

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        hashpass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = db.users_data
        data = user.find_one({'name': name})

        if data is None :
            user.insert_one({'name': name, 'password': hashpass})
            session['name'] = name
            return redirect(url_for('Home'))
        else:
            return 'user already exist, kindly choose another name!'

    return render_template("register.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.pop('name',None)
    return redirect('Login_page')


if __name__ == "__main__":
    app.run(debug = True, port= 8000) 


'''from http import client
import pymongo 
'''
'''data = {"username": "arun", "password": "arun@123"}
x = db.users_data.insert_one(data)
print(x)
'''




