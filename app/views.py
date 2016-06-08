from flask import render_template, json

from app import app
from .models import ChordViz, ForceViz, Faculty, Departments

from collections import defaultdict

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/chord/<viztype>/<rabid>')
@app.route('/chord/<viztype>/<rabid>/<page>')
def chordViz(viztype, rabid, page=0):
	rabid = "http://vivo.brown.edu/individual/{0}".format(rabid)
	vizData = ChordViz.query.filter_by(rabid=rabid, page=page).first()
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

@app.route('/<graphtype>')
@app.route('/<graphtype>/')
def forceIndex(graphtype):
	if graphtype == "force":
		allViz = ForceViz.query.all()
		urlbase = "http://localhost:8000/force/"
		pageTitle = "Force Graph"
	elif graphtype == "chord":
		allViz = ChordViz.query.all()
		urlbase = "http://localhost:8000/chord/"
		pageTitle = "Chord Graph"
	forceFac = [ f.rabid for f in allViz if 'org-brown' not in f.rabid]
	faculty = Faculty.query.filter(Faculty.rabid.in_(forceFac)).all()
	forceDept = [f.rabid for f in allViz if 'org-brown' in f.rabid]
	depts = Departments.query.filter(Departments.rabid.in_(forceDept)).all()
	alphaFac = defaultdict(list)
	for f in faculty:
		graphurl = urlbase + "faculty/" + f.rabid[33:]
		alphaFac[f.fullname[0].upper()].append({"graphurl":graphurl, "name":f.fullname})
	sortedFac = { k: sorted(v, key=lambda fac: fac["name"]) for k,v in alphaFac.items() }
	for k, l in sortedFac.items():
		sortedFac[k] = [ l[i:i+20] for i in range(0, len(l), 20) ]
	sortedDepts = sorted([ { "graphurl": urlbase + "dept/"+d.rabid[33:],
					"name":d.label } for d in depts ], key=lambda dept: dept["name"])
	chunkedDepts = [ sortedDepts[i:i+20] for i in range(0, len(sortedDepts), 20) ]
	return render_template('force_index.html', pageTitle=pageTitle,
							faculty=sortedFac, depts=chunkedDepts)

@app.route('/force/<viztype>/<rabid>')
@app.route('/force/<viztype>/<rabid>/<page>')
def indexPage(viztype, rabid, page=0):
	rabid = "http://vivo.brown.edu/individual/{0}".format(rabid)
	vizData = ForceViz.query.filter_by(rabid=rabid, page=page).first()
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