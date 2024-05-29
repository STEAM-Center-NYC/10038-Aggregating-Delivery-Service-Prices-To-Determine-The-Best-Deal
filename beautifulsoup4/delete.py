import pymysql
import pymysql.cursors

db_link = '127.0.0.1'

connection = pymysql.connect(
    database = 'frugal_foods',
    user = 'cvasquez',
    password = '242590909',
    host = db_link,
    cursorclass = pymysql.cursors.DictCursor
)

cursor = connection.cursor()
cursor.execute("DELETE FROM `price`")
connection.commit()
cursor.execute("DELETE FROM `items`")
connection.commit()
cursor.close()