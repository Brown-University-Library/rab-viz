import sys
import csv
import os
import json

def main(inFileFac, inDeptFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	facs = []

	with open(inFileFac, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		# rabid, last, first, label, title, primaryOU 
		for row in rdr:
			if not row[5]:
				primaryOU = "None"
			else:
				primaryOU = row[5]
			facs.append((row[0], row[1], row[2], row[3], row[4], primaryOU))

	deptLabels = dict()

	altDeptLabels = {
		"Earth, Environmental and Planetary Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept667",
		"Geological Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept667",
		"Brown University":
			"http://vivo.brown.edu/individual/org-brown-univ",
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
		"Sheridan Center": #Just a stub for now, pointing at Engineering
			"http://vivo.brown.edu/individual/org-brown-univ-dept75",
		"Clin Neurosciences (Neurology)":
			"http://vivo.brown.edu/individual/org-brown-univ-dept235",
		"Cognitive, Linguistic and Psychological Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept288",
		"Admin General":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Middle East Studies":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Community Health":
			"http://vivo.brown.edu/individual/org-brown-univ-dept250",
		"Population Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept78",
		"Development Studies":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Physiology":
			"http://vivo.brown.edu/individual/org-brown-univ-dept55",
		"Medical Science": #Pointed at Medicine
			"http://vivo.brown.edu/individual/org-brown-univ-dept84",
		"None":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Renaissance and Early Modern Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept32",
		"Environment and Society":
			"http://vivo.brown.edu/individual/org-brown-univ-dept687",
		"Public Policy":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Clin Neurosciences (Neurosurg)":
			"http://vivo.brown.edu/individual/org-brown-univ-dept240",
		"Dean of the College":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Slavic Languages":
			"http://vivo.brown.edu/individual/org-brown-univ-dept669",
		"Gender Studies":
			"http://vivo.brown.edu/individual/org-brown-univ",
		"Cognitive and Linguistic Sciences":
			"http://vivo.brown.edu/individual/org-brown-univ-dept288",
		"International Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept748",
		"Environmental Change Initiative":
			"http://vivo.brown.edu/individual/org-brown-univ-dept687",
		"Environmental Studies":
			"http://vivo.brown.edu/individual/org-brown-univ-dept687",
	}

	with open(inDeptFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			deptLabels[row[1]] = row[0]

	with open(
			os.path.join(targetDir,'faculty_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		for fac in facs:
			rabid, last, first, name, title, ou = fac
			if ou in deptLabels:
				ouURI = deptLabels[ou]
			elif ou in altDeptLabels:
				ouURI = altDeptLabels[ou]
			else:
				raise Exception("Bad OU: ", ou)
			abbrev = last + ", " + first[0]
			row = (rabid, last, first, name, abbrev, title, ouURI)
			wrtr.writerow(row)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])