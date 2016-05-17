from flask import render_template, json

from app import app
from .models import ChordViz, ForceViz, Faculty, Departments
# @app.route('/')
# @app.route('/index')
# def index():
# 	viz = ChordDeptViz.query.filter_by(
# 		deptid="http://vivo.brown.edu/individual/org-brown-univ-dept84").first()
# 	return viz.facultydata

# @app.route('/chord/dept/<deptid>')
# def showChordDeptViz(deptid):
# 	rabid = "http://vivo.brown.edu/individual/{0}".format(deptid)
# 	viz = ChordDeptViz.query.filter_by(deptid=rabid).first()
# 	vizkey = json.loads(viz.facultykey)
# 	all_faculty = Faculty.query.all()
# 	all_depts = Department.query.all()
# 	dept_lookup = { d.rabid: d.label for d in all_depts }
# 	faculty_lookup = { f.rabid: f.nameabbrev for f in all_faculty }
# 	newkey = [ [faculty_lookup[facdata[0]], dept_lookup[facdata[1]], facdata[0]]
# 					for facdata in vizkey ]
# 	legend = list({ n[1] for n in newkey })
# 	deptMap = { d.label: d.rabid for d in all_depts }
# 	deptLabel = dept_lookup[rabid]
# 	vizdata = json.loads(viz.facultydata)
# 	return render_template(
# 			'chord_dept.html', deptLabel=deptLabel, legend=legend,
# 			deptMap=deptMap, vizkey=newkey, vizdata=vizdata)

# @app.route('/chord/faculty/<facid>')
# def showChordFacViz(facid):
# 	rabid = "http://vivo.brown.edu/individual/{0}".format(facid)
# 	print facid
# 	print rabid
# 	viz = ChordFacViz.query.filter_by(facid=rabid).first()
# 	vizkey = json.loads(viz.coauthkey)
# 	all_faculty = Faculty.query.all()
# 	all_depts = Department.query.all()
# 	dept_lookup = { d.rabid: d.label for d in all_depts }
# 	faculty_lookup = { f.rabid: [f.primarydept, f.nameabbrev, f.fullname] for f in all_faculty }
# 	newkey = [ [faculty_lookup[uri][1], dept_lookup[faculty_lookup[uri][0]], uri]
# 					for uri in vizkey ]
# 	legend = list({ n[1] for n in newkey })
# 	deptMap = { d.label: d.rabid for d in all_depts }
# 	fullname = faculty_lookup[rabid][2]
# 	vizdata = json.loads(viz.coauthdata)
# 	return render_template(
# 			'chord_dept.html', deptLabel=fullname, legend=legend,
# 			deptMap=deptMap, vizkey=newkey, vizdata=vizdata)

# @app.route('/force/dept/<deptid>')
# def showForceDeptViz(deptid):
# 	rabid = "http://vivo.brown.edu/individual/{0}".format(deptid)
# 	viz = ForceDeptViz.query.filter_by(deptid=rabid).first()
# 	vizkey = json.loads(viz.nodeuris)
# 	all_faculty = Faculty.query.all()
# 	all_depts = Department.query.all()
# 	dept_lookup = { d.rabid: d.label for d in all_depts }
# 	faculty_lookup = { f.rabid: [f.primarydept, f.nameabbrev, f.fullname] for f in all_faculty }
# 	newkey = [ [faculty_lookup[uri][1], dept_lookup[faculty_lookup[uri][0]], uri]
# 					for uri in vizkey ]
# 	nodes = [ {	"name": faculty_lookup[uri][1],
# 				"group": dept_lookup[faculty_lookup[uri][0]] }
# 					for uri in vizkey ]
# 	legend = list({ n["group"] for n in nodes })
# 	deptMap = { d.label: d.rabid for d in all_depts }
# 	facMap = { f.nameabbrev: f.rabid for f in all_faculty if f.rabid in vizkey }
# 	fullname = dept_lookup[rabid]
# 	links = json.loads(viz.links)
# 	vizdata = {"nodes": nodes, "links": links}
# 	return render_template(
# 			'force.html', deptLabel=fullname, legend=legend,
# 			deptMap=deptMap, facMap=facMap, vizdata=vizdata,
# 			linkDist=20, repel=-200)

# @app.route('/force/faculty/<facid>')
# def showForceFacViz(facid):
# 	rabid = "http://vivo.brown.edu/individual/{0}".format(facid)
# 	viz = ForceFacViz.query.filter_by(facid=rabid).first()
# 	vizkey = json.loads(viz.nodeuris)
# 	all_faculty = Faculty.query.all()
# 	all_depts = Department.query.all()
# 	dept_lookup = { d.rabid: d.label for d in all_depts }
# 	faculty_lookup = { f.rabid: [f.primarydept, f.nameabbrev, f.fullname] for f in all_faculty }
# 	newkey = [ [faculty_lookup[uri][1], dept_lookup[faculty_lookup[uri][0]], uri]
# 					for uri in vizkey ]
# 	nodes = [ {	"name": faculty_lookup[uri][1],
# 				"group": dept_lookup[faculty_lookup[uri][0]] }
# 					for uri in vizkey ]
# 	legend = list({ n["group"] for n in nodes })
# 	deptMap = { d.label: d.rabid for d in all_depts }
# 	facMap = { f.nameabbrev: f.rabid for f in all_faculty if f.rabid in vizkey }
# 	fullname = faculty_lookup[rabid][2]
# 	links = json.loads(viz.links)
# 	vizdata = {"nodes": nodes, "links": links}
# 	return render_template(
# 			'force.html', deptLabel=fullname, legend=legend,
# 			deptMap=deptMap, facMap=facMap, vizdata=vizdata,
# 			linkDist=40, repel=-1200)

@app.route('/chord/<viztype>/<rabid>')
def chordViz(viztype, rabid):
	rabid = "http://vivo.brown.edu/individual/{0}".format(rabid)
	vizData = ChordViz.query.filter_by(rabid=rabid).first()
	legend = json.loads(vizData.legend)
	matrix = json.loads(vizData.matrix)
	allFaculty = Faculty.query.all()
	allDepts = Departments.query.all()
	facultyLookup = { f.rabid: [f.abbrev, f.deptLabel, f.rabid] for f in allFaculty }
	facultyList = [ facultyLookup[f] for f in legend ]
	deptList = list({ f[1] for f in facultyList })
	deptMap = { l: d.rabid for l in deptList for d in allDepts if l in json.loads(d.useFor)  }
	if viztype=='dept':
		pageLabel = [ d.label for d in allDepts if d.rabid == rabid ][0]
	elif viztype=='faculty':
		pageLabel = [ f.fullname for f in allFaculty if f.rabid == rabid ][0]
	return render_template(
			'chord.html', pageLabel=pageLabel, legend=deptList,
			deptMap=deptMap, vizkey=facultyList, vizdata=matrix)

@app.route('/force/<viztype>/<rabid>')
def forceViz(viztype, rabid):
	rabid = "http://vivo.brown.edu/individual/{0}".format(rabid)
	vizData = ForceViz.query.filter_by(rabid=rabid).first()
	legend = json.loads(vizData.legend)
	allFaculty = Faculty.query.all()
	allDepts = Departments.query.all()
	facultyLookup = { f.rabid: [f.abbrev, f.deptLabel, f.rabid] for f in allFaculty }
	nodes = [ {	"name": facultyLookup[uri][0],
				"group": facultyLookup[uri][1] }
					for uri in legend ]
	links = json.loads(vizData.links)
	deptList = list({ n["group"] for n in nodes })
	deptMap = { l: d.rabid for l in deptList for d in allDepts if l in json.loads(d.useFor)  }
	facMap = { f.abbrev: f.rabid for f in allFaculty if f.rabid in legend }
	vizdata = {"nodes": nodes, "links": links}
	if viztype=='dept':
		pageLabel = [ d.label for d in allDepts if d.rabid == rabid ][0]
	elif viztype=='faculty':
		pageLabel = [ f.fullname for f in allFaculty if f.rabid == rabid ][0]
	return render_template(
			'force.html', pageLabel=pageLabel, legend=deptList,
			deptMap=deptMap, facMap=facMap, vizdata=vizdata,
			linkDist=40, repel=-1200)