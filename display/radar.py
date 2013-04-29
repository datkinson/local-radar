from flask import Flask, g
import sqlite3

app = Flask(__name__)

DATABASE = 'db/sensors.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

@app.route('/')
def showall():
    cur = g.db.execute('select * from sonar')
#    for row in cur.fetchall():
#	    print row['distance']
    print cur.fetchall()

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
