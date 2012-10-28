# -*- coding: utf-8 -*-
import numpy as np
import string
import csv
import utils
import sys
from ellipse_photometry import Settings



class GalaxyParameters:
  @staticmethod
  def SDSS(ID):
    listFile = Settings.getConstants().listFile
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
  
  @staticmethod
  def getSDSSUrl(ID):
      dataDir = Settings.getConstants().dataDir
      band = Settings.getConstants().band
      camcol = GalaxyParameters.SDSS(ID).camcol
      field = GalaxyParameters.SDSS(ID).field
      field_str = GalaxyParameters.SDSS(ID).field_str
      runstr = GalaxyParameters.SDSS(ID).runstr
      fpCFile = dataDir+'/SDSS/'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz'
      return fpCFile
  @staticmethod
  def getFilledUrl(ID, band):
      dataDir = Settings.getConstants().dataDir
      camcol = GalaxyParameters.SDSS(ID).camcol
      field = GalaxyParameters.SDSS(ID).field
      field_str = GalaxyParameters.SDSS(ID).field_str
      runstr = GalaxyParameters.SDSS(ID).runstr
      dupeList = [162, 164, 249, 267, 319, 437, 445, 464, 476, 477, 480, 487, 498, 511, 537, 570, 598, 616, 634, 701, 767, 883, 939]
      if band == 'r':
	fpCFile = dataDir+'/filled2/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
      	if (ID +1) in dupeList:
		fpCFile = dataDir+'/filled3/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
      else:
      	      fpCFile = dataDir+'/filled_'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
	      if(ID + 1) in dupeList:
		fpCFile = fpCFile+'B'
      return fpCFile
  @staticmethod
  def getMaskUrl(ID):
     dataDir = Settings.getConstants().dataDir
     NedName = GalaxyParameters.getNedName(ID).NedName
     print NedName
     maskFile = dataDir+'/MASKS/'+NedName+'_mask_r.fits'
     return maskFile
     	
  @staticmethod
  def getNedName(ID):
    simpleFile = Settings.getConstants().simpleFile
    ret = GalaxyParameters()
    with open(simpleFile, 'rb') as f:
      NEDNAME_col = 2
      mycsv = csv.reader(f)
      mycsv = list(mycsv)	
      ret.NedName = string.strip(mycsv[ID][NEDNAME_col])
    return ret
  
