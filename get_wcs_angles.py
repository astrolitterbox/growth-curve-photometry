# -*- coding: utf-8 -*-
#import Interpol
#import getImages
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
#import plot_survey as plot
#import photometry as phot
from math import ceil
#import readAtlas
#import circle
import db
import os
import sdss
#import imtools
#import scipy.misc

dbDir = '../db/'


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
      band = setBand()
      camcol = GalaxyParameters.SDSS(listFile, ID).camcol
      field = GalaxyParameters.SDSS(listFile, ID).field
      field_str = GalaxyParameters.SDSS(listFile, ID).field_str
      runstr = GalaxyParameters.SDSS(listFile, ID).runstr
      fpCFile = dataDir+'/SDSS/'+band+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz'

      return fpCFile
  @staticmethod
  def getFilledUrl(listFile, dataDir, ID):
     sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
     return dataDir+filledDir+utils.createOutputFilename(sdssFilename)
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
    return ret
  

  
  
#class Inpaint():  
  
class Interpolation():
  
  @staticmethod
  def rotateYourOwl(inputArray, n):
    return np.rot90(inputArray, n)
  
  @staticmethod
  def runInpainting(maskFile, listFile, dataDir, ID, log):
    maskFilename = dataDir+utils.getMask(maskFile, ID)
    sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
    outputFilename = utils.createOutputFilename(sdssFilename, dataDir)
    outputDir = dataDir+'/filled'
    print 'output filename', outputFilename
    #try:
      #with open(dataDir+'/filled2/'+outputFilename) as f: pass
      #print 'skipping', ID
    #except IOError as e:
    print 'inpainting', ID
    sdssImage = pyfits.open(sdssFilename)
    imageData = sdssImage[0].data
    imageData = imageData - 1000 #soft bias subtraction, comment out if needed
    head = sdssImage[0].header
    maskFile = pyfits.open(maskFilename)
    print 'MASK', maskFilename
    mask = maskFile[0].data
    callInpaint(imageData, mask, outputDir)	
    return log
  @staticmethod  
  def plotFilled(inputImage, i):
    CALIFA_ID = str(int(i)+1)
    outputImage = inputImage
    #outputImage, cdf = imtools.histeq(outputImage)
    #scipy.misc.imsave('img/g/'+CALIFA_ID+'_image.jpg', outputImage)  
  @staticmethod
  def callInpaint(img, mask, outputFilename, i):
      maskedImg = np.ma.array(img, mask = mask)
      NANMask =  maskedImg.filled(np.NaN)
      filled = inpaint.replace_nans(NANMask)
      #outputFilename = utils.createOutputFilename(sdssFilename, dataDir)
      hdu = pyfits.PrimaryHDU(filled)
      
      if os.path.exists(outputFilename):
	  print outputFilename
	  outputFilename = outputFilename+"B"
	  hdu.writeto(outputFilename)      
      else:
	  hdu.writeto(outputFilename)   
      #Interpolation.plotFilled(filled, i)


def setBand():
  return 'r'

def checkInput(listFile, dataDir, ID, run, rerun, camcol, runstr, band, field_str, fitsDir):
	try:
	  f = open(GalaxyParameters.getSDSSUrl(listFile, dataDir, ID-1))
	  print 'it is here', ID - 1
	  pass
	except IOError as e: 
	  print e, ID - 1
	  os.system('wget -P '+fitsDir+band+' http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz')     
	  pass

	try:
	  f = open(fitsDir+'r/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
	  print 'it is here', 'r', ID - 1
	  pass
	except IOError as e:  
	  print e, 'r', ID - 1
	  os.system('wget -P '+fitsDir+'r/ http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
	  pass

def checkOutput(dataDir, ID, run, rerun, camcol, runstr, band, field_str, fitsDir, filledDir):
	outputFilename = dataDir+'/'+filledDir+'fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fits'
	print outputFilename
	try:
	  f = open(outputFilename)
	  #print 'musu', ID
	except IOError as e:
	  
	  out = [ID]
	  utils.writeOut(out, 'missing_'+setBand()+'.csv')
	  pass
	  
	  
def main():
  iso25D = 40 / 0.396
  #dataDir = '/media/46F4A27FF4A2713B_/work2/data/'
  dataDir = '../data'
  band = setBand()
  #outputFile = dataDir+'/growthCurvePhotometry.csv'
  listFile = dataDir+'/SDSS_photo_match.csv'
  fitsDir = dataDir+'/SDSS/'
  #filledDir = 'filled_'+band+'/'
  filledDir = 'filled2/'
  imgDir = 'img/'+band
  simpleFile = dataDir+'/CALIFA_mother_simple.csv'
  maskFile = dataDir+'/maskFilenames.csv'  
  dataFile = 'list.txt'
  
  for ID in range(1, 940):
  
	  	    print 'id,', int(ID) - 1	
		    ra = GalaxyParameters.SDSS(listFile, int(ID) - 1).ra
		    dec = GalaxyParameters.SDSS(listFile, int(ID) - 1).dec
		    run = GalaxyParameters.SDSS(listFile, int(ID) - 1).run
		    rerun = GalaxyParameters.SDSS(listFile, int(ID) - 1).rerun
		    camcol = GalaxyParameters.SDSS(listFile, int(ID) - 1).camcol		    
		    field = GalaxyParameters.SDSS(listFile, int(ID) - 1).field
		    runstr = GalaxyParameters.SDSS(listFile, int(ID) - 1).runstr
		    field_str = sdss.field2string(field)

		    print 'getting header info...'
		    rFile = fitsDir+'r/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'

		    WCS=astWCS.WCS(rFile)	
		    pa = utils.convert(db.dbUtils.getFromDB('pa', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+str(ID)))
		    ang = WCS.getRotationDeg() 
		    print ang
		    
		    pa_align = ang + pa - 360
		    out = int(ID), pa_align[0][0]
		    print out
		    utils.writeOut(out, "align_pa.csv")



if __name__ == "__main__":
  main()
