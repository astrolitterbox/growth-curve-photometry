# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
#import Interpol
#import getImages
print 'start'
import pyfits
print 'pyfits'
import math
import os
print 'os'
import string
import gzip
print 'gzip'
import csv
print 'csv'
import utils
print 'utils'
import inpaint
print 'inpaint'
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
    out = [ID, GalaxyParameters.getSDSSUrl(ID), centerCoords[0], centerCoords[1], pixelCoords[0], pixelCoords[1]]
    utils.writeOut(out, 'coords.csv')
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
    if band != 'r' or (i == 882) or (i == 576):
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
	    fluxData[0,2] = 1 #Npix
	    fluxData[0,3] = inputImage[center] #currentFluxM 
	    fluxData[0,4] = 1 #NpixM
	    return fluxData
  
  
  
  
  @staticmethod
  def setLimitCriterion(i, band):
    skySD = Photometry.getSkyParams(i, band).skySD
    C = 0.00005
    return C*skySD
      
 

  
  @staticmethod
<<<<<<< HEAD
  def buildGrowthCurve(center, distances, pa, ba, CALIFA_ID, fit_type):
 	    print 'PA, ba: ', pa, ba
	    band = Settings.getConstants().band
	    if fit_type == 'ellipse':
	    	isoA_max = Settings.getSkyFitValues(str(CALIFA_ID)).isoA
	    	sky = Settings.getSkyFitValues(str(CALIFA_ID)).sky
		
	    elif fit_type == 'circ':
	    	isoA_max = Settings.getSkyFitValues(str(CALIFA_ID)).isoA_circ
	    	sky = Settings.getSkyFitValues(str(CALIFA_ID)).sky_circ
	    print isoA_max, 'isoA'
=======
  def buildGrowthCurve(center, distances, CALIFA_ID):
	    band = Settings.getConstants().band
	    isoA_max = np.float(db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+ str(CALIFA_ID)))
	    pa = db.dbUtils.getFromDB('pa', Settings.getConstants().dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0]
	    ba = db.dbUtils.getFromDB('ba', Settings.getConstants().dbDir+'CALIFA.sqlite', 'bestBA', ' where califa_id = '+ CALIFA_ID)[0]

	    #Input array
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8
	    inputImage = Photometry.getInputFile(int(CALIFA_ID) - 1, band)
            #masked input array
	    mask = Photometry.getMask(int(CALIFA_ID)-1)           
            inputImageM = np.ma.masked_array(inputImage, mask=mask)    
	    ellipseMask = np.zeros((inputImage.shape))
	    #ellipseMaskM = ellipseMask.copy()
	    fluxData = Photometry.initFluxData(inputImage, center, distances)
	    currentPixels = center
	    currentFlux = inputImage[center] 	
<<<<<<< HEAD
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
	    print isoA_max
=======
	    
	    Npix = 1 #init
	    growthSlope = 200 #init
	    
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8
	    for isoA in range(1, int(isoA_max)+1):
	      
	      #draw ellipse for all pixels:
	      currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
      	      Npix = inputImage[currentPixels].shape[0]
	      currentFlux = np.sum(inputImage[currentPixels])
	      ellipseMask[currentPixels] = 1
	      #totalNpix = inputImage[np.where(ellipseMask == 1)].shape[0]	      
	      Npix = inputImage[currentPixels].shape[0]
	      
	      #draw ellipse for masked pixels only:     
	      currentPixelsM = ellipse.draw_ellipse(inputImageM.shape, center[0], center[1], pa, isoA, ba)
	      #ellipseMaskM[currentPixelsM] = 1
	      currentFluxM = np.sum(inputImageM[currentPixelsM])	      
	      NpixM = inputImageM[currentPixelsM].shape[0]
	      #totalNpixM = inputImageM[np.where(ellipseMaskM == 1)].shape[0]
	      #Setting the fluxData array values

	      fluxData[isoA, 0] = isoA
	      fluxData[isoA, 1] = currentFlux 	      
	      fluxData[isoA, 2] = Npix
	      fluxData[isoA, 3] = currentFluxM
	      fluxData[isoA, 4] = NpixM #Npix, excluding masked areas
	      isoA = isoA +1
	    fluxData = fluxData[0:isoA-1,:] #the last isoA value was incremented, so it should be subtracted 
	    #flux = np.sum(np.sum(fluxData[:, 3]) -  sky*np.sum(fluxData[:, 4])) #Total flux - sky*Npix, with masked areas
	    #fluxM = np.sum(np.sum(fluxData[:, 6]) -  sky*np.sum(fluxData[:, 7])) #Total flux - sky*Npix, without masked areas
	    #print flux, fluxM, 'flux, fluxM'	    
	    #fluxData[:, 1] = np.cumsum(fluxData[:, 3]) - sky*np.cumsum(fluxData[:, 4]) #cumulative flux, _sky_subtracted
	    #fluxData[:, 2] = fluxData[:, 2] - sky #sky-subtracted flux per pixel
	    #print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
	    # --------------------------------------- writing an ellipse of counted points, testing only
	    #if e:
<<<<<<< HEAD
	    #  hdu = pyfits.PrimaryHDU(output)
	    #  hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')
	    #np.savetxt('growth_curves/'+Settings.getConstants().band+'/total_gc_profile'+CALIFA_ID+'.csv', fluxData)	
	    return (flux, fluxData, sky) 
=======
	    
	    #hdu = pyfits.PrimaryHDU(ellipseMask)
            #hdu.writeto('galaxy.fits', clobber=True)	    
	    #plot the ellipse image
	    outputImage = inputImage
	    elPix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, isoA_max, ba)   
	    outputImage[elPix] = 0
	    outputImage, cdf = imtools.histeq(outputImage)
	    scipy.misc.imsave('img/new/'+Settings.getConstants().band+"/"+CALIFA_ID+".png", outputImage)

	    #Save profile
	    np.savetxt('growth_curves/new/'+Settings.getConstants().band+'/gc_profile'+CALIFA_ID+'.csv', fluxData)	
	    #return fluxData 
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8
  
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

    Photometry.buildGrowthCurve(center, distances, CALIFA_ID)
    
<<<<<<< HEAD
    # --------------------------------------- starting ellipse GC photometry

    print 'ELLIPTICAL APERTURE'
    totalFlux, fluxData, gc_sky = Photometry.buildGrowthCurve(center, distances, pa, ba, CALIFA_ID, 'ellipse')  
    elMajAxis = fluxData.shape[0]
    elMag = Photometry.calculateFlux(totalFlux, i)
    
    try:
	elHLR = fluxData[np.where(np.floor(totalFlux/fluxData[:, 1]) == 1)][0][0] - 1 #Floor() -1 -- last element where the ratio is 2
    	elR90 = fluxData[np.where(np.round(fluxData[:, 1]/totalFlux, 1) == 0.9)][0][0] 
	print elHLR  
    except IndexError as e:
        print 'err'
	elHLR = e
    
    #plotGrowthCurve.plotGrowthCurve(fluxData, Settings.getConstants().band, CALIFA_ID)
=======
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8

    #---- circular aperture	
    if band == 'r':	    
    	    print 'Circular APERTURE'
    	    totalFlux, fluxData, gc_sky = Photometry.buildGrowthCurve(center, distances, 0, 1, CALIFA_ID, 'circ')  
    	    circRadius = fluxData.shape[0]
    	    circMag = Photometry.calculateFlux(totalFlux, i)
    #	    
    	    try:
    #		print np.floor(totalFlux/fluxData[:, 1])
    		circHLR = fluxData[np.where(np.floor(totalFlux/fluxData[:, 1]) == 1)][0][0] - 1 #Floor() -1 -- last element where the ratio is 2
    		circR90 = fluxData[np.where(np.round(fluxData[:, 1]/totalFlux, 1) == 0.9)][0][0] 
    #		print circHLR  
    	    except IndexError as e:
    #		print 'err'
    		circHLR = e
		# ------------------------------------- formatting output row
#	    output = [CALIFA_ID, elMag, elHLR, circMag, circHLR, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 
 #   else:
<<<<<<< HEAD
    output = [CALIFA_ID, elMag, circMag, elHLR, elR90, circHLR, circR90, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 
=======
    #output = [CALIFA_ID, elMag, elMagMasked, elHLR, Photometry.getSkyParams(i, band).skyMean,  gc_sky] 
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8

    #print output
	
    
    # --------------------- writing output jpg file with both outermost annuli  
<<<<<<< HEAD
    outputImage = Photometry.getInputFile(int(CALIFA_ID) - 1, Settings.getConstants().band)
    #circpix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, circRadius, 1)
    elPix = ellipse.draw_ellipse(outputImage.shape, center[0], center[1], pa, elMajAxis, ba)    
    #outputImage[circpix] = 0
    outputImage[elPix] = 0
    #outputImage[circHLR] = 0
    
    outputImage, cdf = imtools.histeq(outputImage)
        
    #scipy.misc.imsave('img/output/'+CALIFA_ID+'.jpg', outputImage)    
    #scipy.misc.imsave(Settings.getConstants().imgDir+Settings.getConstants().band+'/circ_'+CALIFA_ID+'_gc.jpg', outputImage)
=======
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8

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
<<<<<<< HEAD
    ret.sky = np.float(db.dbUtils.getFromDB('sky', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+ str(CALIFA_ID))[0][0])
    ret.isoA = np.float(db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+ str(CALIFA_ID))[0][0]) - 75 #middle of the ring

    ret.sky_circ = np.float(db.dbUtils.getFromDB('sky', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_circ', ' where califa_id = '+ str(CALIFA_ID))[0][0])
    ret.isoA_circ = np.float(db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_circ', ' where califa_id = '+ str(CALIFA_ID))[0][0]) - 75 #middle of the ring
    #ret.isoA = 799
    if (CALIFA_ID == 253):
	    ret.circ_isoA = 649
    elif (CALIFA_ID == 882):
	    ret.circ_isoA = 599
=======
    ret.isoA = np.float(db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_new', 'where califa_id = '+ str(CALIFA_ID))) 
    #Sky value where masked regions were included
    #ret.skyUM = np.float(db.dbUtils.getFromDB('skyUM', Settings.getConstants().dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+ str(CALIFA_ID))[0][0])
    

>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8
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
  print 'a'
  iso25D = 40 / 0.396
  fitsdir = Settings.getConstants().dataDir+'SDSS'+Settings.getConstants().band
  band = Settings.getConstants().band
<<<<<<< HEAD
  print 'go'
  #missing = utils.convert(db.dbUtils.getFromDB('califa_id', Settings.getConstants().dbDir+'CALIFA.sqlite', band+'_flags'))
  #print missing
  #missing = np.genfromtxt('wrong_tsfield.csv', delimiter = ',', dtype = int)
  #missing = np.genfromtxt("susp_z.csv", dtype = int, delimiter = "\n")
  #print missing
  #for x, i in enumerate(missing):
  for i in range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi):
    #print i, lim_lo, lim_hi, setBand()
  #  print Settings.getConstants().band, Settings.getFilterNumber()
    i = int(i) - 1
    Astrometry.getPixelCoords(i)
    try:
      print 'filename', GalaxyParameters.getSDSSUrl(i)
      print 'filledFilename', GalaxyParameters.getFilledUrl(i, band)
      print i, 'i'
      
      #output = Photometry.calculateGrowthCurve(i)
      #utils.writeOut(out, 'centers.csv')
      #utils.writeOut(output, band+'_pht'+str(Settings.getConstants().lim_lo)+'.csv')
    except IOError as err:
      print 'err', err
      output = [str(i+1), 'File not found', err]
      utils.writeOut(output, band+'_ellipseErrors.csv')
      pass   
 
=======

  galaxyRange = range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi)
  chunks = 6
  for galaxyList in splitList(galaxyRange, chunks):
    #print len(galaxyList), 'length of a list of IDs'
    print galaxyList
    p = multiprocessing.Process(target=measure, args=[galaxyList])
    p.start()
      
      
>>>>>>> 6e37c77243e796d1b8f113abe74ccaa2de9c12a8
   
if __name__ == "__main__":
  main()


