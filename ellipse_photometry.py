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
import sdss_photo_check as sdss
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
  def buildGrowthCurve(center, distances, pa, ba, CALIFA_ID):
		band = Settings.getConstants().band
		sky = Settings.getSkyFitValues(str(CALIFA_ID)).sky
		isoA_max = Settings.getSkyFitValues(str(CALIFA_ID)).isoA			
		inputImage = Photometry.getInputFile(int(CALIFA_ID) - 1, band)
		#masked input array
		mask = Photometry.getMask(int(CALIFA_ID)-1)
		inputImageM = np.ma.masked_array(inputImage, mask=mask)
		ellipseMask = np.zeros((inputImage.shape), dtype=np.uint8)
		ellipseMaskM = ellipseMask.copy()
		fluxData = Photometry.initFluxData(inputImage, center, distances)
		currentPixels = center
		currentFlux = inputImage[center] 

		Npix = 1 #init
		growthSlope = 200 #init
		for isoA in range(1, int(isoA_max)+1):
		  
		  #draw ellipse for all pixels:
		  currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
		  Npix = inputImage[currentPixels].shape[0]
		  currentFlux = np.sum(inputImage[currentPixels])
		  ellipseMask[currentPixels] = 1
		  Npix = inputImage[currentPixels].shape[0]

		  #draw ellipse for masked pixels only:
		  currentPixelsM = ellipse.draw_ellipse(inputImageM.shape, center[0], center[1], pa, isoA, ba)
		  ellipseMaskM[currentPixelsM] = 1
		  
		  NpixM = inputImageM[currentPixelsM].compressed().shape[0]
		  currentFluxM = np.sum(inputImageM.filled(0)[currentPixelsM])	
		  #print Npix - NpixM, currentFlux-currentFluxM
		  
		  #growthSlope = utils.getSlope(oldFlux, currentFlux, isoA-1, isoA)
		  #print 'isoA', isoA
		  fluxData[isoA, 0] = isoA
		  fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)])# cumulative flux
		  fluxData[isoA, 2] = inputImage[np.where(ellipseMask == 1)].shape[0]

		  fluxData[isoA, 3] = np.sum(inputImageM[np.where(ellipseMaskM == 1)])# cumulative flux, without masked pixels
		  fluxData[isoA, 4] = inputImageM[np.where(ellipseMaskM == 1)].shape[0]

		  isoA = isoA +1
		  #gc_sky = np.mean(fluxData[isoA-width:isoA-1, 2])
		flux = np.sum(inputImage[np.where(ellipseMask == 1)]) - sky*inputImage[np.where(ellipseMask == 1)].shape[0]	
		fluxData = fluxData[0:isoA-1,:] #the last isoA value was incremented, so it should be subtracted
		#fluxData[:, 1] = fluxData[:, 1] - sky*fluxData[:, 5]#cumulative flux, _sky_subtracted
		#fluxData[:, 3] = fluxData[:, 3] - sky*fluxData[:, 4]
		#fluxData[:, 2] = fluxData[:, 2] - sky #sky-subtracted flux per pixel
		  #print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
		  # --------------------------------------- writing an ellipse of counted points, testing only
		  #if e:
		hdu = pyfits.PrimaryHDU(ellipseMask)
		hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')
		
		np.savetxt('growth_curves/new/'+Settings.getConstants().band+'/gc_profile'+CALIFA_ID+'.csv', fluxData)	
  
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
  def calculateGrowthCurve(i):
    CALIFA_ID = str(i+1)
    band = Settings.getConstants().band
    dbDir = '../db/'
    imgDir = 'img/'+Settings.getConstants().band+'/'
    center = Photometry.getCenter(i)
    distances = Photometry.createDistanceArray(i)
    
    pa = db.dbUtils.getFromDB('pa', Settings.getConstants().dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0]
    ba = db.dbUtils.getFromDB('ba', Settings.getConstants().dbDir+'CALIFA.sqlite', 'bestBA', ' where califa_id = '+ CALIFA_ID)[0]

    Photometry.buildGrowthCurve(center, distances, pa, ba, CALIFA_ID)
    

    #---- circular aperture	
    #if band == 'r':	    
    #	    print 'Circular APERTURE'
    #	    totalFlux, fluxData, gc_sky = Photometry.buildGrowthCurve(center, distances, 0, 1, CALIFA_ID)  
    #	    circRadius = fluxData.shape[0]
    #	    circMag = Photometry.calculateFlux(totalFlux, i)
    #	    
    #	    try:
    #		print np.floor(totalFlux/fluxData[:, 1])
    #		circHLR = fluxData[np.where(np.floor(totalFlux/fluxData[:, 1]) == 1)][0][0] - 1 #Floor() -1 -- last element where the ratio is 2
    #		print circHLR  
    #	    except IndexError as e:
    #		print 'err'
    #		circHLR = e
		# ------------------------------------- formatting output row
#	    output = [CALIFA_ID, elMag, elHLR, circMag, circHLR, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 
 #   else:
    #output = [CALIFA_ID, elMag, elMagMasked, elHLR, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 

    #print output
	
    
    # --------------------- writing output jpg file with both outermost annuli  

    #circpix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, circRadius, 1)
    #return output
    
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
    ret.dbDir = '../db/'
    ret.lim_lo = int(sys.argv[1])
    ret.lim_hi = int(sys.argv[2])
    return ret
        
  @staticmethod
  def getSkyFitValues(CALIFA_ID):
    band = Settings.getConstants().band
    ret = Settings()
    ret.isoA = db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(CALIFA_ID))[0] 
    
    #Sky value where masked regions were included
    ret.sky = np.float(db.dbUtils.getFromDB('sky', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+ str(CALIFA_ID))[0])
    

    return ret


  			

def splitList(galaxyRange, chunkNumber):
    #Get the number of IDs in a chunk we want
    n = int(math.floor(len(galaxyRange)/chunkNumber)) + 1
    print n, 'length of a chunk'
    return [galaxyRange[i:i+n] for i in range(0, len(galaxyRange), n)]

def measure(galaxyList):
  band = Settings.getConstants().band        
  for i in galaxyList:
      i = int(i) - 1
      try:
	  print 'filename', GalaxyParameters.getSDSSUrl(i)
	  print 'filledFilename', GalaxyParameters.getFilledUrl(i, band)
	  Photometry.calculateGrowthCurve(i)
      except IOError as err:
	print 'err', err
	output = [str(i+1), 'File not found', err]
	utils.writeOut(output, "ellipseErrors_new.csv")
	pass   
  


def main():
  iso25D = 40 / 0.396
  fitsdir = Settings.getConstants().dataDir+'SDSS'+Settings.getConstants().band
  band = Settings.getConstants().band

  galaxyRange = range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi)
  chunks = 6
  for galaxyList in splitList(galaxyRange, chunks):
    #print len(galaxyList), 'length of a list of IDs'
    print galaxyList
    p = multiprocessing.Process(target=measure, args=[galaxyList])
    p.start()
      
      
   
if __name__ == "__main__":
  main()


