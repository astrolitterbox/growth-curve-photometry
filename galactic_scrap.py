#the main part is written by mic (http://wemakethings.net)
#usage: set input filename and outputFile: python galactic_scrap.py inputFile outputFile

import sys
import urllib
import re

nedNames = sys.argv[1]
outputFile = sys.argv[2]

names = open(nedNames).readlines()
i = 1;
for name in names:
	url = "http://ned.ipac.caltech.edu/cgi-bin/objsearch?objname=" + name.strip() + "&extend=no&hconst=70&omegam=0.272&omegav=0.728&corr_z=1&out_csys=Equatorial&out_equinox=J2000.0&obj_sort=RA+or+Longitude&of=pre_text&zv_breaker=30000.0&list_limit=5&img_stamp=NO"
	page = urllib.urlopen(url).read()
	match = re.search("V \(Virgo \+ GA \+ Shapley\)   \: +(.*) +\+", page)
	if match:
		velocity = match.group(1)
	else:
		velocity = "NULL"
	dataline = str(i) + ",'" + name.strip() + "'," + velocity
	print dataline
	outfile = open(outputFile, "a")
	outfile.write(dataline + "\n")
	outfile.close()
	i+=1
