from app import db

class ChordDeptViz(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	deptid = db.Column(db.String(), index=True)
	facultykey = db.Column(db.String())
	facultydata = db.Column(db.String())

# class Faculty(db.Model):
# 	__bind_key__ = 'faculty'
#     id = db.Column(db.Integer, primary_key=True)
#     nickname = db.Column(db.String(64), index=True, unique=True)
#     email = db.Column(db.String(120), index=True, unique=True)