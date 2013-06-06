#usage: python sky_fitting.py lower_limit upper_limit band


# -*- coding: utf-8 -*-
import pyfits
import math
import os
import string
import gzip
import csv
import utils
import inpaint
from astLib import astWCS
import numpy as np
import sdss_photo_check as sdss
import imtools
import plot_survey as plot
#import photometry as phot
import readAtlas
import ellipse
import db
import getTSFieldParameters
import plotGrowthCurve		
from math import isnan
import scipy.misc 
import sys
from galaxyParameters import *
import matplotlib.pylab as plt
import cProfile
import multiprocessing



#a set of methods for swapping between pixel coordinates and ra, dec

class Astrometry():
  @staticmethod
  def getCenterCoords(ID):
    centerCoords = (GalaxyParameters.SDSS(ID).ra, GalaxyParameters.SDSS(ID).dec)
    return centerCoords
  @staticmethod
  def getPixelCoords(ID):   
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(ID)) #changed -- was filledUrl. I don't write coords to my masks..
    centerCoords = Astrometry.getCenterCoords(ID)
    print 'centerCoords', centerCoords
    pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    print 'pixCoords', pixelCoords
    out = [ID, centerCoords[0], centerCoords[1], pixelCoords[0], pixelCoords[1]]
    #utils.writeOut(out, 'coords.csv')
    return (pixelCoords[1], pixelCoords[0]) #y -- first, x axis -- second
  @staticmethod
  def distance2origin(shape, center):
    grid = np.indices(shape)
    y = grid[0] - center[0]
    x = grid[1] - center[1]
    r = np.round(np.sqrt(np.square(y) + np.square(x)), 0)
    return r
  @staticmethod
  def makeDistanceArray(img, center):
    distances = np.zeros(img.shape)
    distances = Astrometry.distance2origin(img.shape, center)

    return distances



class Photometry():
  pixelScale = 0.396
  iso25D = 40 / 0.396
  @staticmethod
  def getCenter(i):
    ra = Astrometry.getCenterCoords(i)[0]
    dec = Astrometry.getCenterCoords(i)[1]
    return Astrometry.getPixelCoords(i)
  @staticmethod
  def findClosestEdge(distances, center):
  #finds the closest distance from the center to the edge. Used for sky gradient calculation, as we want to avoid using a small number of pixels in a ring.
  #works by finding minimum [index] distance to one of the edges of array. 
    maxy = distances.shape[0] 
    maxx = distances.shape[1]
    print center, maxy, maxx
    yUp = center[0]
    yDown = maxy - center[0]
    xLeft = center[1]
    xRight = maxx - center[1]
    return int(math.floor(min(yUp, yDown, xLeft, xRight)))

  @staticmethod
  def createDistanceArray(i):
    center = Photometry.getCenter(i)

    #print 'center coords', center, 'coords', center[0], center[1]
    inputImage = Photometry.getInputFile(i, band=Settings.getConstants().band)
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(i))
    return distances
  @staticmethod
  def getInputFile(i, band):
    #print 'filename:', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(i, band))
    inputImage = inputFile[0].data
    if band != 'r':
       inputImage-=1000 
    #print 'opened the input file'
    return inputImage
  @staticmethod    
  def getInputHeader(listFile, dataDir, i): 
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(i))	
    head = inputFile[0].header
    return head	
  @staticmethod
  def getMask(ID):
     dataDir = Settings.getConstants().dataDir
     maskFilename = dataDir+utils.getMask(Settings.getConstants().maskFile, ID)
     maskFile = pyfits.open(maskFilename)
     mask = maskFile[0].data
     print maskFilename
     maskFile.close()
     print mask.shape, 'mask'
     return mask
       
  @staticmethod
  def fitSky(center, distances, pa, ba, CALIFA_ID):
    #limit = findClosestEdge(distances, center)
    band = Settings.getConstants().band
    inputImage = Photometry.getInputFile(int(CALIFA_ID) - 1, band)
    mask = Photometry.getMask(int(CALIFA_ID) - 1)
    #start = Photometry.getStart(CALIFA_ID) - 500
    start = 100
    radius = 150
    step = 50
    fluxSlopeM = -10 #init
    fluxSlope = -10
    while fluxSlopeM < 0:
      fluxData = Photometry.growEllipses(inputImage, distances, center, start, start+radius, pa, ba, CALIFA_ID, mask)
      #fitting unmasked
      xi = fluxData[:, 0] #isoA
      A = np.array([xi, np.ones(len(fluxData))])
      y = np.divide(fluxData[:, 1], fluxData[:, 2]) #flux ppx
      #print np.mean(y), start
      w = np.linalg.lstsq(A.T,y)[0] # obtaining the parameters
      fluxSlope = w[0]
      line = w[0]*xi+w[1] # regression line
      #print fluxSlope, 'slope'
      #fitting masked
      #print 'fitting masked'
      xi = fluxData[:, 0] #isoA
      A = np.array([xi, np.ones(len(fluxData))])
      yM = np.divide(fluxData[:, 3],fluxData[:, 4]) #flux ppx

      w = np.linalg.lstsq(A.T,yM)[0] # obtaining the parameters
      fluxSlopeM = w[0]
      print np.mean(yM), np.mean(y), start, fluxSlope, np.sum(fluxData[:, 2]), np.sum(fluxData[:, 4])  
      line = w[0]*xi+w[1] # regression line
      #print fluxSlopeM, 'slope'

      start = start + step
    return np.mean(y), fluxSlope, np.mean(yM), fluxSlopeM, fluxData[-1, 0]
   
  @staticmethod
  def growEllipses(inputImage, distances, center, start, end, pa, ba, CALIFA_ID, mask):
    fluxData = np.empty((150, 5))
    i = 0
    for isoA in range(start, end):
	      #draw ellipse for all pixels:
	      currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
      	      Npix = inputImage[currentPixels].shape[0]
	      currentFlux = np.sum(inputImage[currentPixels])
	      #draw ellipse with masks:
	      inputImageM = np.ma.masked_array(inputImage, mask=mask)
	      NpixM = inputImageM[currentPixelsM].compressed().shape[0]

	      inputImageM = np.ma.fix_invalid(inputImage, fill_value=0)
	      currentPixelsM = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
	      currentFluxM = np.sum(inputImage[currentPixelsM])
	      print Npix, NpixM, 'npix', currentFlux, currentFluxM, 'flux'
	      
	      #write out
	      fluxData[i, 0] = isoA
	      fluxData[i, 1] = currentFlux
	      fluxData[i, 2] = Npix
	      fluxData[i, 3] = currentFluxM
	      fluxData[i, 4] = NpixM
	      
	      #print isoA, currentFlux, Npix, currentFlux/Npix
	      i = i + 1
	      #print 'ret'
    return fluxData

    
  @staticmethod
  def calculateGrowthCurve(i):
    CALIFA_ID = str(i+1)

    dbDir = '../db/'
    imgDir = 'img/'+Settings.getConstants().band+'/'
    center = Photometry.getCenter(i)
    distances = Photometry.createDistanceArray(i)

    pa = db.dbUtils.getFromDB('pa', Settings.getConstants().dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0]
    ba = db.dbUtils.getFromDB('ba', Settings.getConstants().dbDir+'CALIFA.sqlite', 'bestBA', ' where califa_id = '+ CALIFA_ID)[0]
    
    #print CALIFA_ID, pa
    #pa = -1*(90 - pa)
    
    # --------------------------------------- starting ellipse GC photometry

    print 'ELLIPTICAL APERTURE'
    try:
      #returns np.mean(y), fluxSlope, np.mean(yM), fluxSlopeM, fluxData[-1, 0]
      sky, slope, skyM, slopeM, isoA  = Photometry.fitSky(center, distances, pa, ba, CALIFA_ID)
    except IndexError:
      sky = 'nan'
      slope = 'nan'
      isoA = 'nan'
      print 'aaaa'
    out = (CALIFA_ID, sky, slope, skyM, slopeM, isoA)
    utils.writeOut(out, "sky_fits_"+Settings.getConstants().band+"_new.csv")
    

def getDuplicates():
	#for i in range(0, 939):
	#	print i+1, GalaxyParameters.getFilledUrl(listFile, dataDir, i)
		
    	fnames = np.genfromtxt('outputNames.txt', dtype='object')

    	#ndtype = [('id', int), ( 'fname', str)]
    	#fnames = fnames.view(ndtype)
    	#du = np.lib.recfunctions.find_duplicates(fnames, key='fname', ignoremask=True, return_index=False)    
	ids = list(fnames[:, 0])	
	fnames = list(fnames[:, 1])	
	u, indices = np.unique(fnames, return_index=True)
	#print indices.shape, type(indices)
	dupes = [int(item) for item in ids if int(item) not in list(indices)]
	print dupes


class Settings():
  
  @staticmethod
  def getConstants():
    ret = Settings()
    ret.band = sys.argv[3]
    ret.dataDir = '../data/'    
    ret.listFile = ret.dataDir+'/SDSS_photo_match.csv'  
    ret.simpleFile = ret.dataDir+'/CALIFA_mother_simple.csv'
    ret.maskFile = ret.dataDir+'maskFilenames.csv'
    ret.outputFile = ret.dataDir+'/gc_out.csv'
    ret.imgDir = 'img/'
    ret.outputFile = ret.dataDir+'/gc_out.csv'
    ret.dbDir = '../db/'    
    ret.lim_lo = int(sys.argv[1])
    ret.lim_hi = int(sys.argv[2])
    return ret
    

  @staticmethod
  def getFilterNumber():
  	if Settings.getConstants().band == 'u':
  		return 0
  	elif Settings.getConstants().band == 'g':
  		return 1
  	elif Settings.getConstants().band == 'r':
  		return 2
  	elif Settings.getConstants().band == 'i':
  		return 3
  	elif Settings.getConstants().band == 'z':
  		return 4
  			

def doFitting(galaxyList):
    for i in galaxyList:
      i = int(i) - 1
      band = Settings.getConstants().band      
      try:
	  print 'filename', GalaxyParameters.getSDSSUrl(i)
	  print 'filledFilename', GalaxyParameters.getFilledUrl(i, band)
	  print i, 'i'
	  output = Photometry.calculateGrowthCurve(i)
	  #utils.writeOut(output, band+'_log'+str(Settings.getConstants().lim_lo)+'.csv')
      except IOError as err:
	  print 'err', err
	  output = [str(i+1), 'File not found', err]
	  utils.writeOut(output, band+'_skyFitErrors.csv')
	  pass   
  
def splitList(galaxyRange, chunkNumber):
    #Get the number of IDs in a chunk we want
    n = int(math.floor(len(galaxyRange)/chunkNumber)) + 1
    print n, 'length of a chunk'
    return [galaxyRange[i:i+n] for i in range(0, len(galaxyRange), n)]

def getMissing():
  ready_ids = np.genfromtxt("sky_fits_r_new.csv", delimiter=",", dtype='i')[:, 0]
  print ready_ids
  missing_ids = []
  for califa_id in range(1, 940):
    if califa_id not in ready_ids:
      missing_ids.append(califa_id)
  return sorted(missing_ids)    
    

def main():
  iso25D = 40 / 0.396
  #getMissing()
  #exit()
  fitsdir = Settings.getConstants().dataDir+'SDSS'+Settings.getConstants().band
  #getting list of CALIFA IDS to work with
  galaxyRange = range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi)
  
  #OR:
  #getting list of missing galaxy IDs:
  #galaxyRange = getMissing()
  chunks = 6
  for galaxyList in splitList(galaxyRange, chunks):
    #print len(galaxyList), 'length of a list of IDs'
    print galaxyList
    p = multiprocessing.Process(target=doFitting, args=[galaxyList])
    p.start()
   
if __name__ == "__main__":
  main()


