from collections import defaultdict
import json
import csv
import os
import sys


def main(inCoauthFile, facCheckFile, targetDir):
	if not os.path.exists(targetDir):
		os.makedirs(targetDir)

	activeFaculty = set()
	auth_check = []
	coauth_check = []
	wx = defaultdict(lambda: defaultdict(lambda: 0))

	with open(facCheckFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			activeFaculty.add(row[0])

	with open(inCoauthFile, "r") as f:
		rdr = csv.reader(f, delimiter=',', quotechar='"')
		for row in rdr:
			if row[0] in activeFaculty and row[1] in activeFaculty:
				auth_check.append(row[0])
				coauth_check.append(row[1])
				wx[row[0]][row[1]] += 1
			else:
				continue

	# Simple sanity checks
	# All authors in CSV are keys in coauthor network dictionary
	assert set(wx.keys()) == set(auth_check)
	# Authors, coauthors, and network keys are all the same
	assert set(coauth_check) == set(wx.keys()) & set(auth_check)

	fac1_check = wx.keys()[0] # first author
	fac2_check = wx[fac1_check].keys()[0] # first author's first coauthor
	# Assert coauthorship counts are reciprocal
	assert wx[fac1_check][fac2_check] == wx[fac2_check][fac1_check]

	coauth_cnt = []
	coauth_json = []

	for auth, coauths in wx.items():
		coauth_json.append((auth, json.dumps(coauths)))
		for coauth, cnt in coauths.items():
			coauth_cnt.append((auth, coauth, cnt))

	with open(
			os.path.join(targetDir,'coauthors_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		wrtr.writerows(coauth_cnt)

	with open(
			os.path.join(targetDir,'author_json_data.csv'),
			 'w') as dataout:
		wrtr = csv.writer(dataout)
		wrtr.writerows(coauth_json)

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3])