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
from do_GC_photometry import calculateFlux
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
		mask = getCroppedMask(mask, int(CALIFA_ID)-1)
		inputImageM = np.ma.masked_array(inputImage, mask=mask)
		ellipseMask = np.zeros((inputImage.shape), dtype=np.uint8)
		ellipseMaskM = ellipseMask.copy()
		fluxData = Photometry.initFluxData(inputImage, center, distances)
		#currentPixels = center
		#currentFlux = inputImage[center] 

		Npix = 1 #init
		growthSlope = 200 #init
		for isoA in range(1, int(isoA_max)+1):

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
		  
		  #NpixM = inputImageM[currentPixelsM].compressed().shape[0]
		  #currentFluxM = np.sum(inputImageM.filled(0)[currentPixelsM])	
		  #print Npix - NpixM, currentFlux-currentFluxM
		  
		  #growthSlope = utils.getSlope(oldFlux, currentFlux, isoA-1, isoA)
		  #print 'isoA', isoA

		  fluxData[isoA, 0] = isoA
		  fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)])# cumulative flux
		  fluxData[isoA, 2] = inputImage[np.where(ellipseMask == 1)].shape[0]

		  fluxData[isoA, 3] = np.sum(maskedPixels)# cumulative flux, without masked pixels
		  fluxData[isoA, 4] = maskedPixels.shape[0]
		  #print Npix, NpixM, fluxData[isoA, 2], fluxData[isoA, 4]
		  isoA = isoA +1
		  #gc_sky = np.mean(fluxData[isoA-width:isoA-1, 2])
		#flux = np.sum(inputImage[np.where(ellipseMask == 1)]) - sky*inputImage[np.where(ellipseMask == 1)].shape[0]	
		fluxData = fluxData[0:isoA-1,:] #the last isoA value was incremented, so it should be subtracted
		#fluxData[:, 1] = fluxData[:, 1] - sky*fluxData[:, 5]#cumulative flux, _sky_subtracted
		#fluxData[:, 3] = fluxData[:, 3] - sky*fluxData[:, 4]
		#fluxData[:, 2] = fluxData[:, 2] - sky #sky-subtracted flux per pixel
		  #print inputImage[np.where(ellipseMask == 1)].shape[0], '***************************************'
		  # --------------------------------------- writing an ellipse of counted points, testing only
		
		#hdu = pyfits.PrimaryHDU(ellipseMask)
		#hdu.writeto('masks/ellipseMask'+CALIFA_ID+'.fits', clobber=True)
		    # --------------------- writing output jpg file with both outermost annuli  
		outputImage = inputImage
		elPix = ellipse.draw_ellipse(inputImage.shape, center[0], center[1], pa, isoA-1, ba)    
		outputImage[elPix] = 0	
		outputImage, cdf = imtools.histeq(outputImage)
		scipy.misc.imsave('img/2/snapshots/'+band+"/"+CALIFA_ID+'.jpg', outputImage)
		np.savetxt('growth_curves/2/'+Settings.getConstants().band+'/gc_profile'+CALIFA_ID+'.csv', fluxData)	
  
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
    imgDir = 'img/2/'+Settings.getConstants().band+'/'
    center = Photometry.getCenter(i)
    distances = Photometry.createDistanceArray(i)
    
    e = Photometry.findClosestEdge(distances, center)
    pa = db.dbUtils.getFromDB('pa', Settings.getConstants().dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0]
    ba = db.dbUtils.getFromDB('ba', Settings.getConstants().dbDir+'CALIFA.sqlite', 'bestBA', ' where califa_id = '+ CALIFA_ID)[0]
    utils.writeOut([CALIFA_ID, e], 'closest_edge.csv')
    #Photometry.buildGrowthCurve(center, distances, pa, ba, CALIFA_ID)
    

    
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
    ret.isoA = db.dbUtils.getFromDB('isoA', Settings.getConstants().dbDir+'CALIFA.sqlite', 'gc2_'+band+"_sky", ' where califa_id = '+str(CALIFA_ID))[0]  
    #Sky value where masked regions were not included
    ret.sky = np.float(db.dbUtils.getFromDB('mSky', Settings.getConstants().dbDir+'CALIFA.sqlite', 'gc2_'+band+"_sky", ' where califa_id = '+ str(CALIFA_ID))[0])
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
  

def getMissing():
  band = Settings.getConstants().band
  missing_ids = []
  for califa_id in range(1, 940):
      try:
	with open('growth_curves/2/'+band+"/gc_profile"+str(califa_id)+".csv"): pass
      except IOError:
	missing_ids.append(califa_id)
  return sorted(missing_ids)    

def rFilename(ID):
  ID = ID+1
  fitsDir = Settings.getConstants().dataDir+'SDSS/'
  ra = GalaxyParameters.SDSS(int(ID) - 1).ra
  dec = GalaxyParameters.SDSS(int(ID) - 1).dec
  run = GalaxyParameters.SDSS(int(ID) - 1).run
  rerun = GalaxyParameters.SDSS(int(ID) - 1).rerun
  camcol = GalaxyParameters.SDSS(int(ID) - 1).camcol
  field = GalaxyParameters.SDSS(int(ID) - 1).field
  runstr = GalaxyParameters.SDSS(int(ID) - 1).runstr
  field_str = sdss.field2string(field)
  rFile = fitsDir+'r/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'
  return rFile

def getCroppedMask(mask, i):
    #WCS for u band:
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(i))   
    #WCS for r band:
    rFile = rFilename(i)
    WCSr = astWCS.WCS(rFile)
    #as in fill.py:
    band_center = WCS.wcs2pix(WCS.getCentreWCSCoords()[0], WCS.getCentreWCSCoords()[1])
    r_center = WCS.wcs2pix(WCSr.getCentreWCSCoords()[0], WCSr.getCentreWCSCoords()[1])
    shift = [band_center[0] - r_center[0], band_center[1] - r_center[1]]
    shift = [math.ceil(shift[1]), math.ceil(shift[0])]
    print shift, 'shift', band_center, r_center, 
    croppedMask = sdss.getShiftedImage(mask, shift)
    return croppedMask
    
def getEllipticalSky(image, i):
    center = Photometry.getCenter(i)
    print i
    CALIFA_ID = str(i+1)
    pa = db.dbUtils.getFromDB('pa', Settings.getConstants().dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+ CALIFA_ID)[0]
    ba = db.dbUtils.getFromDB('ba', Settings.getConstants().dbDir+'CALIFA.sqlite', 'bestBA', ' where califa_id = '+ CALIFA_ID)[0]
    isoA_max = Settings.getSkyFitValues(str(CALIFA_ID)).isoA
    start = int(isoA_max - 150)
    end = int(isoA_max)
    print start, end
    fluxData = np.empty((150, 2))
    ellipseMask = np.empty((image.shape))
    for ind, isoA in enumerate(range(start, end)):
      currentPixels = ellipse.draw_ellipse(image.shape, center[0], center[1], pa, isoA, ba)
      ellipseMask[currentPixels] = 1      
      fluxData[ind, 0] = np.sum(image[np.where(ellipseMask == 1)])# cumulative flux
      fluxData[ind, 1] = image[np.where(ellipseMask == 1)].shape[0]
    Npix = fluxData[-1,1]  
    sky = np.mean(fluxData[-1, 0]/Npix)
    return sky

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
	  utils.writeOut(output, "ellipseOtherBandErrors.csv")
	  pass   
    np.savetxt("gc_ellmask_"+band+".csv", out, fmt="%s, %f, %f")


def main():
  iso25D = 40 / 0.396
  
  band = Settings.getConstants().band

  #galaxyRange = getMissing()
  galaxyRange = range(Settings.getConstants().lim_lo, Settings.getConstants().lim_hi)
  print galaxyRange

  chunks = 8
  for galaxyList in splitList(galaxyRange, chunks):
    #print len(galaxyList), 'length of a list of IDs'
    print galaxyList
    p = multiprocessing.Process(target=measure, args=[galaxyList])
    p.start()
      
      
   
if __name__ == "__main__":
  main()


