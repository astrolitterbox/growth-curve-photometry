# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
#import Interpol
#import getImages
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
import sdss as sdss
import imtools
import plot_survey as plot
#import photometry as phot
import readAtlas
import ellipse
import db

import plotGrowthCurve		
from math import isnan
import scipy.misc 
import sys
from galaxyParameters import *
import cProfile
import multiprocessing
#from do_GC_photometry import calculateFlux
import getTSFieldParameters


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
    #print Astrometry.distance2origin(0,0, center), 'squared distance to origin'
    distances = Astrometry.distance2origin(img.shape, center)
    #for i in range(0, img.shape[0]):
    #  for j in range(0, img.shape[1]):
#	distances[i,j] = Astrometry.distance2origin(i,j, center)
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
  def initFluxData(inputImage, center, distances):
	    print np.max(distances)

	    fluxData = np.empty((np.max(distances), 5))
	    fluxData[0,0] = 0 #isoA
	    fluxData[0,1] = inputImage[center] #currentFlux
	    fluxData[0,2] = 1
	    fluxData[0,3] = inputImage[center] #currentFluxM 
	    fluxData[0,4] = 1 #NpixM


	    return fluxData
  
  
  
  @staticmethod
  def setLimitCriterion(i, band):
    skySD = Photometry.getSkyParams(i, band).skySD
    C = 0.00005
    return C*skySD
      
 

  
  @staticmethod
  def buildGrowthCurve(name, center, distances, pa, ba, inputImage, mask, isoA_max):
		band = Settings.getConstants().band
		#masked input array
		inputImageM = np.ma.masked_array(inputImage, mask=mask)
		ellipseMask = np.zeros((inputImage.shape), dtype=np.uint8)
		ellipseMaskM = ellipseMask.copy()
		fluxData = Photometry.initFluxData(inputImage, center, distances)
		#currentPixels = center
		#currentFlux = inputImage[center] 

		Npix = 1 #init
		growthSlope = 200 #init
		md = np.max(distances)
		#print md, 'MD'
		for isoA in range(1, min(int(isoA_max), int(md))):

		  #draw ellipse for all pixels:
		  currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
		  #Npix = inputImage[currentPixels].shape[0]
		  #currentFlux = np.sum(inputImage[currentPixels])
		  ellipseMask[currentPixels] = 1
		  Npix = inputImage[currentPixels].shape[0]

		  #draw ellipse for masked pixels only:
		  currentPixelsM = ellipse.draw_ellipse(inputImageM.shape, center[0], center[1], pa, isoA, ba)
		  ellipseMaskM[currentPixelsM] = 1
		  maskedPixels = inputImageM[np.where((ellipseMaskM == 1) & (mask == 0))]
		  #print np.sum(maskedPixels), np.sum(inputImage[np.where(ellipseMask == 1)])

		  fluxData[isoA, 0] = isoA
		  fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)])# cumulative flux
		  fluxData[isoA, 2] = inputImage[np.where(ellipseMask == 1)].shape[0]

		  fluxData[isoA, 3] = np.sum(maskedPixels)# - maskedPixels.shape[0]*sky# cumulative flux, without masked pixels
		  fluxData[isoA, 4] = maskedPixels.shape[0]
		  #print Npix, NpixM, fluxData[isoA, 2], fluxData[isoA, 4]
		  isoA = isoA +1
		  #gc_sky = np.mean(fluxData[isoA-width:isoA-1, 2])
		#flux = np.sum(inputImage[np.where(ellipseMask == 1)]) - sky*inputImage[np.where(ellipseMask == 1)].shape[0]	
		fluxData = fluxData[0:isoA-1,:] 
		#fluxData[:, 3] = fluxData[:, 3] - fluxData[isoA-1, 4]*sky
		#print fluxData[isoA-1, 4], 'no pix'
		#fluxData[:, 3] = np.cumsum(fluxData[:, 3])
		#fluxData[:, 1] = np.cumsum(fluxData[:, 1])
		#the last isoA value was incremented, so it should be subtracted
		#fluxData[:, 1] = fluxData[:, 1] - sky*fluxData[:, 5]#cumulative flux, _sky_subtracted
		#fluxData[:, 3] = fluxData[:, 3] - sky*fluxData[:, 4]
		#fluxData[:, 2] = fluxData[:, 2] - sky #sky-subtracted flux per pixel
		  #print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
		  # --------------------------------------- writing an ellipse of counted points, testing only
		plotGrowthCurve.plotGrowthCurve(fluxData, Settings.getConstants().band, name)
		#hdu = pyfits.PrimaryHDU(ellipseMask)
		#hdu.writeto('vimos_masks/Mask'+name+"_"+Settings.getConstants().band+'.fits', clobber=True)
		np.savetxt('vimos_growth_curves/el/'+Settings.getConstants().band+'/gc_profile_el_new_'+name+'.csv', fluxData)	
  
  @staticmethod
  def checkLimitCriterion(fluxData, distance, limitCriterion, width):
    out = 0
    try:      
      n = fluxData[distance-width:distance+1, 3].shape[0]
      nPix = np.sum(fluxData[distance-width:distance+1, 5])
      slope = np.sum(np.abs(fluxData[distance-width:distance+1, 3]))/nPix
      #print 'slope: ', slope, 'limit: ', limitCriterion, distance, 'dist'
      
      if slope <= limitCriterion:
        mean = np.mean(fluxData[distance-width:distance+1, 2])
	print 'limit reached!', distance, nPix, mean, 'mean'
	out = 1
    except IndexError as e:
      print 'indexError', distance, e
      out = 0
    return out  

  @staticmethod
  def getFluxRatio(i, band):
    ret = Photometry()
    ret.fluxRatio = 0.5*np.sum(Photometry.getInputFile(i, band))/np.sum(Photometry.getInputFile(i, 'r'))
    return ret
    


  @staticmethod
  def getSkyParams(i, band):
    ret = Photometry()
    inputImage = Photometry.getInputFile(i, band)
    distances = Photometry.createDistanceArray(i)
    sky = inputImage[np.where(distances > 2*int(round(Photometry.iso25D)))]
    ret.skyMean = np.mean(sky)   
    ret.skySD = np.std(sky)
    return ret
    
  @staticmethod
  def calculateGrowthCurve(name, ba, pa, isoA_max, sky):
    band = Settings.getConstants().band
    imgName = 'vimos/sdss/SDSS/'+name+"/galaxy_"+Settings.getConstants().band+'_large.fits'
    dataFile = pyfits.open(imgName)
    img = dataFile[0].data
    img = img - sky
    try:
    	mask = pyfits.open('vimos/sdss/SDSS/'+name+"/mask_large.fits")[0].data
    except IOError:
        mask = np.zeros(img.shape)
    center = Photometry.getCenter(img)
    distances = Astrometry.makeDistanceArray(img, center)
    
    print 'Input shape:', img.shape, ' Max distance: ', np.max(distances)	
    Photometry.buildGrowthCurve(name, center, distances, pa, ba, img, mask, isoA_max)
    



class Settings():
  
  @staticmethod
  def getConstants():
    ret = Settings()
    ret.lo = sys.argv[1]
    ret.hi = sys.argv[2]
    ret.band = sys.argv[3]
    ret.dataDir = '../data/'    
    ret.listFile = ret.dataDir+'/SDSS_photo_match.csv'  
    ret.simpleFile = ret.dataDir+'/CALIFA_mother_simple.csv'
    ret.maskFile = ret.dataDir+'maskFilenames.csv'
    ret.outputFile = ret.dataDir+'/gc_out.csv'
    ret.imgDir = 'img/'
    ret.dbDir = '../db/'

    return ret




def getFluxUnderMask(i):
  band = Settings.getConstants().band
  maskFilename = 'masks/ellipseMask'+str(i+1)+'.fits'
  image = Photometry.getInputFile(i, band)
  print image.shape
  imageR = Photometry.getInputFile(i, 'r')
  ellipseMaskFile = pyfits.open(maskFilename)
  ellipseMask = ellipseMaskFile[0].data
  ellipseMask = getCroppedMask(ellipseMask, i)
  print ellipseMask.shape
  galaxy = image[np.where(ellipseMask == 1)]
  fluxInEllipse = np.sum(galaxy)
  sky = getEllipticalSky(image, i)
  Npix = galaxy.shape[0]
  skySubFlux = fluxInEllipse - Npix*sky
  mag =  calculateFlux(skySubFlux, i-1)
  ellipseMaskFile.close()
  return mag, sky
  
def measureFluxInOtherBands(galaxyList):
    band = Settings.getConstants().band
    out = []
    for i in galaxyList:
	i = int(i) - 1
	try:	    
	    print 'filledFilename', GalaxyParameters.getFilledUrl(i, band)
	    mag, sky = getFluxUnderMask(i)
	    out.append((i+1, mag, sky))
	except IOError as err:
	  print 'err', err
	  output = [str(i+1), 'File not found', err]
	  utils.writeOut(output, "ellipseErrors.csv")
	  pass   
    np.savetxt("gc_ellmask_"+band+".csv", out, fmt="%s, %f, %f")


def main():
  mags = []
  data = np.genfromtxt("vimos/sdss/ba_pa_values.csv", delimiter=",", dtype='object')
  names = data[:, 0]
  band = Settings.getConstants().band
  res = np.genfromtxt("vimos_sky2_"+band+"_ell.csv", delimiter=",", dtype='object')
  sky_values = res[:, 3]
  isoA_values = res[:, 5]
  for i, galaxy in enumerate(names):
    #if i < 24:
    #	    continue
    ba = np.float(data[i, 1])
    pa = np.float(data[i, 2]) + 90
    sky = np.float(sky_values[i])
    isoA = np.float(isoA_values[i])
    print isoA, galaxy, sky
    Photometry.calculateGrowthCurve(galaxy, ba, pa, isoA, sky)
    #exit()
   
if __name__ == "__main__":
  main()


