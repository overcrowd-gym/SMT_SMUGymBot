
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
from models import visitorship, report_hour

# Step 05: add routes and their binded functions here

# your code ends here 

if __name__ == '__main__':
	app.run(debug=True)

