from datetime import datetime

from app import db
from sqlalchemy.dialects.postgresql import TIME
import datetime
from sqlalchemy.types import TypeDecorator, TIMESTAMP


class Visitorship(db.Model):
	__tablename__ = 'visitorship'

	id = db.Column(db.Integer, primary_key=True) 
	report_date = db.Column(db.Date, unique=True)
	total_capacity = db.Column(db.Integer(), nullable=False)

	# ONE-to-MANY relationship model - Each visitor may have multiple report hour; each report hour is tagged to only one visitor.
	visit_hour = db.relationship('Report_hour', back_populates='hour_per_visitor', uselist=True, cascade='all, delete-orphan', lazy=True)


	def __init__(self, report_date, total_capacity, visit_hour=None):
		self.report_date = report_date
		self.total_capacity = total_capacity
		self.visit_hour = [] if visit_hour is None else visit_hour

	def serialize(self):
		return {
			'reportDate': self.report_date.strftime('%d-%m-%y'), 
			'totalCapacity': self.total_capacity,
			'response':[{"gender":v.gender, "capacity":v.capacity, "hour": v.hour.strftime('%H:%M')} for v in self.visit_hour]
		}



class Report_hour(db.Model):
	__tablename__ = 'report_hour'

	# date = db.Column(db.DateTime, primary_key=True)
	id = db.Column(db.Integer, primary_key=True) 
	hour = db.Column(db.Time, nullable=False)
	gender = db.Column(db.String(1), nullable=False)
	capacity = db.Column(db.Integer, nullable=False)

	report_date = db.Column(db.Date, db.ForeignKey('visitorship.report_date'), nullable=False)

	hour_per_visitor = db.relationship('Visitorship', back_populates='visit_hour')

	# put this within the Review class
	def __init__(self, report_date, hour, gender, capacity):
		self.report_date = report_date
		self.hour = hour
		self.gender = gender
		self.capacity = capacity 

	def serialize(self): #not sure if this is right
			return {
				'reportDate': self.report_date.strftime('%d-%m-%y'),
				'hour': self.hour.strftime('%H:%M'),
				'gender': self.gender,
				'capacity': self.capacity
			}
	



