# -*- coding: utf-8 -*-
import pyfits
import os
import string
import gzip
import csv
import utils
import inpaint
from astLib import astWCS
import numpy as np
import sdss_photo_check as sdss
import plot_survey as plot
#import photometry as phot

#import readAtlas
#import circle
import db
import os


class GalaxyParameters:
  @staticmethod
  def SDSS(listFile, ID):
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
  def getSDSSUrl(listFile, dataDir, ID):
      camcol = GalaxyParameters.SDSS(listFile, ID).camcol
      field = GalaxyParameters.SDSS(listFile, ID).field
      field_str = GalaxyParameters.SDSS(listFile, ID).field_str
      runstr = GalaxyParameters.SDSS(listFile, ID).runstr
      fpCFile = dataDir+'/SDSS/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'
      return fpCFile
  @staticmethod
  def getFilledUrl(listFile, dataDir, ID):
     sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
     return dataDir+"/filled2/"+utils.createOutputFilename(sdssFilename, dataDir)
  @staticmethod
  def getMaskUrl(listFile, dataDir, simpleFile, ID):
     NedName = GalaxyParameters.getNedName(listFile, simpleFile, ID).NedName
     print NedName
     maskFile = dataDir+'/MASKS/'+NedName+'_mask_r.fits'
     return maskFile
  @staticmethod
  def getNedName(listFile, simpleFile, ID):
    ret = GalaxyParameters()
    with open(simpleFile, 'rb') as f:
      NEDNAME_col = 2
      mycsv = csv.reader(f)
      mycsv = list(mycsv)	
      ret.NedName = string.strip(mycsv[ID][NEDNAME_col])
      print ret.NedName
    return ret
  
    

def main():
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  #dataDir = '../data'
  dataDir = '/media/46F4A27FF4A2713B_/work2/data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
		
  i = 938
 
    
  print GalaxyParameters.getMaskUrl(listFile, dataDir, simpleFile, i)
  print GalaxyParameters.getFilledUrl(listFile, dataDir, i)
  print GalaxyParameters.getNedName(listFile, simpleFile, i)

  import os
  #os.system("gwenview "+"/home/opit/Desktop/PhD/dev/growth-curve-photometry/img/snapshots/"+str(i+1)+"_gc-50%.jpg")
  
  #os.system("/home/opit/Desktop/ds9  -zoom 0.3 -scale mode 99.5 -file "+ GalaxyParameters.getSDSSUrl(listFile, dataDir, i) +" -file  "+ GalaxyParameters.getMaskUrl(listFile, dataDir, simpleFile, i) +" -match frames")
  #os.system("gimp "+ GalaxyParameters.getMaskUrl(listFile, dataDir, simpleFile, i))

  exit()

  import pyfits
  
  imgFile = pyfits.open(GalaxyParameters.getSDSSUrl(listFile, dataDir, i))
  img = imgFile[0].data
  img = img[-700:,0:451]
  hdu = pyfits.PrimaryHDU(img)
  hdu.writeto('norm/'+imgFile)  
  
  
  maskFile = pyfits.open(GalaxyParameters.getMaskUrl(listFile, dataDir, i))
  mask = maskFile[0].data
  mask =   mask[-700:,0:451]
  hdu = pyfits.PrimaryHDU(mask)
  hdu.writeto('norm/'+maskFile)  

if __name__ == "__main__":
  main()

  
  
