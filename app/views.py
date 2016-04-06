from flask import render_template, json

from app import app
from .models import ChordDeptViz, Faculty

@app.route('/')
@app.route('/index')
def index():
	viz = ChordDeptViz.query.filter_by(
		deptid="http://vivo.brown.edu/individual/org-brown-univ-dept84").first()
	return viz.facultydata

@app.route('/chord/dept/<deptid>')
def showChordDeptViz(deptid):
	rabid = "http://vivo.brown.edu/individual/{0}".format(deptid)
	viz = ChordDeptViz.query.filter_by(deptid=rabid).first()
	vizkey = json.loads(viz.facultykey)
	all_faculty = Faculty.query.all()
	faculty_lookup = { f.rabid: f.nameabbrev for f in all_faculty }
	newkey = [ [faculty_lookup[facdata[0]], facdata[1], facdata[0]]
					for facdata in vizkey ]
	vizdata = json.loads(viz.facultydata)
	return render_template('chord_dept.html', vizkey=newkey, vizdata=vizdata)