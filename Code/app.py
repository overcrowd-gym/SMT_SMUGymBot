
# Step 01: import necessary libraries/modules
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import datetime
import json
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.sql import extract
from sqlalchemy.sql import func
from statistics import mean

# Step 02: initialize flask app here 
app = Flask(__name__)
app.debug = True

# Step 03: add database configurations here
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smugymuser:888000@localhost:5432/smugym'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine('postgresql://smugymuser:888000@localhost:5432/smugym')
Session = sessionmaker(bind = engine)
session = Session()

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
	if 'reportDate' in request.args:
		reportDate = (request.args.get('reportDate'))
		cap = Visitorship.query.filter_by(report_date=reportDate).first()
		return jsonify(cap.serialize_whour())
	
	# elif 'gender' in request.args:
	# 	gender = request.args.get('gender')
	# 	print(gender)
	# 	recordObject = {}
	# 	# User.query.join(Skill).filter(Skill.skill == skill_name)
	# 	caps = db.session.query(Visitorship).join(Report_hour).filter(Report_hour.gender==gender).all()
	# 	return jsonify([c.serialize_whour() for c in caps])
	
	else:
		caps = Visitorship.query.all() 
		return jsonify([c.serialize_whour() for c in caps])


@app.route('/getHourwquery/', methods=['GET'])
def get_hourlydatav2():
	# query data based on gender, start_hour, end_hour.

	if 'reportDate' in request.args and 'gender' in request.args and 'start_hour' in request.args and 'end_hour' in request.args:
		reportDate = request.args.get('reportDate')
		gender = request.args.get('gender')
		start_hour = request.args.get('start_hour')
		end_hour = request.args.get('end_hour')
		hours = Report_hour.query.filter(Report_hour.report_date==reportDate).filter(Report_hour.gender==gender).filter(Report_hour.hour.between(start_hour,end_hour))
		return jsonify([h.serialize() for h in hours])

	if 'reportDate' in request.args and 'gender' in request.args and 'start_hour' in request.args:
		reportDate = request.args.get('reportDate')
		gender = request.args.get('gender')
		start_hour = request.args.get('start_hour')
		hours = Report_hour.query.filter(Report_hour.report_date==reportDate).filter(Report_hour.gender==gender).filter(Report_hour.hour==start_hour)
		return jsonify([h.serialize() for h in hours])
	
	if 'reportDate' in request.args and 'start_hour' in request.args and 'end_hour' in request.args:
		reportDate = request.args.get('reportDate')
		start_hour = request.args.get('start_hour')
		end_hour = request.args.get('end_hour')
		hours = Report_hour.query.filter(Report_hour.report_date==reportDate).filter(Report_hour.hour.between(start_hour,end_hour))
		return jsonify([h.serialize() for h in hours])
	
	if 'gender' in request.args and 'start_hour' in request.args and 'end_hour' in request.args:
		gender = request.args.get('gender')
		start_hour = request.args.get('start_hour')
		end_hour = request.args.get('end_hour')
		hours = Report_hour.query.filter(Report_hour.gender==gender).filter(Report_hour.hour.between(start_hour,end_hour))
		return jsonify([h.serialize() for h in hours])

	if 'reportDate' in request.args and 'gender' in request.args:
		reportDate = request.args.get('reportDate')
		gender = request.args.get('gender')
		hours = Report_hour.query.filter(Report_hour.report_date==reportDate).filter(Report_hour.gender==gender)
		return jsonify([h.serialize() for h in hours])

	if 'reportDate' in request.args and 'start_hour' in request.args:
		reportDate = request.args.get('reportDate')
		start_hour = request.args.get('start_hour')
		hours = Report_hour.query.filter(Report_hour.report_date==reportDate).filter(Report_hour.hour==start_hour)
		return jsonify([h.serialize() for h in hours])
		
	if 'gender' in request.args and 'start_hour' in request.args:
		start_hour = request.args.get('start_hour')
		gender = request.args.get('gender')
		hours = Report_hour.query.filter(Report_hour.gender==gender).filter(Report_hour.hour.between(start_hour,end_hour))
		return jsonify([h.serialize() for h in hours])

	if 'start_hour' in request.args and 'end_hour' in request.args:
		start_hour = request.args.get('start_hour')
		end_hour = request.args.get('end_hour')
		hours = Report_hour.query.filter(Report_hour.hour.between(start_hour,end_hour))
		return jsonify([h.serialize() for h in hours])

	elif 'reportDate' in request.args:
		reportDate = request.args.get('reportDate')
		print(reportDate)
		hours = Report_hour.query.filter_by(report_date=reportDate)
		return jsonify([h.serialize() for h in hours])
	
	elif 'gender' in request.args:
		gender = (request.args.get('gender'))
		hours = Report_hour.query.filter_by(gender=gender)
		return jsonify([h.serialize() for h in hours])
	
	elif 'start_hour' in request.args:
		start_hour = (request.args.get('start_hour'))
		print(start_hour)
		hours = Report_hour.query.filter_by(hour=start_hour)
		return jsonify([h.serialize() for h in hours])
		
	else:
		hours = Report_hour.query.all() 
		return jsonify([h.serialize() for h in hours])

#  allows the user to determine which day (and/or hour) of the week is the busiest, 
#  so that they know what is the best timing/day to visit the gym
@app.route('/getWeekData/', methods=['GET']) 
def get_weekdata():

	# show hour of the week
	if 'start_date' in request.args and 'end_date' in request.args and 'start_hour' in request.args:
		# between start and end date, hour -> report_hour
		start_hour = request.args.get('start_hour')
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')
		hours = Report_hour.query.filter(Report_hour.hour==start_hour).filter(Report_hour.report_date.between(start_date,end_date))
		return jsonify([h.serialize() for h in hours])

	# show the capacity of day of the week
	elif 'start_date' in request.args and 'end_date' in request.args: 
		#start and end date, return capacity for the week
		start_date = request.args.get('start_date')
		end_date = request.args.get('end_date')
		visitors = Visitorship.query.filter(Visitorship.report_date.between(start_date,end_date)) #between start and end, visitorship!!!
		return jsonify([v.serialize() for v in visitors])

	# show capacity of day and hour of the week
	elif 'start_date_time' in request.args and 'start_date_time' in request.args: 
		start_date = request.args.get('start_date_time')
		end_date = request.args.get('end_date_time')
		hours = Report_hour.query.filter(Report_hour.report_date.between(start_date,end_date))
		return jsonify([h.serialize() for h in hours])


# "prediction" of whether a particular day of the week and time will be busy (based on historical data)
@app.route('/getprediction/', methods=['GET']) 
def get_prediction():
	result = {}
	weekday_num = request.args['weekday_num']
	time = request.args['time']

	if 'num_limit' in request.args:
		num_limit = int(request.args['num_limit'])
	else:
		num_limit = 25

	# visits = Report_hour.query.filter(Report_hour.hour==time).filter(extract('dow',Report_hour.report_date)==weekday_num)
	visits = Report_hour.query.with_entities(func.sum(Report_hour.capacity).label("sum")).filter(Report_hour.hour==time).filter(extract('dow',Report_hour.report_date)==weekday_num).group_by(Report_hour.report_date)

	visit_list = [visit.sum for visit in visits]
	avg_visit = round(mean(visit_list))
	print(avg_visit)
	result["average"] = avg_visit

	if avg_visit < num_limit:
		result["status"] = "empty"
	else:
		result["status"] = "busy"

	return jsonify(result)

#------------------------------------ ADD DATA INTO DB --------------------------------------#
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

