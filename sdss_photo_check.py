#!/usr/bin/env python

# Written by Min-Su Shin in Princeton astrophysics
# Feel free use or revise the code.
# puporse : to search the SDSS PhotoObjAll in a command-line mode
# modified to be incorporated in a larger code by astrolitterbox
import sqlcl
import sys
import string
import time


def get_sdss_photometry(coords):

	if (len(coords) == 1 or len(coords) != 2):
		print "It checks the SDSS PhotoObjAll catalog to find all photometric objects\n within a given radius."
		print "usage : sdss_photo_check.py (ra) (dec) -r (search radius)"
		print "\tra : degree"
		print "\tdec : degree"
		print "\tsearch radius : arcsec (optional) (default : 3 arcsec)"
		print "output : ObjId model_u model_g model_r model_i model_z"
		sys.exit()

	search_rad = '10'
	print coords, "****************************", coords[0]	
	ra = str(coords[0])
	print ra, coords[0]
	dec = str(coords[1])

	sql_query = "select P.objid, P.modelMag_u, P.modelMag_g, P.modelMag_r, P.modelMag_i, P.modelMag_z from PhotoObjAll P, dbo.fGetNearbyObjAllEq("+ra+","+dec+","+search_rad+") n where P.objID = n.objID"
	query_result = sqlcl.query(sql_query).readlines()
	if len(query_result) > 1 :
		data_part = string.split(query_result[1],",")
		output_string = ""
		for x in data_part:
			output_string = output_string + x.strip() + " "
		print output_string
		time.sleep(1.0)
	else :
		print "No object found"
				
