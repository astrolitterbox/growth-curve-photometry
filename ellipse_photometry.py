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
      camcol = GalaxyParameters.SDSS(listFile, ID).camcol
      field = GalaxyParameters.SDSS(listFile, ID).field
      field_str = GalaxyParameters.SDSS(listFile, ID).field_str
      runstr = GalaxyParameters.SDSS(listFile, ID).runstr
      fpCFile = dataDir+'/filled/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fits'
      return fpCFile
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
  


#a set of methods for swapping between pixel coordinates and ra, dec

class Astrometry():
  @staticmethod
  def getCenterCoords(listFile, ID):
    centerCoords = (GalaxyParameters.SDSS(listFile, ID).ra, GalaxyParameters.SDSS(listFile, ID).dec)
    return centerCoords
  @staticmethod
  def getPixelCoords(listFile, ID, dataDir):   
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)) #changed -- was filledUrl. I don't write coords to my masks..
    centerCoords = Astrometry.getCenterCoords(listFile, ID)
    print 'centerCoords', centerCoords
    pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    print 'pixCoords', pixelCoords
    return (pixelCoords[1], pixelCoords[0]) #y -- first, x axis -- second
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
  def getCenter(listFile, i, dataDir):
    ra = Astrometry.getCenterCoords(listFile, i)[0]
    dec = Astrometry.getCenterCoords(listFile, i)[1]
    return Astrometry.getPixelCoords(listFile, i, dataDir)
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
  def createDistanceArray(listFile, i, dataDir):
    center = Photometry.getCenter(listFile, i, dataDir)

    #print 'center coords', center, 'coords', center[0], center[1]
    inputImage = Photometry.getInputFile(listFile, dataDir, i)
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(listFile, i, dataDir))
    return distances
  @staticmethod
  def getInputFile(listFile, dataDir, i):
    #print 'filename:', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(listFile, dataDir, i))
    inputImage = inputFile[0].data
    #print 'opened the input file'
    return inputImage
  @staticmethod    
  def getInputHeader(listFile, dataDir, i): 
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(listFile, dataDir, i))	
    head = inputFile[0].header
    return head	
  @staticmethod
  def calculateFlux(flux, listFile, i):
  	tsFieldParams = getTSFieldParameters.getParams(listFile, i)
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
  def getSkyGradient(start, end, center, inputImage, pa, ba, skyMean):

       #inputIndices = utils.createIndexArray(inputImage.shape)
       #take means of (2n - 1) elliptical annuli as input fluxes for gradient search
       
       gradientRingWidth = 13

       startFlux = 0
       startNpix = 0
       endFlux = 0
       endNpix = 0       
       
       print start, end, 'start and end', skyMean, 'skyMean'   

       for i in range(0, gradientRingWidth):
		elStart = inputImage[ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, start-i, ba)]
	    	startFlux += np.sum(elStart) - elStart.shape[0]*skyMean	    	   		    	

	    	startNpix += elStart.shape[0]#ellipse.get_ellipse_circumference(start-i, ba)  #*skyMean -- WHY?	   
	    	elEnd = inputImage[ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, end-i, ba)]
	    	
	    	endFlux += np.sum(elEnd) - elEnd.shape[0]*skyMean
	    	endNpix += elEnd.shape[0]  #*skyMean -- WHY?
       
       startFlux = startFlux/startNpix
       endFlux = endFlux/endNpix
       print startFlux, 'startFlux', endFlux, 'endFlux'
       #ringLength = ellipse.get_ellipse_circumference(end-(gradientRingWidth - 1)/2, ba) 
       #gradient = utils.getSlope(startFlux, endFlux+startFlux, start, end)
       gradient = (endFlux-startFlux)/(end-start)
       #skyErr = (startFlux - endFlux)/(gradientRingWidth*ringLength)
       print gradient, 'gradient'#, skyErr, 'mean flux difference per pixel'
       return gradient  #skyErr
  

  
  @staticmethod
  def buildGrowthCurve(inputImage, center,  distances, skyMean, pa, ba, CALIFA_ID):
	    ellipseMask = np.zeros((inputImage.shape))	    
            sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
	    fluxData = np.empty((np.max(distances), 6))
	    currentPixels = center
	    currentFlux = inputImage[center] - skyMean	
	    isoA = 1 #initialising    
	    Npix = 1
	    totalNpix = 1		
	    oldFlux = inputImage[center[0], center[1]]
	    growthSlope = 200
	    outputImage = inputImage
	    skySD = np.std(sky)
	    limitCriterion = 0.01*skySD
	    while Photometry.checkLimitCriterion(fluxData, isoA-1, limitCriterion) != 1:
	      previousNpix = Npix
	      oldEllipseMask = ellipseMask
	      oldFlux = currentFlux#currentFlux/previousNpix
	      currentPixels = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA, ba)
	      ellipse.getPixelEllipseLength(isoA, ba)
	      ellipseMask[currentPixels] = 1
	      Npix = inputImage[currentPixels].shape[0]      
	      totalNpix = inputImage[np.where(ellipseMask == 1)].shape[0]
	      currentFlux = np.sum(inputImage[currentPixels]) - skyMean*Npix
	      growthSlope = utils.getSlope(oldFlux, currentFlux, isoA-1, isoA)
	      print 'isoA', isoA, 'Npix', Npix
	      fluxData[isoA, 0] = isoA
	      fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)]) - skyMean*inputImage[np.where(ellipseMask == 1)].shape[0] #sky-subtracted cumulative flux
	      fluxData[isoA, 2] = currentFlux/Npix #sky-subtracted flux per pixel
	      fluxData[isoA, 3] = growthSlope#currentFluxSkysub/Npix #mean sky-subtracted flux per pixel at some isoA
	      fluxData[isoA, 4] = ellipse.get_ellipse_circumference(isoA, ba)
	      fluxData[isoA, 5] = Npix
	      #print fluxData[isoA, 2], 'cum flux pp'
	      isoA = isoA +1
	    fluxData = fluxData[0:isoA-1,:] #due to indexing and the last isoA value was incremented, so it should be subtracted 
	    flux = np.sum(inputImage[np.where(ellipseMask == 1)]) - skyMean*inputImage[np.where(ellipseMask == 1)].shape[0]
	    print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
	    # --------------------------------------- writing an ellipse of counted points, testing only
	    #hdu = pyfits.PrimaryHDU(ellipseMask)
	    #hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')
	    print fluxData[:, 5]
	    return (flux, fluxData) 
  
  @staticmethod
  def checkLimitCriterion(fluxData, distance, limitCriterion):
    out = 0    
    try:      
      n = fluxData[distance-4:distance+1, 3].shape[0]
      nPix = np.sum(fluxData[distance-4:distance+1, 5])

      print np.sum(np.abs(fluxData[distance-4:distance+1, 3]))/nPix, 'avg', limitCriterion, 'criterion', distance, 'dist'
      if np.sum(np.abs(fluxData[distance-4:distance+1, 3]))/nPix < limitCriterion:
	print 'limit reached!', distance, nPix
	out = 1
    except IndexError as e:
      print 'indexError', distance, e
      out = 0
    return out  
  
  @staticmethod
  def calculateGrowthCurve(listFile, dataDir, i):
    CALIFA_ID = str(i+1)
    inputImage = Photometry.getInputFile(listFile, dataDir, i)
    dbDir = '../db/'

    center = Photometry.getCenter(listFile, i, dataDir)
    distances = Photometry.createDistanceArray(listFile, i, dataDir)
    #hdu = pyfits.PrimaryHDU(distances)
    #hdu.writeto('distances.fits')
    sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
    skyMean = np.mean(sky)   
    skySD = np.std(sky)
    #i+1 in the next line reflects the fact that CALIFA id's start with 1
    pa = db.dbUtils.getFromDB('PA', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0][0]  #parsing tuples
    ba = db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0][0]#parsing tuples
    #ba = 1
    #r_mag = db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0][0]#parsing tuples
    #r_e = db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0][0]#parsing tuples
    #lucy_re = db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'lucie', ' where id = '+ CALIFA_ID)[0][0]#parsing tuples
    #l_SkyMean = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'lucie', ' where id = '+ CALIFA_ID)[0][0] - 1000#parsing tuples
 #   print 'ba', ba
    
    #fluxData = Photometry.buildGrowthCurve(inputImage, center, distances, skyMean, pa, ba)
    #isoA = fluxData.shape[0]
    isoA = 230

    print 'starting to calculate sky gradient...', skySD	
    print 'isoA', isoA -1
    
    start = isoA-3 + 50

    oldSky =  skyMean
    
    end = Photometry.findClosestEdge(distances, center)
    if end < Photometry.iso25D:
      skyMean = oldSky
    elif start >= end:
      skyMean = oldSky
    else:      
      #skyErr = 1 #init
      #while abs(skyErr) > 0.001: #abs(0.01*skySD):
      skyErr = Photometry.getSkyGradient(start, end, center, inputImage, pa, ba, skyMean)
      skyMean += skyErr
      print skyMean, 'skyMean'    


    #print 'old sky mean', skyMean, 'building the GC with new skyMean', skyMean   	
    
    if  math.isnan(skyMean):
      output = ['unable to get the sky value', GalaxyParameters.getSDSSUrl(listFile, dataDir, i), GalaxyParameters.getFilledUrl(listFile, dataDir, i)]
      return output
      
    #skyMean = 131
    #oldSky = 130
    
  
    # --------------------------------------- starting GC photometry in circular annuli
    print 'CIRCULAR APERTURE'
    #circFlux, circFluxData = Photometry.circularFlux(inputImage, center,  distances, skyMean)  
    circFlux, circFluxData = Photometry.buildGrowthCurve(inputImage, center, distances, skyMean, pa, 1, str(i+1))
    circRadius = circFluxData.shape[0]
    print circRadius, 'circle radius'
    otherFlux = circFluxData[-1, 1]   
    print 'fluxes: mask:', circFlux, 'sum', otherFlux    
    try:
	    circHLR = np.where(np.round(circFluxData[:,1]/circFlux, 1) == 0.5)[0][0]
    except IndexError as e:
	    circHLR = str(e)
	    
    circMag = Photometry.calculateFlux(circFlux, listFile, i)

    
    #scipy.misc.imsave('img/output/'+CALIFA_ID+'.jpg', outputImage)    
    #scipy.misc.imsave('img/new_snapshots/'+str(i+1)+'_gc.jpg', outputImage)

    
    # --------------------------------------- starting ellipse GC photometry
    '''
    print 'ELLIPTICAL APERTURE'
    flux, fluxData = Photometry.buildGrowthCurve(inputImage, center, distances, skyMean, pa, ba, CALIFA_ID)  
    totalFlux = flux
    otherFlux = fluxData[fluxData.shape[0]-1, 1]   
    elMajAxis = fluxData.shape[0]
    #print 't', totalFlux, 'o', otherFlux
    elMag = Photometry.calculateFlux(totalFlux, listFile, i)
    try:
    	elHLR = fluxData[np.where(np.round(fluxData[:, 1]/totalFlux, 1) == 0.5)][0][0]    
    except IndexError as e:
	elHLR = e
    plotGrowthCurve.plotGrowthCurve(fluxData, CALIFA_ID)
    '''
    
    
    # --------------------- writing output jpg file with both outermost annuli  
    outputImage = inputImage
    circpix = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, circRadius, 1)
    elPix = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, circRadius, ba)    
    outputImage[circpix] = 500
    outputImage[elPix] = 500
    
    outputImage, cdf = imtools.histeq(outputImage)
        
    #scipy.misc.imsave('img/output/'+CALIFA_ID+'.jpg', outputImage)    
    scipy.misc.imsave('img/new_snapshots/fixed/'+CALIFA_ID+'_gc.jpg', outputImage)

    #hdu = pyfits.PrimaryHDU(outputImage)
    #outputName = 'CALIFA'+CALIFA_ID+'.fits'
    #hdu.writeto(outputName) 
    

    
    # ------------------------------------- formatting output row
    output = [CALIFA_ID, elMag, elHLR, circMag, circHLR, skyMean, oldSky]
    print skyMean, oldSky, 'sky'
    return output
    
    
def main():
  iso25D = 40 / 0.396

  #dataDir = '../data'
  dataDir = '/media/46F4A27FF4A2713B_/work2/data'
  fitsdir = dataDir+'SDSS'
  #  fitsDir = '../data/SDSS/'
  #  dataDir = '../data'
  listFile = dataDir+'/SDSS_photo_match.csv'
  outputFile = dataDir+'/gc_out.csv'
  imgDir = 'img/'
  simpleFile = dataDir+'/CALIFA_mother_simple.csv'
  maskFile = dataDir+'maskFilenames.csv'
  noOfGalaxies = 939
 
  #for i, x in enumerate((479, 476, 510, 486, 597, 436, 463, 163, 444, 569, 475, 766, 248, 497, 536, 615, 319, 700, 161, 266, 591, 540, 655, 136, 172, 173, 304, 512, 578, 147, 170, 185, 245, 175, 567, 706)):  
  for i in range(115, 116):    
    try:
      print 'filename', GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
      print 'filledFilename', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
      print i, 'i'
      output = Photometry.calculateGrowthCurve(listFile, dataDir, i)
      utils.writeOut(output)
    except IOError as err:
      print 'err', err
      output = [str(i+1), 'File not found', err]
      utils.writeOut(output)
      pass   
 
 
 
 
  exit()
  for i in range(88, 89):
    try:
      #print 'filename', GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
      #print 'filledFilename', GalaxyParameters.getFilledUrl(listFile, dataDir, i)

      print i, 'a'
      output = Photometry.calculateGrowthCurve(listFile, dataDir, i)
      utils.writeOut(output)
#      plotFilled(Photometry.getInputFile(listFile, dataDir, i), i)
    except IOError as err:
      print 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' 
      output = [str(i+1), 'File not found', err]
      utils.writeOut(output)
      pass

def plotFilled(inputImage, i):
    CALIFA_ID = str(i+1)
    outputImage = inputImage
    outputImage, cdf = imtools.histeq(outputImage)
    scipy.misc.imsave('img/output/fixed/'+CALIFA_ID+'_image.jpg', outputImage)
   
if __name__ == "__main__":
  main()


