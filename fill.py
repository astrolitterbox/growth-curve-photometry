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
import plot_survey as plot
#import photometry as phot
from sgolay2d import sgolay2d
import readAtlas
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
     return '../data/filled/'+utils.createOutputFilename(sdssFilename)
  @staticmethod
  def getMaskUrl(listFile, dataDir, simpleFile, ID):
     NedName = GalaxyParameters.getNedName(listFile, simpleFile, ID).NedName
     print NedName
     maskFile = dataDir+'/MASKS/'+NedName+'_mask_r.fits'
     return maskFile
  
  
  
#class Inpaint():  
  
class Interpolation():

  @staticmethod
  def runInpainting(maskFile, listFile, dataDir, ID, log):
    maskFilename = utils.getMask(maskFile, ID)
    sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
    outputFilename = utils.createOutputFilename(sdssFilename)
    print 'output filename', outputFilename
    try:
      with open(dataDir+'/filled/'+outputFilename) as f: pass
      print 'skipping', ID
    except IOError as e:
      print 'inpainting', ID
      sdssImage = pyfits.open(sdssFilename)
      imageData = sdssImage[0].data
      imageData = imageData - 1000 #soft bias subtraction, comment out if needed
      head = sdssImage[0].header
      maskFile = pyfits.open(maskFilename)
      mask = maskFile[0].data
      maskedImg = np.ma.array(imageData, mask = mask)
      NANMask =  maskedImg.filled(np.NaN)
      filled = inpaint.replace_nans(NANMask, 100, 0.1, 2, 'idw')
      hdu = pyfits.PrimaryHDU(filled, header = head)
      hdu.writeto(dataDir+'/filled/'+outputFilename)
    return log
    
    

def main():
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  #noOfGalaxies = 938
  #i = 0
  #inputFile = Photometry.getInputFile(listFile, dataDir, i)
  #distances = Photometry.createDistanceArray(listFile, i, dataDir)
  #inputImage = Photometry.calculateGrowthCurve(listFile, dataDir, i)
  
  #center = Photometry.getCenter(listFile, i, dataDir)
  #distances = Photometry.createDistanceArray(listFile, i, dataDir)
  
  #Photometry.createDistanceArray(listFile, i, dataDir, center)
  #Photometry.circleContours(inputFile, distances, center, iso25D)
  #print GalaxyParameters.getNedName(listFile, simpleFile, 0).NedName, 'url:', GalaxyParameters.getSDSSUrl(listFile, dataDir, 0)
  #print Astrometry.getCenterCoords(listFile, 0)
  
  log = []
  #for i in range(766, 938):  
  #  print i, 'galaxy'
  
  
  for i in range(0, 938):
    print 'i', i
    Interpolation.runInpainting(maskFile, listFile, dataDir, i, log)
  
  
  
  #  print GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
  #np.savetxt('errorlog.txt', log)  
  #Photometry.calculateGrowthCurve(listFile, dataDir, 4)
  #print GalaxyParameters.getFilledUrl(listFile, dataDir, 2)
  #print Photometry.compareWithSDSS(listFile, dataDir, 4)
  #ra = float(GalaxyParameters.SDSS(listFile, 4).ra)
  #dec = float(GalaxyParameters.SDSS(listFile, 4).dec)
  #print readAtlas.find_mag(ra, dec)
  
  #center = Astrometry.getPixelCoords(listFile, i, dataDir)
  #print inputImage.shape
  #inputImage = utils.get_cutout(center, inputImage, 500)
  #circle.main(inputImage)  
  #Photometry.calculateGrowthCurve(listFile, dataDir, 4)
  #print GalaxyParameters.getFilledUrl(listFile, dataDir, 2)
  #print Photometry.compareWithSDSS(listFile, dataDir, 4)
  #ra = float(GalaxyParameters.SDSS(listFile, 4).ra)
  #dec = float(GalaxyParameters.SDSS(listFile, 4).dec)
  #hdu = pyfits.PrimaryHDU(inputImage)
  #hdu.writeto('input.fits')
  #print readAtlas.find_mag(ra, dec)

if __name__ == "__main__":
  main()
