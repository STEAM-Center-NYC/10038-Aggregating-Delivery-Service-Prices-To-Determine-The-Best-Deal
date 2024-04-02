from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
import flask_login
from dynaconf import Dynaconf 
from argon2 import PasswordHasher





settings = Dynaconf(
    settings_file = ('settings.toml')
)

app = Flask(__name__)
app.secret_key = settings.app_key
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    def get_id(self):
        return str(self.id)

def connect_db():
    return pymysql.connect(
        host="127.0.0.1",
        user= settings.db_user,
        password = str(settings.db_pass),
        database=settings.db_name,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():
    '''Opens a new database connection per request.'''        
    if not hasattr(g, 'db'):
        g.db = connect_db()
    return g.db

@app.teardown_appcontext
def close_db(error):
    '''Closes the database connection at the end of request.'''    
    if hasattr(g, 'db'):
        g.db.close()

@login_manager.user_loader
def load_user(user_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `users` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

    if result is None:
        return None
    
    return User(result["id"], result["username"], result["email"])

@app.route('/home', methods=['GET', 'POST'])
def restaurant_list():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `restaurant`")
    results = cursor.fetchall()
    cursor.close()
    # user_login = flask_login.current_user.username
    return render_template("index.jinja", restaurants = results)

@app.route('/')
def landing ():
    return render_template ('landing.jinja')


@app.route('/restaurant/<restaurant_id>', methods=['GET', 'POST'])
def restaurant(restaurant_id):
    cursor = get_db().cursor()
    cursor.execute(f"SELECT * FROM `restaurant` WHERE `restaurant_id` = {restaurant_id}")
    restaurant_results = cursor.fetchone()
    cursor.execute(f"SELECT * FROM `items` INNER JOIN `price` ON `items`.item_id = `price`.item_id WHERE `restaurant_id` = {restaurant_id}")
    itemprice_results = cursor.fetchall()
    return render_template("restaurant.jinja", restaurant_data = restaurant_results, itemprice = itemprice_results)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        new_username = request.form['new_username']
        new_password = request.form['new_password']
        new_email = request.form['new_email']
        cursor = get_db().cursor()
        cursor.execute(f'INSERT INTO `users` (`username`, `password`, `email`) VALUES ("{new_username}", "{new_password}", "{new_email}");')
        cursor.close()
        get_db().commit()
        return redirect('/login')
    return render_template('signup.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        cursor = get_db().cursor()
        cursor.execute(f'SELECT * FROM `users` WHERE `username` = "{username}"')
        result = cursor.fetchone()
        if password == result['password']:
            user = load_user(result['id'])
            flask_login.login_user(user)
            return redirect('/home')
    return render_template('login.jinja')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect('/')