from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
from dynaconf import Dynaconf 

app = Flask(__name__)

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

@app.route('/home')
def index ():
    return render_template('index.jinja')

@app.route('/')
def landing ():
    return render_template ('landing.jinja')