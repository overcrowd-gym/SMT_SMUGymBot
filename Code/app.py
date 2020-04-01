
# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json


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
		reportDate = request.args.get('reportDate')
		print(reportDate)
		hours = Report_hour.query.filter_by(report_date=reportDate)
		return jsonify([h.serialize() for h in hours])
	
	if 'gender' in request.args:
		gender = (request.args.get('gender'))
		hours = Report_hour.query.filter_by(gender=gender)
		return jsonify([h.serialize() for h in hours])
	
	if 'start_hour' in request.args:
		start_hour = (request.args.get('start_hour'))
		print(start_hour)
		hours = Report_hour.query.filter_by(hour=start_hour)
		return jsonify([h.serialize() for h in hours])
		
	else:
		hours = Report_hour.query.all() 
		return jsonify([h.serialize() for h in hours])

#  allows the user to determine which day (and/or hour) of the week is the busiest, 
#  so that they know what is the best timing/day to visit the gym
@app.route('/getWeeklyHourly/', methods=['GET']) 
def get_busyday():
	if 'start_date' in request.args and 'end_date' in request.args: 
		#start and end date, return capacity for the week
		start = request.args.get('start_date')
		end = request.args.get('end_date')
		hours = Report_hour.query.filter_by(report_date=reportDate) #between start and end, visitorship!!!
		return jsonify([h.serialize() for h in hours])

	if 'start_date' in request.args and 'end_date' in request.args and 'hour' in request.args:
		# between start and end date, hour -> report_hour
		start = request.args.get('start_date')

# "prediction" of whether a particular day of the week and time will be busy (based on historical data)
@app.route('/getprediction/', methods=['GET']) 
def get_prediction():
	if 'start_date' in request.args and 'end_date' in request.args: # day and time 
		# start_date, end_date and time -> add up female and male 
		# get date where start_date and end_date + max(cap)
		# get hour where date = max(cap) and max(cap) -> M+F
		# select * from report_date where report_date between start and end + max(capacity)

		# return full or empty
		start = request.args.get('start_date')



@app.route('/reporthour', methods=['POST'])
def create_reporthour():

	# report_date = request.json['date']
	# hour = request.json['hour']
	# gender = request.json['gender']
	# capacity = request.json['capacity']
	count=0
	hours = request.json['report_hours']

	try:
		for each in hours:
			report_date = each['report_date']
			hour = each['hour']
			gender = each['gender']
			capacity = each['capacity']
			new_hour = Report_hour(hour=hour,gender=gender,capacity=capacity,report_date = report_date)
			db.session.add(new_hour)
			db.session.commit() 
			count+=1

		return jsonify('{} record added'.format(count))

	except Exception as e:
		return (str(e))

@app.route('/visitor', methods=['POST'])
def create_visitor():
	count = 0 
	visitors = request.json['visitors']
	# report_date = request.json['date']
	# capacity = request.json['capacity']

	try:
		for v in visitors:
			report_date = v['report_date']
			capacity = v['total_capacity']
			new_day = Visitorship(report_date = report_date,total_capacity=capacity)
			db.session.add(new_day)
			db.session.commit()
			count += 1 
	
		return jsonify('{} record added'.format(count))

	except Exception as e:
		return (str(e))

# your code ends here 

if __name__ == '__main__':
	app.run(debug=True)

