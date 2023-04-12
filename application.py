from flask import Flask, request, render_template, url_for, flash, redirect, session, send_file
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_session import Session
from datetime import date, datetime
import pandas as pd
import openpyxl
import os

app=Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.config['SECRET_KEY']='uOzPG137aJNoq2bBJ4b9P81DY5vCiRxY'

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db_internship00.db'
db=SQLAlchemy(app)


# ===== <ManyToMany> ===== 
enrollments = db.Table('enrollments',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.course_id'), primary_key=True)
)

class Student(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	name=db.Column(db.String(40),nullable=False, unique=True)
	surname=db.Column(db.String(40),nullable=False)
	taxcode=db.Column(db.String(11))

class Course(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	course_id=db.Column(db.String, nullable=False, unique=True)
	course_type=db.Column(db.String)
	course_name=db.Column(db.String)
	date_start=db.Column(db.DateTime)
	date_end=db.Column(db.DateTime)

#OneToMany Company-->Internship
class Internship(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	iflag=db.Column(db.Integer)
	status=db.Column(db.String)
	intern_type=db.Column(db.String,db.ForeignKey('company.company_type'))
	course_id=db.Column(db.String, db.ForeignKey('course.course_id'))
	student_id=db.Column(db.Integer, db.ForeignKey('student.id'))
	date_start=db.Column(db.DateTime)
	date_end=db.Column(db.DateTime)

class Company(db.Model):
	id=db.Column(db.Integer, primary_key=True)
	company_name=db.Column(db.String(45), nullable=False)
	address=db.Column(db.String)
	zone=db.Column(db.String)
	area=db.Column(db.String)
	company_type=db.Column(db.String)
	category=db.Column(db.String)
	intern_max=db.Column(db.Integer)
	intern_free=db.Column(db.Integer)
	intern_busy=db.Column(db.Integer)
	intern_done=db.Column(db.Integer)
	internships=db.relationship('Internship', backref='company')

@app.route('/',methods=['GET','POST'])
def index():
	companies=Company.query.all()
	if request.method == 'POST':
		return render_template('index.html', companies=companies)
	else:
		return render_template('index.html', companies=companies)

@app.route('/api/addcompany', methods=['GET','POST'])
def add_company():
	if request.method=='POST':
		companyname=request.form['companyname']
		companyzone=request.form['companyzone']
		companytype=request.form['companytype']
		if not companyname:
			flash('companyname obbligatorio!')
		elif not companyzone:
			flash('companyzone obbligatoria!')
		elif not companytype:
			flash('companytype obbligatoria!')
		else:
			checkcompany=Company.query.filter_by(company_name=companyname).first()
			if checkcompany:
				flash('Struttura gia'' presente')
			company=Company(
				company_name=companyname,
				zone=companyzone,
				company_type=companytype
				)
			db.session.add(company)
			db.session.commit()
			return redirect(url_for('index'))
		return render_template('newcompany.html') #I land again on newuser page if conditions are not all ok
	else:
		return render_template('newcompany.html')


@app.route('/api/allcompanies', methods=['GET','POST'])
def all_companies():
	companies=Company.query.all()
	return render_template('index.html', companies=companies)
