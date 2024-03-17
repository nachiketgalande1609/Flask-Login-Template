# Import necessary modules
from bson import ObjectId
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from pymongo import MongoClient
from models.models import User
import bcrypt
from config import SECRET_KEY, MONGO_URI

# Initialize Flask app
app = Flask("__main__")

# Set secret key for session management
app.secret_key = SECRET_KEY

# Initialize Flask-Login for user authentication
login_manager = LoginManager(app)

# MongoDB connection
client = MongoClient(MONGO_URI)
db = client['my_app']

# Define a User class for Flask-Login
class User(UserMixin):
    def __init__(self, user_id, email=None, username=None):
        self.id = user_id
        self.email = email
        self.username = username

    def get_id(self):
        return str(self.id)
    
# Callback function to reload the user object from the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    # Retrieve user data from MongoDB based on user_id
    user_data = db.users.find_one({'_id': ObjectId(user_id)})
    if user_data:
        # Create a User object with the retrieved username and user_id
        user = User(user_id=user_id, email=user_data['email'], username=user_data['username'])
        return user
    else:
        return None

# Route for the home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for the account page, accessible only to logged-in users
@app.route('/account')
@login_required
def account():
    return render_template('account.html')

# Route for user signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        # Check if the user already exists in the database
        existing_user = db.users.find_one({'email': email})
        if existing_user:
            flash('User already exists', 'error')
            return render_template('signup.html')
        
        # Hash the password before storing it
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        password = hashed_password.decode('utf-8')

        # Create a new user model object
        new_user = User(email, username, password)

        # Insert user data into MongoDB
        db.users.insert_one({
            'email': new_user.email,
            'username': new_user.username,
            'password': new_user.password
        })

        # Since User model doesn't provide an ID, you might need to retrieve it from MongoDB
        user = db.users.find_one({'username': new_user.username})

        # Create a new user object using the retrieved user ID
        user_obj = User(user['_id'], username=new_user.username)

        login_user(user_obj)

        # Redirect to home page
        return redirect(url_for('home'))
    else:
        return render_template("signup.html")

# Route for user login
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check if the user exists in the database
        user_data = db.users.find_one({'username': username})
        
        if bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            # If the user exists and the password is correct, log in the user
            user = User(user_id=str(user_data['_id']), username=user_data['username'])
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'error')
            return render_template('login.html')
    else:
        return render_template('login.html')

# Route for user logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

# Run the Flask app
if __name__=="__main__":
    app.run(debug=True)