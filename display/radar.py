from flask import Flask, g, jsonify, render_template
import sqlite3

app = Flask(__name__)

DATABASE = 'db/sensors.db'

output = ""

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

@app.route('/')
def showall():
    g.db.row_factory = dict_factory
    cur = g.db.cursor()
    cur.execute("select * from sonar")
    return render_template("sonar.html", readings = cur.fetchall())

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
