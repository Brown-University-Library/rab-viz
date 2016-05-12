import sys
import csv
import os
import json
from collections import defaultdict

def main(inDeptFile, inFacFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	depts = dict()
	altLabels = {
		"Earth, Environmental and Planetary Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept667",
		"Geological Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept667",
		"Brown University":
			"",
		"Psychology":
			"http://vivo.brown.edu/individual/org-brown-univ-dept288",
		"Humanities":
			"http://vivo.brown.edu/individual/org-brown-univ-dept124",
		"Clinical Neuroscience":
			"http://vivo.brown.edu/individual/org-brown-univ-dept56",
		"Behavioral and Preventive Medicine":
			"http://vivo.brown.edu/individual/org-brown-univ-dept280",
		"Egyptology and Ancient Western Asian Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept668",
		"Sheridan Center":
			"",
		"Clin Neurosciences (Neurology)":
			"http://vivo.brown.edu/individual/org-brown-univ-dept235",
		"Cognitive, Linguistic and Psychological Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept288",
		"Admin General":
			"",
		"Middle East Studies":
			"",
		"Community Health":
			"http://vivo.brown.edu/individual/org-brown-univ-dept250",
		"Population Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept78",
		"Development Studies":
			"",
		"Physiology":
			"http://vivo.brown.edu/individual/org-brown-univ-dept55",
		"Medical Science":
			"",
		"None":
			"",
		"Renaissance and Early Modern Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept32",
		"Environment and Society":
			"http://vivo.brown.edu/individual/org-brown-univ-dept687",
		"Public Policy":
			"",
		"Clin Neurosciences (Neurosurg)":
			"http://vivo.brown.edu/individual/org-brown-univ-dept240",
		"Dean of the College":
			"",
		"Slavic Languages":
			"http://vivo.brown.edu/individual/org-brown-univ-dept669",
		"Gender Studies":
			"",
		"Cognitive and Linguistic Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept288",
		"International Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept748",
		"Environmental Change Initiative":
			"http://vivo.brown.edu/individual/org-brown-univ-dept687",
	}

	with open(inDeptFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		#Auth1URI, Auth2URI, CitationURI
		for row in rdr:
			# Handle departments with more than 1 label
			if depts.get(row[0]):
				continue
			else:
				depts[row[0]] = row[1]
				altLabels[row[1]] = row[0]

	with open(inFacFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		#Skip header
		head = rdr.next()
		for row in rdr:
			if not row[5]:
				aff = "None"
			else:
				aff = row[5]
			# Handle departments with more than 1 label
			if aff in altLabels and altLabels[aff] != "":
				continue
			else:
				print "No URI for affiliation: ", aff
				continue

	useFor = defaultdict(list)
	for label in altLabels:
		useFor[altLabels[label]].append(label)

	with open(
			os.path.join(targetDir,'departments_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for deptid, label in depts.items():
			row = (deptid, label, json.dumps(useFor[deptid]))
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])