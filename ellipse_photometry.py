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
import getTSFieldParameters
import plotGrowthCurve		
from math import isnan
import scipy.misc 
import sys
from galaxyParameters import *


#a set of methods for swapping between pixel coordinates and ra, dec

class Astrometry():
  @staticmethod
  def getCenterCoords(ID):
    centerCoords = (GalaxyParameters.SDSS(ID).ra, GalaxyParameters.SDSS(ID).dec)
    return centerCoords
  @staticmethod
  def getPixelCoords(ID):   
    #WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(ID)) #changed -- was filledUrl. I don't write coords to my masks..
    #centerCoords = Astrometry.getCenterCoords(ID)
    #print 'centerCoords', centerCoords
    #pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    #print 'pixCoords', pixelCoords
    #out = [ID, centerCoords[0], centerCoords[1], pixelCoords[0], pixelCoords[1]]
    #utils.writeOut(out, 'coords.csv')
    return (745, 1024) #y -- first, x axis -- second
  @staticmethod
  def distance2origin(y, x, center):
   deltaY = y - center[0]
   deltaX = x - center[1]
   r = (deltaY**2 + deltaX**2)
   return r
  @staticmethod
  def makeDistanceArray(img, center):
    distances = np.zeros(img.shape)
    print Astrometry.distance2origin(0,0, center), 'squared distance to origin'
    for i in range(0, img.shape[0]):
      for j in range(0, img.shape[1]):
	distances[i,j] = Astrometry.distance2origin(i,j, center)
    return np.round(np.sqrt(distances), 0)



class Photometry():
  pixelScale = 0.396
  iso25D = 40 / 0.396
  @staticmethod
  def getCenter(i):
    #ra = Astrometry.getCenterCoords(i)[0]
    #dec = Astrometry.getCenterCoords(i)[1]
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
    inputImage = Photometry.getInputFile()
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(i))
    return distances
  @staticmethod
  def getInputFile():
    #print 'filename:', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
    #inputFile = pyfits.open(GalaxyParameters.getFilledUrl(i, band))
    inputFile = pyfits.open('noisy_deVauc.fits')
    inputImage = inputFile[0].data
    #if band != 'r':
    #   inputImage-=1000 
    #print 'opened the input file'
    return inputImage
  @staticmethod    
  def getInputHeader(listFile, dataDir, i): 
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(i))	
    head = inputFile[0].header
    return head	
  @staticmethod
  def calculateFlux(flux, i):
  	tsFieldParams = getTSFieldParameters.getParams(i, Settings.getFilterNumber())
  	zpt = tsFieldParams[0]
  	ext_coeff = tsFieldParams[1]
  	airmass = tsFieldParams[2]
  	print zpt, ext_coeff, airmass, 'tsparams'    
	fluxRatio = flux/(53.9075*10**(-0.4*(zpt+ext_coeff*airmass)))
    	mag = -2.5 * np.log10(fluxRatio)
    	#mag2 = -2.5 * np.log10(fluxRatio2)
    	print 'full magnitude', mag
	return mag
  
  
  
  
  @staticmethod
  def initFluxData(inputImage, center, distances):
	    fluxData = np.empty((np.max(distances), 6))
	    fluxData[0,0] = 0
	    fluxData[0,1] = inputImage[center]
	    fluxData[0,2] = inputImage[center]
	    fluxData[0,3] = inputImage[center]
	    fluxData[0,4] = 1
	    fluxData[0,5] = 1
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
	    print sky, 'sky'
	    isoA_max = Settings.getSkyFitValues(str(CALIFA_ID)).isoA	    
	    inputImage = Photometry.getInputFile()
	    ellipseMask = np.zeros((inputImage.shape))	    
	    fluxData = Photometry.initFluxData(inputImage, center, distances)
	    currentPixels = center
	    currentFlux = inputImage[center] 	
	    isoA = 1 #initialising    
	    Npix = 1
	    totalNpix = 1		
	    oldFlux = inputImage[center[0], center[1]]
	    growthSlope = 200
	    #outputImage = inputImage
	    #limitCriterion = Photometry.setLimitCriterion(int(CALIFA_ID) - 1, band = Settings.getConstants().band)
	    #width = 20/Photometry.getFluxRatio(int(CALIFA_ID) - 1, band).fluxRatio
	    #print width, 'width'

	    #output = inputImage.copy()
	    #while Photometry.checkLimitCriterion(fluxData, isoA-1, limitCriterion, width) != 1:
	    for isoA in range(1, isoA_max+1):
	      previousNpix = Npix
	      oldFlux = currentFlux	      
	      currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
	      ellipse.getPixelEllipseLength(isoA, ba)
	      ellipseMask[currentPixels] = 1
	      Npix = inputImage[currentPixels].shape[0]      
	      totalNpix = inputImage[np.where(ellipseMask == 1)].shape[0]
	      currentFlux = np.sum(inputImage[currentPixels])
	      #output[currentPixels] = 1
	      #growthSlope = utils.getSlope(oldFlux, currentFlux, isoA-1, isoA)
	      #print 'isoA', isoA, 'Npix', Npix
	      fluxData[isoA, 0] = isoA
	      fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)])# cumulative flux
	      fluxData[isoA, 2] = currentFlux/Npix 
	      #fluxData[isoA, 3] = growthSlope/Npix
	      fluxData[isoA, 3] = currentFlux #current flux
	      fluxData[isoA, 4] = Npix
	      fluxData[isoA, 5] = totalNpix
	      isoA = isoA +1
	    #gc_sky = np.mean(fluxData[isoA-width:isoA-1, 2])
	    flux = np.sum(inputImage[np.where(ellipseMask == 1)]) -  sky*inputImage[np.where(ellipseMask == 1)].shape[0]	    
	    fluxData = fluxData[0:isoA-1,:] #the last isoA value was incremented, so it should be subtracted 
	    fluxData[:, 1] = fluxData[:, 1] - sky*fluxData[:, 5]#cumulative flux, _sky_subtracted
	    fluxData[:, 2] = fluxData[:, 2] - sky #sky-subtracted flux per pixel
	    #print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
	    # --------------------------------------- writing an ellipse of counted points, testing only
	    #if e:
	    #  hdu = pyfits.PrimaryHDU(output)
	    #  hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')
	    #np.savetxt('growth_curves/'+Settings.getConstants().band+'/total_gc_profile'+CALIFA_ID+'.csv', fluxData)	
	    return (flux, fluxData, sky) 
  
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
    inputImage = Photometry.getInputFile()
    distances = Photometry.createDistanceArray(i)
    sky = inputImage[np.where(distances > 2*int(round(Photometry.iso25D)))]
    ret.skyMean = np.mean(sky)   
    ret.skySD = np.std(sky)
    return ret
    
  @staticmethod
  def calculateGrowthCurve(i):
    CALIFA_ID = 'test_noisy_deVauc'
    band = Settings.getConstants().band
    dbDir = '../db/'
    imgDir = 'img/'+Settings.getConstants().band+'/'
    center = Photometry.getCenter(i)
    distances = Photometry.createDistanceArray(i)
    #hdu = pyfits.PrimaryHDU(distances)
    #hdu.writeto('distances.fits')

    pa = 90 #because it's so
    ba = 0.5 #db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0][0]#parsing tuples
    
    # --------------------------------------- starting ellipse GC photometry

    print 'ELLIPTICAL APERTURE'
    totalFlux, fluxData, gc_sky = Photometry.buildGrowthCurve(center, distances, pa, ba, CALIFA_ID)  
    elMajAxis = fluxData.shape[0]
    elMag = Photometry.calculateFlux(totalFlux, i)
    print 'mag', elMag
    try:
	elHLR = fluxData[np.where(np.floor(totalFlux/fluxData[:, 1]) == 1)][0][0] - 1 #Floor() -1 -- last element where the ratio is 2
	print elHLR  
    except IndexError as e:
        print 'err'
	elHLR = e
    
    #plotGrowthCurve.plotGrowthCurve(fluxData, Settings.getConstants().band, CALIFA_ID)

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
    
    output = [CALIFA_ID, elMag, elHLR, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 

    print output
	
    
    # --------------------- writing output jpg file with both outermost annuli  
    outputImage = Photometry.getInputFile()
    #circpix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, circRadius, 1)
    elPix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, elMajAxis, ba)    
    #outputImage[circpix] = 0
    outputImage[elPix] = 0
    #outputImage[circHLR] = 0
    
    outputImage, cdf = imtools.histeq(outputImage)
        
    #scipy.misc.imsave('img/output/'+CALIFA_ID+'.jpg', outputImage)    
    scipy.misc.imsave(Settings.getConstants().imgDir+Settings.getConstants().band+'/L_'+CALIFA_ID+'_gc.jpg', outputImage)

    #hdu = pyfits.PrimaryHDU(outputImage)
    #outputName = 'CALIFA'+CALIFA_ID+'.fits'
    #hdu.writeto(outputName) 
    

    
    return output
    
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
    ret.dataDir = '../data'    
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
<<<<<<< HEAD
    ret.sky = 122.94
    ret.isoA = 649
=======
    ret.sky = db.dbUtils.getFromDB('sky', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+ str(CALIFA_ID))[0][0]
    ret.isoA = db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+ str(CALIFA_ID))[0][0] - 75 #middle of the ring
>>>>>>> b5cecb5988a0c8292aad1e2fd39f671fba7b9cc6
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
  iso25D = 40 / 0.396
  #band = Settings.setBand()

 # dataDir = '/media/46F4A27FF4A2713B_/work2/data'
  fitsdir = Settings.getConstants().dataDir+'SDSS'+Settings.getConstants().band
  #  fitsDir = '../data/SDSS/'
  #  dataDir = '../data'
  band = Settings.getConstants().band
  
  #missing = np.genfromtxt('u_wrong_skies.csv', delimiter = ',', dtype = object)[:, 0]
  #print missing
  #missing = np.genfromtxt('wrong_tsfield.csv', delimiter = ',', dtype = int)
  #missing = np.genfromtxt("susp_z.csv", dtype = int, delimiter = "\n")
  #print missing
  #for x, i in enumerate(missing):
  for i in range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi):
    #print i, lim_lo, lim_hi, setBand()
    print Settings.getConstants().band, Settings.getFilterNumber()
    i = int(i) - 1
    try:
      #print 'filename', GalaxyParameters.getSDSSUrl(i)
      #print 'filledFilename', GalaxyParameters.getFilledUrl(i, band)
      #print i, 'i'
      output = Photometry.calculateGrowthCurve(i)
      utils.writeOut(output, 'test_noisy_deVauc.csv')
      #utils.writeOut(output, band+'_total_log'+str(Settings.getConstants().lim_lo)+'.csv')
    except IOError as err:
      print 'err', err
      output = [str(i+1), 'File not found', err]
      #utils.writeOut(output, band+'_ellipseErrors.csv')
      pass   
 
   
if __name__ == "__main__":
  main()


