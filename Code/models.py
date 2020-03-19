import datetime

from app import db


class Visitorship(db.Model):
	__tablename__ = 'visitorship'

	report_date = db.Column(db.Date, primary_key=True)
	total_capacity = db.Column(db.Integer(), nullable=False)

	# ONE-to-MANY relationship model - Each visitor may have multiple report hour; each report hour is tagged to only one visitor.
	visit_hour = db.relationship('report_hour', back_populates='hour_per_visitor', uselist=True, cascade='all, delete-orphan', lazy=True)
	
	def __init__(self, report_date, total_capacity):
		self.report_date = report_date
		self.total_capacity = total_capacity


	def serialize(self):
		return {
			'reportDate': self.report_date, 
			'totalCapacity': self.total_capacity,
		}


class Report_hour(db.Model):
	__tablename__ = 'report_hour'

	# hour have to use datetime format first then trancate the time after that
	datetime = db.Column(db.DateTime, primary_key=True)
	#hour = db.Column(db.DateTime, primary_key=True)
	gender = db.Column(db.String(80), primary_key=True)
	capacity = db.Column(db.Integer, unique=False, nullable=False)

	hour_per_visitor = db.relationship('visitorship', back_populates='visit_hour')

	# put this within the Review class
	def __init__(self, datetime, gender, capacity):
		self.date = datetime
		self.gender = gender
		self.capacity = capacity 

	def serialize(self): #not sure if this is right
			return {
				'reportDate': self.report_date, 
				'response': [
					{
						"gender": self.gender,
						"capacity": self.capacity
					}
				]
			}



