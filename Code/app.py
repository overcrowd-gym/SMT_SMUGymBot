
# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy


# Step 02: initialize flask app here 
app = Flask(__name__)
app.debug = True


# Step 03: add database configurations here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smugymuser:888000@localhost:5432/smugym'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Step 04: import models
from models import Visitorship, Report_hour

# Step 05: add routes and their binded functions here
@app.route('/getVisitorship', methods=['GET'])
def get_visitorship():
	if 'reportDate' in request.args:
		reportDate = (request.args.get('reportDate'))
		cap = Visitorship.query.filter_by(report_date=reportDate).first()
		return jsonify(cap.serialize())
	else:
		caps = Visitorship.query.all() 
		return jsonify([c.serialize() for c in caps])	

@app.route('/getHourlyData', methods=['GET'])
def get_menu():
	if 'reportDate' in request.args:
		reportDate = (request.args.get('reportDate'))
		hour = Report_hour.query.filter_by(report_date=reportDate).first()
		return jsonify(hour.serialize())
	else:
		hours = Report_hour.query.all() 
		return jsonify([h.serialize() for h in hours])	

# your code ends here 

if __name__ == '__main__':
	app.run(debug=True)

