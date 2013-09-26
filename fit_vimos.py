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
#import getTSFieldParameters
import plotGrowthCurve		
from math import isnan
import scipy.misc 
import sys
#from galaxyParameters import *
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
  def getCenter(image):
    y = image.shape[0]	
    x = image.shape[1]
    #if (y%2 == 1 and x%2 == 1):
    yc = y/2
    xc = x/2
    center = (yc, xc)
    return center
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
  def fitSky(center, distances, pa, ba, img, mask, name):
    #limit = findClosestEdge(distances, center)
    band = Settings.getConstants().band
    #start = Photometry.getStart(CALIFA_ID) - 500
    start = 10
    radius = 30
    step = 5
    fluxSlopeM = -10 #init
    fluxSlope = -10
    while fluxSlopeM < 0:
      fluxData = Photometry.growEllipses(img, distances, center, start, start+radius, pa, ba, mask)
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
      #print np.mean(yM), np.mean(y), start, fluxSlope, np.sum(fluxData[:, 2]), np.sum(fluxData[:, 4])  
      line = w[0]*xi+w[1] # regression line
      print fluxSlopeM, 'slope', start+radius
      start = start + step
    img_c = img.copy()
    currentPixels = ellipse.draw_ellipse(img.shape, center[0], center[1], pa, start-step, ba)
    img_c[currentPixels] = 10
    img_c, cdf = imtools.histeq(img_c)
        
    scipy.misc.imsave('vimos/img/snapshots/'+band+"/"+name+'.png', img_c)         
    return np.mean(y), fluxSlope, np.mean(yM), fluxSlopeM, fluxData[-1, 0]
   
  @staticmethod
  def growEllipses(inputImage, distances, center, start, end, pa, ba,  mask):
    fluxData = np.empty((30, 5))
    i = 0
    for isoA in range(start, end):
	      #draw ellipse for all pixels:
	      currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
      	      Npix = inputImage[currentPixels].shape[0]
	      currentFlux = np.sum(inputImage[currentPixels])
	      #draw ellipse with masks:
	      inputImageM = np.ma.masked_array(inputImage, mask=mask)
	      currentPixelsM = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
	      
	      NpixM = inputImageM[currentPixelsM].compressed().shape[0]
	      currentFluxM = np.sum(inputImageM.filled(0)[currentPixelsM])
	      
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
  def calculateGrowthCurve(name, ba, pa):
    imgName = 'vimos/sdss/SDSS/'+name+"/galaxy_"+Settings.getConstants().band+'_large.fits'
    dataFile = pyfits.open(imgName)
    img = dataFile[0].data
    try:
    	mask = pyfits.open('vimos/sdss/SDSS/'+name+"/mask_large.fits")[0].data
    	print mask.shape, img.shape
 	if mask.shape != img.shape:
		print mask.shape, img.shape, 'ALERT'
		pass

	#mask = mask/255
    except IOError:
     	mask = np.zeros(img.shape)
    center = Photometry.getCenter(img)
    distances = Astrometry.makeDistanceArray(img, center)

    
    
    # --------------------------------------- starting ellipse GC photometry
    
    print 'ELLIPTICAL APERTURE'
    try:
      #returns np.mean(y), fluxSlope, np.mean(yM), fluxSlopeM, fluxData[-1, 0]
      sky, slope, skyM, slopeM, isoA  = Photometry.fitSky(center, distances, pa, ba, img, mask, name)
    except IndexError:
      print 'aaa'
      sky = 'nan'
      slope = 'nan'
      isoA = 'nan'
      print 'aaaa'
    out = (name, sky, slope, skyM, slopeM, isoA)
    utils.writeOut(out, "vimos_sky2_"+Settings.getConstants().band+"_ell.csv")
    
    print 'Circular APERTURE --------------------------'
    try:
      #returns np.mean(y), fluxSlope, np.mean(yM), fluxSlopeM, fluxData[-1, 0]
      sky, slope, skyM, slopeM, isoA  = Photometry.fitSky(center, distances, 0, 1, img, mask, name)
    except IndexError:
      print 'aaa'
      sky = 'nan'
      slope = 'nan'
      isoA = 'nan'
      print 'aaaa'
    out = (name, sky, slope, skyM, slopeM, isoA)
    utils.writeOut(out, "vimos_sky2_"+Settings.getConstants().band+"_circ.csv")
    

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
    ret.band = sys.argv[1]
    ret.dataDir = '../data/'    
    ret.listFile = ret.dataDir+'/SDSS_photo_match.csv'  
    ret.simpleFile = ret.dataDir+'/CALIFA_mother_simple.csv'
    ret.maskFile = ret.dataDir+'maskFilenames.csv'
    ret.outputFile = ret.dataDir+'/gc_out.csv'
    ret.imgDir = 'img/'
    ret.outputFile = ret.dataDir+'/gc_out.csv'
    ret.dbDir = '../db/'    
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
  			


def main():
  

  band = sys.argv[1]
  data = np.genfromtxt("vimos/sdss/ba_pa_values.csv", delimiter=",", dtype='object')
  try:
	 res = np.genfromtxt("vimos_sky2_"+band+"_ell.csv", delimiter=",", dtype='object')
  	 res_names = res[:, 0]
  except IOError:
	  res_names = []
	  pass
  names = data[:, 0]
  for i, galaxy in enumerate(names):
    if galaxy in res_names:
      continue
    ba = np.float(data[i, 1]) 
    pa = np.float(data[i, 2]) + 90
    print i, galaxy
    Photometry.calculateGrowthCurve(galaxy, ba, pa)	
      
if __name__ == "__main__":
  main()


