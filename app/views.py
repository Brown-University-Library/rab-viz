from flask import render_template, json

from app import app
from .models import ChordViz, ForceViz, Faculty, Departments

from collections import defaultdict
import math
import re
import requests
import os

colorRange = ['rgb(23,190,207)','rgb(188,189,34)','rgb(227,119,194)',
'rgb(148,103,189)','rgb(214,39,40)','rgb(44,160,44)','rgb(255,127,14)',
'rgb(31,119,180)','rgb(214,97,107)','rgb(206,109,189)','rgb(214,97,107)',
'rgb(231,186,82)','rgb(181,207,107)','rgb(107,110,207)','rgb(230,85,13)',
'rgb(49,130,189)','rgb(49,163,84)','rgb(158,154,200)','rgb(253,141,60)',
'rgb(116,196,118)','rgb(189,158,57)']

dservURI = "https://vivo.brown.edu/services/data/v1/"

def joinFaculty(vizKey, urlbase, facSQL):
	facObjs = [
		{"rabid": f.rabid,
		"shortid": f.rabid[33:],
		"graphid": urlbase + "faculty/" + f.rabid[33:],
		"name": f.fullname,
		"abbv":f.abbrev + ".",
		"aff":f.deptid,
		"facIdx": vizKey.index(uri),
		"facNet": []
		} for uri in vizKey
			for f in facSQL
				if uri == f.rabid ]
	return facObjs

def joinDepartments(facObjs, urlbase, deptSQL):
	deptData = [ (fac['aff'], fac['facIdx'], fac['facNet'])
					for fac in facObjs ]
	depts = list({ p[0] for p in deptData})
	deptObjs = [
		{"rabid": d.rabid,
		"shortid": d.rabid[33:],
		"graphid": urlbase + "dept/" + d.rabid[33:],
		"name": d.label,
		"deptNet": [],
		"deptMembers": set(),
		} for p in depts
		 		for d in deptSQL
		 			if p == d.rabid ]
	for dept in deptObjs:
		for p in deptData:
			if dept["rabid"] == p[0]:
				dept["deptMembers"].add(p[1])
				dept["deptNet"].extend(p[2])
	for dept in deptObjs:
		dept["deptNet"] = list(dept["deptNet"])
		dept["deptMembers"] = list(dept["deptMembers"])
	return deptObjs

def chunkify(tList, chunk):
	return [ tList[i:i+chunk] for i in range(0, len(tList), chunk) ]

def tabAbbv(chunk):
	start = chunk[0]["name"][0]
	end = chunk[-1]["name"][0]
	if start == end:
		return start
	else:
		return start+"-"+end

def prepFacultyForDisplay(facObjs):
	sortedFacs = sorted(facObjs, key=lambda kv: kv['name'])
	chunkedFacs = chunkify(sortedFacs, 20)
	tabbedFacs = [ {"tab": tabAbbv(chunk),
					"faculty": chunk } for chunk in chunkedFacs ]
	return tabbedFacs

def prepDepartmentsForDisplay(deptObjs):
	sortedDepts = sorted(deptObjs, key=lambda kv: kv['name'])
	columnedDepts = chunkify(sortedDepts, int(math.ceil(len(sortedDepts)/3.0)))
	if len(columnedDepts) < 3: # Needed for when len(deptObjs) == 4
		straggler = columnedDepts[1].pop()
		columnedDepts.append([straggler])
	return columnedDepts

@app.route('/<graphtype>/')
# @app.route('/<graphtype>/')
def index(graphtype):
	if graphtype == "force":
		allViz = ForceViz.query.all()
		urlbase = "http://localhost:8000/force/"
		pageTitle = "Force Graph"
	elif graphtype == "chord":
		allViz = ChordViz.query.all()
		urlbase = "http://localhost:8000/chord/"
		pageTitle = "Chord Graph"
	else:
		raise Exception("Bad graphtype: "+graphtype)
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
	urlbase = "http://localhost:8000/force/"
	vizData = ForceViz.query.filter_by(rabid=rabid, page=page).first()
	vizKey = json.loads(vizData.legend)
	links = json.loads(vizData.links)
	allFaculty = Faculty.query.all()
	allDepts = Departments.query.all()
	facObjs = joinFaculty(vizKey, urlbase, allFaculty)
	for fac in facObjs:
		for l in links:
			if l["source"] == fac["facIdx"]:
				fac["facNet"].append(l["target"])
	deptObjs = joinDepartments(facObjs, urlbase, allDepts)
	nodes = [ {	"name": facObj["name"],
				"group": facObj["aff"]
				} for facObj in facObjs ]
	forceData = { "nodes": nodes, "links": links }
	tabbedFacs = prepFacultyForDisplay(facObjs)
	columnedDepts = prepDepartmentsForDisplay(deptObjs)
	facObjLookup = { fac["rabid"]: fac  for fac in facObjs }
	deptObjLookup = { dept["rabid"]: dept  for dept in deptObjs }
	if viztype=='dept':
		vizSbj = deptObjLookup[rabid]
		dservType = 'ou'
	elif viztype=='faculty':
		vizSbj = facObjLookup[rabid]
		dservType = 'faculty'
	getDserv = os.path.join(dservURI, dservType, vizSbj["shortid"])
	res = requests.get(getDserv)
	if res.status_code == 200:
		resData = res.json()["results"]
		vizSbj["thumb"] = resData.get("thumbnail")
		vizSbj["title"] = resData.get("title")
	return render_template(
			'force.html',
			departments=columnedDepts, faculty=tabbedFacs,
			facObjs=facObjLookup, deptObjs=deptObjLookup,
			vizSubject = vizSbj,
			colorScale=deptObjLookup.keys(),
			vizdata=forceData,
			linkDist=40,
			repel=(-90000/(len(facObjs)+20)**1.4),
			crange=colorRange)
