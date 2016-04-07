from flask import render_template, json

from app import app
from .models import ChordDeptViz, Faculty, Department

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
	all_depts = Department.query.all()
	dept_lookup = { d.rabid: d.label for d in all_depts }
	faculty_lookup = { f.rabid: f.nameabbrev for f in all_faculty }
	newkey = [ [faculty_lookup[facdata[0]], dept_lookup[facdata[1]], facdata[0]]
					for facdata in vizkey ]
	legend = list({ n[1] for n in newkey })
	deptMap = { d.label: d.rabid for d in all_depts }
	deptLabel = dept_lookup[rabid]
	vizdata = json.loads(viz.facultydata)
	return render_template(
			'chord_dept.html', deptLabel=deptLabel, legend=legend,
			deptMap=deptMap, vizkey=newkey, vizdata=vizdata)