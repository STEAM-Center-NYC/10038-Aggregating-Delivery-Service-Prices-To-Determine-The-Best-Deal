from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
import flask_login
from dynaconf import Dynaconf 

app = Flask(__name__)
app.secret_key = "UR7XLL009"

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

settings = Dynaconf(
    settings_file = ('settings.toml')
)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user= settings.db_user,
        password = settings.db_pass,
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
    cursor.execute(f"SELECT * FROM `User` WHERE `id` = {user_id}")
    result = cursor.fetchone()
    cursor.close()
    get_db().commit()

    if result is None:
        return None
    
    return User(result["ID"], result["Username"], result["Email"])

# @app.route('/home', methods=['GET', 'POST'])
# def restaurant_list():
#     cursor = get_db().cursor()
#     cursor.execute("""
#                    SELECT * FROM `restaurant` 
#                    INNER JOIN `items` ON `restaurant`.restaurant_id = `items`.restaurant_id 
#                    INNER JOIN `price` ON `items`.item_id = `price`.item_id
#     """)

@app.route('/home', methods=['GET', 'POST'])
def restaurant_list():
    cursor = get_db().cursor()
    cursor.execute("SELECT * FROM `restaurant`")
    results = cursor.fetchall()
    cursor.close()
    return render_template("index.jinja", restaurants = results)

@app.route('/')
def landing ():
    return render_template ('landing.jinja')