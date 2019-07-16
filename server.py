import sys
#import os
import sqlite3
#sys.path.append("./Flask-0.10.1")
#sys.path.append("./Werkzeug-0.9.6")
#sys.path.append("./Jinja2-2.7.3")
#sys.path.append("./MarkupSafe-0.23")
#sys.path.append("./itsdangerous-0.24")
from flask import Flask
from flask import g
from flask import stream_with_context, request, Response, render_template
app = Flask(__name__, static_folder='', static_url_path='')

@app.route("/")
def root():
    return app.send_static_file('index.html')

#DATABASE = '../Data/VEarth.db'
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
    #return os.getcwd()
    #@stream_with_context
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


@app.route("/pins.json")
def get_pins_json():
	@stream_with_context
	def generate():
		# yield '{"type":"GeometryCollection","geometries":['
		# for pin in query_db("select * from Establishments where Latitude like '50.%' and Longitude like '-4%'"):
		# 	yield '{"type":"Point","coordinates":[%s,%s]},' % (pin['Latitude'], pin['Longitude'])
		# yield '{"type":"Point","coordinates":[%s,%s]}' % (pin['Latitude'], pin['Longitude'])
		# yield ']}'

		yield '{"type": "FeatureCollection","features":['
		for pin in query_db("select * from Establishments where Latitude like '50.%' and Longitude like '-4%'"):
		 	yield '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[%s,%s]}},' % (pin['Latitude'], pin['Longitude'])
		yield '{"type":"Feature","properties":{},"geometry":{"type":"Point","coordinates":[%s,%s]}}' % (pin['Latitude'], pin['Longitude'])
		yield ']}'
		# yield '{"type":"Point","coordinates":[%s,%s]}' % (pin['Latitude'], pin['Longitude'])
		# yield ']}'

           # "features": [
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [-81, 42]}},
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [-82, 43]}},
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [-80, 41]}},
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [19, -24]}},
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [4, 42]}},
           #     {"type": "Feature", "properties": {},
           #         "geometry": {"type": "Point", "coordinates": [32, 35]}},
           # ]
	return Response (generate())

	#		yield
	#return Response(generate())

if __name__ == "__main__":
    app.run(debug=True)
