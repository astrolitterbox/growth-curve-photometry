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
import plot_survey as plot
#import photometry as phot
import readAtlas
import ellipse
import db
import getTSFieldParameters
import plotGrowthCurve		



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
    print ID, 'ID'
    WCS=astWCS.WCS(GalaxyParameters.getFilledUrl(listFile, dataDir, ID))
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
	distances[i,j] = int(round(Astrometry.distance2origin(i,j, center), 0))
    return np.sqrt(distances)



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
       print start, end, 'start and end'
       #take means of (2n - 1) elliptical annuli as input fluxes for gradient search
       startFlux = 0
       startNpix = 0
       endFlux = 0
       endNpix = 0
       gradientRingWidth = 13
       for i in range(0, gradientRingWidth):
#	    	print 'i', i
	    	startFlux += np.sum(inputImage[ellipse.draw_ellipse(center[0], center[1], pa, start-i, ba)]) - ellipse.get_ellipse_circumference(start-i, ba)*skyMean
	    	startNpix += ellipse.get_ellipse_circumference(start-i, ba)*skyMean
	    	endFlux += np.sum(inputImage[ellipse.draw_ellipse(center[0], center[1], pa, end-i, ba)]) - ellipse.get_ellipse_circumference(end-i, ba)*skyMean
	    	endNpix += ellipse.get_ellipse_circumference(end-i, ba)*skyMean
       startFlux = startFlux/startNpix
       endFlux = endFlux/endNpix
       ringLength = ellipse.get_ellipse_circumference(end-(gradientRingWidth - 1)/2, ba) 
       gradient = utils.getSlope(startFlux, endFlux, start, end)
       #skyErr = (startFlux - endFlux)/(gradientRingWidth*ringLength)
       print gradient, 'gradient'#, skyErr, 'mean flux difference per pixel'
       return gradient  #skyErr
  
  @staticmethod
  def circularFlux(inputImage, center,  distances, skyMean):
      sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
      skySD = np.std(sky)
      growthSlope = 200 #init
      oldFlux = inputImage[center[0], center[1]]
      currentFlux = inputImage[center] - skyMean	
      distance = 1
      Npix=1
      fluxData = np.empty((np.max(distances), 4))
      limitCriterion = skySD
      #while abs(growthSlope) > 0.01*skySD:
      #while distance < 120:
      while Photometry.checkLimitCriterion(fluxData, distance, limitCriterion) != 1:
	oldFlux = currentFlux
	previousNpix = Npix
	Npix = inputImage[np.where(distances==distance)].shape[0]
	currentFlux = np.sum(inputImage[np.where(distances==distance)]) - skyMean*Npix
	growthSlope = utils.getSlope(oldFlux/previousNpix, currentFlux/Npix, (distance-1), distance)
	
	fluxData[distance, 0] = distance
	fluxData[distance, 1] = np.sum(inputImage[np.where(distances<=distance)]) - skyMean*inputImage[np.where(distances<=distance)].shape[0]
	fluxData[distance, 2] = np.sum(inputImage[np.where(distances==distance)]) - skyMean*Npix
	fluxData[distance, 3] = growthSlope
	#print 'old flux', oldFlux, 'currentFlux', currentFlux, 'distance', distance, 'slope', growthSlope, 'skySD', skySD
	
	distance+=1        
      print np.sum(inputImage[np.where(distances<distance)]) - skyMean*inputImage[np.where(distances<distance)].shape[0], 'SUM'
      fluxData = fluxData[0:distance-2,:]      
      return fluxData
        
  
  @staticmethod
  def buildGrowthCurve(inputImage, center,  distances, skyMean, pa, ba, CALIFA_ID):
	    ellipseMask = np.zeros((inputImage.shape))
            sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
	    fluxData = np.empty((np.max(distances), 6))
	    currentPixels = center
	    currentFlux = inputImage[center] - skyMean	
#	    print 'center', center
	    cumulativeFlux = inputImage[center[0], center[1]] - skyMean #central pixel, sky subtracted: initialising
#	    print 'center[1]', center[1], 'center', center
	    isoA = 1 #initialising    
	    Npix = 1
	    cumulNpix = 1
	    totalNpix = 1		
	    oldFlux = inputImage[center[0], center[1]]
	    growthSlope = 200
	    meanFlux = inputImage[center[0], center[1]]
#	    print 'central flux', meanFlux
	    outputImage = inputImage
	    #print np.where(distances > int(round(Photometry.iso25D)))[0].shape, 'np.where(distances > int(round(iso25D)))[0].shape'
	    #the square root of the average of the squared deviations from the mean
	    skySD = np.std(sky)
	    sky_rms = np.sqrt(np.sum((sky-skyMean)**2)/len(sky))
#	    print 'skySD', skySD
#	    print sky_rms, 'sky rms'
	    cumulativeFlux = inputImage[center[0], center[1]]-skyMean
	    limitCriterion = 0.01*skySD
	    #while abs(growthSlope) > 1*skySD*Npix:
	    #while abs(growthSlope) > 0.01*skySD:
	    #while isoA < 120:  
	    #fluxData[1, 3] = 20 #init
	    #print 'passing array', fluxData[1, 3]
	    while Photometry.checkLimitCriterion(fluxData, isoA, limitCriterion) != 1:
	      
#	      print 'major axis', isoA
	      previousNpix = Npix
	      oldEllipseMask = ellipseMask
	      #oldFlux = np.sum(inputImage[np.where(oldEllipseMask == 1)]) - previousNpix*skyMean
	      oldFlux = currentFlux#currentFlux/previousNpix
	      currentPixels = ellipse.draw_ellipse(center[0], center[1], pa, isoA, ba)
	      ellipseMask[currentPixels] = 1
	      #print 'sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
	      Npix = inputImage[currentPixels].shape[0]      
	      totalNpix = inputImage[np.where(ellipseMask == 1)].shape[0]
	      cumulNpix = cumulNpix+ Npix
#	      print totalNpix, 'totalNpix', cumulNpix, 'sum of ellipse pixels', Npix, 'Npix'
	      previousCumulativeFlux = cumulativeFlux
	      cumulativeFlux = np.sum(inputImage[np.where(ellipseMask == 1)]) - totalNpix*skyMean		
	      meanFlux = cumulativeFlux/Npix #mean sky-subtracted flux per pixel at a certain isoA      
	      currentFlux = np.sum(inputImage[currentPixels]) - skyMean*Npix
	      currentFlux2 = cumulativeFlux - oldFlux
#	      print 'ellipse pixels flux', currentFlux, 'difference masks flux', currentFlux2
	      #if (isoA)%30==0:
	      #	outputImage[currentPixels] = 1000
	      growthSlope = utils.getSlope(oldFlux/previousNpix, currentFlux/Npix, isoA-1, isoA)
	      
	      print 'slope', growthSlope,'crit', limitCriterion, 'isoA', isoA
	      #cumulativeFlux = np.sum(inputImage[np.where(ellipseMask == 1)]) - totalNpix*skyMean
	      #print 'cumulative Flux', cumulativeFlux      
	      #print 'flux in ellipse', np.sum(inputImage[np.where(ellipseMask == 1)]) - skyMean*inputImage[np.where(ellipseMask == 1)].shape[0]
	      #print 'meanFlux', meanFlux
	      #totalNpix = len(inputImage[np.where(distances < distance)])
	      #  print 'oldFlux - meanFlux', oldFlux - meanFlux
	      #rms = np.sqrt((np.sum(inputImage[currentPixels]**2))/Npix)
	      #print rms, 'rms'
	      SN = meanFlux/skySD
	      #print 'SIGNAL TO NOISE', SN

	      #stDev = np.sqrt(np.sum((inputImage[currentPixels] - meanFlux)**2)/Npix)/Npix
	      #print stDev, 'stDev'
	      fluxData[isoA, 0] = isoA
	      fluxData[isoA, 1] = np.sum(inputImage[np.where(ellipseMask == 1)]) - skyMean*inputImage[np.where(ellipseMask == 1)].shape[0] #sky-subtracted cumulative flux
	      fluxData[isoA, 2] = currentFlux/Npix #sky-subtracted flux per pixel
	      fluxData[isoA, 3] = growthSlope#currentFluxSkysub/Npix #mean sky-subtracted flux per pixel at some isoA
	      fluxData[isoA, 4] = ellipse.get_ellipse_circumference(isoA, ba)
	      fluxData[isoA, 5] = Npix
	      #print fluxData[isoA, 2], 'cum flux pp'
	      isoA = isoA +1
	    fluxData = fluxData[0:isoA-2,:] #due to indexing and the last isoA value was incremented, so it should be subtracted 
	    print 'writing...'
	    outputImage[currentPixels] = 1000
    	    hdu = pyfits.PrimaryHDU(outputImage)  		
    	    hdu.writeto('CALIFA'+CALIFA_ID+'.fits')    
	    return fluxData  
  
  @staticmethod
  def checkLimitCriterion(fluxData, distance, limitCriterion):
    out = 0
    try:
      #print 'distance length', fluxData[distance-10:distance, 3].shape
      n = fluxData[distance-4:distance+1, 3].shape[0]
      #print 'n', n
      if abs(np.sum(fluxData[distance-4:distance+1, 3])) < n*limitCriterion:
	print 'limit reached!', distance
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
#    print 'i', i
    center = Photometry.getCenter(listFile, i, dataDir)
    distances = Photometry.createDistanceArray(listFile, i, dataDir)
    #hdu = pyfits.PrimaryHDU(distances)
    #hdu.writeto('distances.fits')
    sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
    skyMean = np.mean(sky)   
    skySD = np.std(sky)
    #i+1 in the next line reflects the fact that CALIFA id's start with 1
    pa = db.dbUtils.getFromDB('PA_align', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+str(i+1))[0][0] #parsing tuples
#    print 'pa', pa
    ba = db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+str(i+1))[0][0]#parsing tuples
 #   print 'ba', ba
    
    #fluxData = Photometry.buildGrowthCurve(inputImage, center, distances, skyMean, pa, ba)
    #isoA = fluxData.shape[0]
    isoA = 180
    print 'starting to calculate sky gradient...'	
    print 'isoA', isoA -1

    start = isoA-3 + 50
    end = Photometry.findClosestEdge(distances, center)
    
    print 'old sky mean', skyMean
    
    skyErr = 1 #init
    while skyErr > 0.1*skySD:
    	skyErr = Photometry.getSkyGradient(start, end, center, inputImage, pa, ba, skyMean)
    	skyMean -= skyErr
 	print skyMean, 'skyMean'    

   
    print 'old sky mean', skyMean, 'building the GC with new skyMean', skyMean   	
    fluxData = Photometry.buildGrowthCurve(inputImage, center, distances, skyMean, pa, ba, CALIFA_ID)
  
    
    #print 'start HLR debug...'
    #print fluxData[:,-1], 'cumulativeFlux'
    
    #totalNpix = np.sum(fluxData[5])
    
    totalFlux = fluxData[fluxData.shape[0]-1, 1]   
    
    
    '''
    print 'CIRCULAR APERTURE'
    circFluxData = Photometry.circularFlux(inputImage, center,  distances, skyMean)  
    circRadius = circFluxData.shape[0]
    
    fluxInCirc = np.sum(inputImage[np.where(distances <= circRadius)]) - skyMean*(inputImage[np.where(distances <= circRadius)]).shape[0]
    
    circHLR = np.where(np.round(circFluxData[:,1]/fluxInCirc, 1) == 0.5)[0]
    print 'circle HLR', circHLR
    halfLightRadius = fluxData[np.where(np.round(fluxData[:, 1]/totalFlux, 1) == 0.5)[0]][0][0]
    
    #print fluxData[:, 1]/totalFlux    
    print halfLightRadius, "halfLightRadius", np.where(np.round(fluxData[:, 1]/totalFlux, 1) == 0.5)
    
    
    #circFluxData[circFluxData.shape[0]-1, 1] 
    #print 'circRadius', circRadius, 'fluxInCirc', fluxInCirc 
    
    print Photometry.calculateFlux(fluxInCirc, listFile, i), 'circular aperture'
    
    '''
    print Photometry.calculateFlux(totalFlux, listFile, i), 'elliptical mag'
    
    plotGrowthCurve.plotGrowthCurve(fluxData)
    exit()

    
    
    print 'flux in circ apert', fluxInCirc/totalFlux, 'ratio'    
    plotGrowthCurve.plotGrowthCurve(fluxData)
    #inputImage[currentPixels] = 1000	
    exit()
    
    #elliptical mask for total magnitude
    hdu = pyfits.PrimaryHDU(ellipseMask)

    hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')
    inputImage[halfLightRadius] = 1000
    #Reff =  np.where(distances == (np.round(10/Photometry.pixelScale, 0)))
 
    #inputImage[Reff] = 0
    
    #totalNpix = len(inputImage[np.where(distances < distance)])
    
    #totalFlux = np.sum(inputImage[np.where(distances < distance)]) - totalNpix * skyMean - inputImage[center[1], center[0]]
    #print totalFlux, 'totalFlux'
    #print totalNpix, 'total Npix'
    #skysub = np.mean(inputImage[np.where(distances < distance)])
    #print np.mean(skysub), 'np.mean(skysub)'
    #print head['EXPTIME'], 'head[EXPTIME]'
    #print head['NAXIS1'], 'NAXIS1'
    #print 'head[FLUX20]', head['FLUX20']
    #fluxRatio2 = totalFlux/(10**8 * head['FLUX20'])

    #return outputImage
    
    
def main():
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  
#  dataDir = '/media/46F4A27FF4A2713B_/work2/data'

  dataDir = '../data/'
  fitsdir = dataDir+'SDSS'
  #  fitsDir = '../data/SDSS/'
  #  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 938
  i = 1
  CALIFA_ID = str(i+1)

  img = Photometry.calculateGrowthCurve(listFile, dataDir, i)
  hdu = pyfits.PrimaryHDU(img)

  hdu.writeto('CALIFA_'+CALIFA_ID+'.fits')

if __name__ == "__main__":
  main()


