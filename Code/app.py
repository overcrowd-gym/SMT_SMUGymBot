
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

@app.route('/getHourlyData/', methods=['GET'])
def get_hourlydata():
	# query data based on gender, start_hour, end_hour.
	if 'reportDate' in request.args:
		reportDate = (request.args.get('reportDate'))
		hour = Report_hour.query.filter_by(report_date=reportDate).first()
		return jsonify(hour.serialize())
	
	if 'gender' and 'hour' in request.args:
		gender = (request.args.get('gender'))
		hour = Report_hour.query.filter_by(gender=gender).first()
		
	else:
		hours = Report_hour.query.all() 
		return jsonify([h.serialize() for h in hours])

#  allows the user to determine which day (and/or hour) of the week is the busiest, so that they know what is the best timing/day to visit the gym
# "prediction" of whether a particular day of the week and time will be busy (based on historical data)

@app.route('/reporthour', methods=['POST'])
def create_reporthour():

	report_date = request.json['date']
	hour = request.json['hour']
	gender = request.json['gender']
	capacity = request.json['capacity']

	try:
		new_hour = Report_hour(hour=hour,gender=gender,capacity=capacity,report_date = report_date)
		db.session.add(new_hour)
		db.session.commit() 
	
		return jsonify('new hour record {} was created for user {}'.format(hour, gender))

	except Exception as e:
		return (str(e))

@app.route('/visitor', methods=['POST'])
def create_visitor():

	report_date = request.json['date']
	capacity = request.json['capacity']

	try:
		new_day = Visitorship(report_date = report_date,total_capacity=capacity)
		db.session.add(new_day)
		db.session.commit() 
	
		return jsonify('new hour record {} was created for user {}'.format(report_date, capacity))

	except Exception as e:
		return (str(e))

@app.route('/visitorship/<date:date>', methods=['DEL'])
def del_all():
	try:
		# visit = Visitorship.query.delete()
		# db.session.query(Visitorship).delete()
		# db.session.delete(visit)
		visit = Visitorship.query.get(date)
		db.session.delete(visit)
		db.session.commit()
	except:
		db.session.rollback()

	# return jsonify('{} rows was deleted'.format())
 	

# your code ends here 

if __name__ == '__main__':
	app.run(debug=True)

