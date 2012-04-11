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
#import photometry as phot

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
  def getMaskUrl(listFile, dataDir, simpleFile, ID):
     NedName = GalaxyParameters.getNedName(listFile, simpleFile, ID).NedName
     print NedName
     maskFile = dataDir+'/MASKS/'+NedName+'_mask_r.fits'
     return maskFile
  
  @staticmethod
  def getZeropoint(listFile, ID):
      filterNumber = 2 #(0, 1, 2, 3, 4 - ugriz SDSS filters)     
      run = GalaxyParameters.SDSS(listFile, ID).run
      rerun = GalaxyParameters.SDSS(listFile, ID).rerun
      camcol = GalaxyParameters.SDSS(listFile, ID).camcol
      field = GalaxyParameters.SDSS(listFile, ID).field
      runstr = GalaxyParameters.SDSS(listFile, ID).runstr
      field_str = GalaxyParameters.SDSS(listFile, ID).field_str
	#http://das.sdss.org/imaging/5115/40/calibChunks/2/tsField-005115-2-40-0023.fit
      print 'http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
      tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')
      print 'opened'
      img = tsFile[1].data
      head = tsFile[1].header
      zpt_r = list(img.field(27))[0][filterNumber]
      return zpt_r
	
  @staticmethod
  def getNedName(listFile, simpleFile, ID):
    ret = GalaxyParameters()
    with open(simpleFile, 'rb') as f:
      NEDNAME_col = 2
      mycsv = csv.reader(f)
      mycsv = list(mycsv)	
      ret.NedName = string.strip(mycsv[ID][NEDNAME_col])
    return ret
  

class Astrometry():
  @staticmethod
  def getCenterCoords(listFile, ID):
    centerCoords = (GalaxyParameters.SDSS(listFile, ID).ra, GalaxyParameters.SDSS(listFile, ID).dec)
    return centerCoords
  @staticmethod
  def getPixelCoords(listFile, ID, dataDir):
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(listFile, dataDir, ID))
    centerCoords = Astrometry.getCenterCoords(listFile, ID)
    print centerCoords
    pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    return pixelCoords
  
#class Inpaint():  
  
class Interpolation():
  @staticmethod
  def runInpainting(maskFile, listFile, dataDir, ID):
    maskFilename = utils.getMask(maskFile, ID)
    sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
    outputFilename = utils.createOutputFilename(sdssFilename)
    sdssImage = pyfits.open(sdssFilename)
    imageData = sdssImage[0].data
    imageData = imageData - 1000 #soft bias subtraction, comment out if needed
    head = sdssImage[0].header
    maskFile = pyfits.open(maskFilename)
    mask = maskFile[0].data
    maskedImg = np.ma.array(imageData, mask = mask)
    NANMask =  maskedImg.filled(np.NaN)
    filled = inpaint.replace_nans(NANMask, 15, 0.1, 2, 'idw')
    hdu = pyfits.PrimaryHDU(filled, header = head)
    hdu.writeto(dataDir+'/filled/'+outputFilename)
    	
    
    
    
    
def main():

  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 939
  
  #print GalaxyParameters.getNedName(listFile, simpleFile, 0).NedName, 'url:', GalaxyParameters.getSDSSUrl(listFile, dataDir, 0)
  #print Astrometry.getCenterCoords(listFile, 0)
  #print Astrometry.getPixelCoords(listFile, 0, dataDir)

  for i in range(0, 161):
    print i, 'galaxy'
    Interpolation.runInpainting(maskFile, listFile, dataDir, i)  
    print GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
    
  
if __name__ == "__main__":
  main()
