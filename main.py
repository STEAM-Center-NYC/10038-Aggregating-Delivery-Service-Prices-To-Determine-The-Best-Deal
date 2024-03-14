from flask import Flask, render_template, request, redirect, g
import pymysql
import pymysql.cursors
from sf import user, pw

app = Flask(__name__)

def connect_db():
    return pymysql.connect(
        host="10.100.33.60",
        user=f"{user}",
        password=f"{pw}",
        database="frugal_foods",
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

@app.route('/')
def index ():
    return render_template('index.jinja')