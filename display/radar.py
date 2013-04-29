from flask import Flask
import sqlite3
from flask import g

app = Flask(__name__)

DATABASE = '/db/sensors.db'

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
        for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

@app.route('/')
def showall():
    for item in query_db('select * from sonar'):
        print item['x'], 'degrees reads', item['distance'], 'cm'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
