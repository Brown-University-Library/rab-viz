from app import db

class ChordDeptViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deptid = db.Column(db.String(), index=True)
	facultykey = db.Column(db.String())
	facultydata = db.Column(db.String())

class ChordFacViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	facid = db.Column(db.String(), index=True)
	coauthkey = db.Column(db.String())
	coauthdata = db.Column(db.String())

class Faculty(db.Model):
	rabid = db.Column(db.String, primary_key=True)
	shortid = db.Column(db.String())
	firstname = db.Column(db.String())
	lastname = db.Column(db.String())
	fullname = db.Column(db.String())
	nameabbrev = db.Column(db.String())
	preftitle  = db.Column(db.String())
	email = db.Column(db.String())
	primarydept = db.Column(db.String(), index=True)

class Department(db.Model):
	rabid = db.Column(db.String, primary_key=True)
	label = db.Column(db.String())