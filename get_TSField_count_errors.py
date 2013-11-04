# -*- coding: utf-8 -*-
import pyfits
import numpy as np
import utils
#import inspect
import csv
import string
import os
from itertools import chain

def getFilterNumber(band):
  	if band == 'u':
  		return 0
  	elif band == 'g':
  		return 1
  	elif band == 'r':
  		return 2
  	elif band == 'i':
  		return 3
  	elif band == 'z':
  		return 4


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)      


class GalaxyParameters:
  @staticmethod
  def SDSS(ID):
    dataDir = '../data/'    
    listFile = dataDir+'/SDSS_photo_match.csv' 
    ret = GalaxyParameters()
    CALIFAID_col = 0
    ra_col = 1
    dec_col = 2
    run_col = 7
    rerun_col = 8
    camcol_col = 9
    field_col = 10
    with open(listFile, 'rb') as f:
	mycsv = csv.reader(f)
	mycsv = list(mycsv)	
	ret.CALIFAID = string.strip(mycsv[ID][CALIFAID_col])
	ret.ra = string.strip(mycsv[ID][ra_col])
	ret.dec = string.strip(mycsv[ID][dec_col])
	ret.run = string.strip(mycsv[ID][run_col])
	ret.rerun = string.strip(mycsv[ID][rerun_col])
	ret.camcol = string.strip(mycsv[ID][camcol_col])
	ret.field = string.strip(mycsv[ID][field_col])
	ret.runstr = utils.run2string(ret.run)
	ret.field_str = utils.field2string(ret.field)	
    return ret


def getFields(img, filterNumber):
  zpt_r = list(img.field(27))[0][filterNumber]
  ext_coeff = list(img.field(33))[0][filterNumber]
  #airmass = list(img.field(22))[0][filterNumber]
  airmass = img.field('airmass')[0][filterNumber]
  zpt = img.field('aa')[0][filterNumber]
  sky = img.field('sky')[0][filterNumber]
  nCR = img.field('nCR')[0][filterNumber]  
  skySig = img.field('skySig')[0][filterNumber]    
  skyErr = img.field('skyErr')[0][filterNumber]  
  ext_coeff = img.field('kk')[0][filterNumber]
  gain = img.field('gain')[0][filterNumber]  
  dark_variance = img.field('dark_variance')[0][filterNumber]  
  return [zpt_r, ext_coeff, airmass, gain, dark_variance, sky, skySig, skyErr, nCR]

def getParams(ID, band):
      #www.sdss.org/dr7/dm/flatFiles/tsField.html -- SDSS documentation
      filterNumber = getFilterNumber(band) #(0, 1, 2, 3, 4 - ugriz SDSS filters)     
      run = GalaxyParameters().SDSS(ID).run
      rerun = GalaxyParameters.SDSS(ID).rerun
      camcol = GalaxyParameters.SDSS(ID).camcol
      field = GalaxyParameters.SDSS(ID).field
      runstr = GalaxyParameters.SDSS(ID).runstr
      field_str = GalaxyParameters.SDSS(ID).field_str
	
      #print 'STR -- http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+ca  mcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
      
      try:
	print 'http://das.sdss.org/imaging/'+run+'/'+rerun+'/dr/'+camcol+'/drField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
	
	tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')

	img = tsFile[1].data
	#indexing -- field numbering in documentation starts with 0, hence #27 instead of #28 field, etc	
	params = getFields(img, filterNumber)
	tsFile.close()	
      except IOError as err:
	tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/dr/'+camcol+'/drField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')	
	img = tsFile[1].data
	params = getFields(img, filterNumber)
	tsFile.close()
      return params

with open('count_error_params.csv', 'a') as f:
  for i in range(0, 940):
    par = []
    for band in ['u', 'g', 'r', 'i', 'z']: #0, 1, 2, 3, 4
      params = getParams(i, band)
      par.append(params)
    #print str(i+1)+","+str(list(flatten(par)))[1:-1]+os.linesep
    f.write(str(i+1)+","+str(list(flatten(par)))[1:-1]+os.linesep)
    
f.close()
