import sys
import sqlite3
from flask import Flask
from flask import g
from flask import stream_with_context, request, Response, render_template
app = Flask(__name__, static_folder='', static_url_path='')

@app.route("/")
def root():
    return app.send_static_file('index.html')

DATABASE = 'VEarth.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route("/query")
def query():
    def generate():
        for row in query_db('select * from Establishments where BusinessName=?', [request.args['Search']]):
            yield {
                "BusinessName": row["BusinessName"],
                "BusinessType": row["BusinessType"],
                "AddressLine1": row["AddressLine1"],
                "AddressLine2": row["AddressLine2"],
                "PostCode": row["PostCode"],
                "Rating": row["Rating"]
            }

    return render_template("Resultpage.html", results=generate())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    #app.run(debug=True)
    app.run(host='0.0.0.0', port='80', debug=False) #do not enable debug while live!!!. It allows remote code execution.
