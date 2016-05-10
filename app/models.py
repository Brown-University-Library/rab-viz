from app import db

class ChordDeptViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deptid = db.Column(db.String(), index=True)
	legend = db.Column(db.String())
	matrix = db.Column(db.String())

class ChordFacViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	facid = db.Column(db.String(), index=True)
	coauthkey = db.Column(db.String())
	coauthdata = db.Column(db.String())

class ForceFacViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	facid = db.Column(db.String(), index=True)
	nodeuris = db.Column(db.String())
	links = db.Column(db.String())

class ForceDeptViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deptid = db.Column(db.String(), index=True)
	nodeuris = db.Column(db.String())
	links = db.Column(db.String())

class Faculty(db.Model):
	rabid = db.Column(db.String, primary_key=True)
	lastname = db.Column(db.String())
	firstname = db.Column(db.String())
	fullname = db.Column(db.String())
	abbrev = db.Column(db.String())
	title  = db.Column(db.String())
	deptLabel = db.Column(db.String())

class Departments(db.Model):
	rabid = db.Column(db.String, primary_key=True)
	label = db.Column(db.String())

class Affiliations(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	facid = db.Column(db.String(), index=True)
	deptid = db.Column(db.String(), index=True)
	rank = db.Column(db.Integer())

class Coauthors(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	authid = db.Column(db.String(), index=True)
	coauthid = db.Column(db.String(), index=True)
	cnt = db.Column(db.Integer())

class AuthorJson(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	facid = db.Column(db.String(), index=True)
	jsondata = db.Column(db.String())

class ChordViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rabid = db.Column(db.String(), index=True)
	legend = db.Column(db.String())
	matrix = db.Column(db.String())