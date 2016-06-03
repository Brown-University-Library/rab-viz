from flask import render_template, json

from app import app
from .models import ChordViz, ForceViz, Faculty, Departments

colorRange = ['rgb(23,190,207)','rgb(188,189,34)','rgb(227,119,194)',
'rgb(148,103,189)','rgb(214,39,40)','rgb(44,160,44)','rgb(255,127,14)',
'rgb(31,119,180)','rgb(214,97,107)','rgb(206,109,189)','rgb(214,97,107)',
'rgb(231,186,82)','rgb(181,207,107)','rgb(107,110,207)','rgb(230,85,13)',
'rgb(49,130,189)','rgb(49,163,84)','rgb(158,154,200)','rgb(253,141,60)',
'rgb(116,196,118)','rgb(189,158,57)']

# colorRange = [
# 			"rgba(23,190,207,1)",
# 			"rgba(188,189,34,1)",
# 			"rgba(227,119,194)",
# 			"rgb(148,103,189,1)",
# 			"rgba(214,39,40,1)",
# 			"rgba(44,160,44,1)",
# 			"rgba(255,127,14,1)",
# 			"rgba(31,119,180,1)",
# 			"rgba(214,97,107,1)",
# 			"rgba(206,109,189,1)",
# 			"rgba(214,97,107,1)",
# 			"rgba(231,186,82,1)",
# 			"rgba(181,207,107,1)",
# 			"rgba(107,110,207,1)",
# 			"rgba(230,85,13,1)",
# 			"rgba(49,130,189,1)",
# 			"rgba(49,163,84,1)",
# 			"rgba(158,154,200,1)",
# 			"rgba(253,141,60,1)",
# 			"rgba(116,196,118,1)",
# 			"rgba(189,158,57,1)"
# 			]

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

@app.route('/force/<viztype>/<rabid>')
@app.route('/force/<viztype>/<rabid>/<page>')
def forceViz(viztype, rabid, page=0):
	rabid = "http://vivo.brown.edu/individual/{0}".format(rabid)
	vizData = ForceViz.query.filter_by(rabid=rabid, page=page).first()
	legend = json.loads(vizData.legend)
	allFaculty = Faculty.query.all()
	allDepts = Departments.query.all()
	facultyLookup = { f.rabid: [f.abbrev, f.deptLabel, f.rabid] for f in allFaculty }
	nodes = [ {	"name": facultyLookup[uri][0],
				"group": facultyLookup[uri][1],
				"rabid": facultyLookup[uri][2] }
					for uri in legend ]
	links = json.loads(vizData.links)
	deptList = sorted(list({ n["group"] for n in nodes }))
	deptMap = { l: d.rabid for l in deptList for d in allDepts if l in json.loads(d.useFor)  }
	facMap = { f.abbrev: f.rabid for f in allFaculty if f.rabid in legend }
	facObjs = [ {'rabid': f.rabid,
				'name': f.fullname,
				'abbv':f.abbrev,
				'aff':f.deptLabel } for f in allFaculty
										if f.rabid in legend ]
	facObjs = sorted(facObjs, key=lambda kv: kv['name'])
	vizdata = {"nodes": nodes, "links": links}
	if viztype=='dept':
		pageLabel = [ d.label for d in allDepts if d.rabid == rabid ][0]
	elif viztype=='faculty':
		pageLabel = [ f.fullname for f in allFaculty if f.rabid == rabid ][0]
	return render_template(
			'force.html', pageLabel=pageLabel, legend=deptList,
			deptMap=deptMap, facMap=facMap, faculty=facObjs, vizdata=vizdata,
			linkDist=30, repel=-350, crange=colorRange)