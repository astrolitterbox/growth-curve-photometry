

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
    pixelCoords = WCS.wcs2pix(centerCoords[0], centerCoords[1])
    return pixelCoords
  @staticmethod
  def distance2origin(y, x, center):
   deltaY = y - center[1]
   deltaX = x - center[0]
   r = np.sqrt(deltaY**2 + deltaX**2)
   return r
  @staticmethod
  def makeDistanceArray(img, center):
    distances = np.zeros(img.shape)
    print Astrometry.distance2origin(0,0, center), 'distance'
    for i in range(0, img.shape[0]):
      for j in range(0, img.shape[1]):
	distances[i,j] = int(round(Astrometry.distance2origin(i,j, center), 0))
    return distances

class Photometry():
  pixelScale = 0.396
  iso25D = 40 / 0.396
  @staticmethod
  def getCenter(listFile, i, dataDir):
    ra = Astrometry.getCenterCoords(listFile, i)[0]
    dec = Astrometry.getCenterCoords(listFile, i)[1]
    return Astrometry.getPixelCoords(listFile, i, dataDir)
  @staticmethod
  def createDistanceArray(listFile, i, dataDir):
    center = Photometry.getCenter(listFile, i, dataDir)

    print 'center coords', center, 'coords', center[1], center[0]
    inputImage = Photometry.getInputFile(listFile, dataDir, i)
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(listFile, i, dataDir))
    return distances
  @staticmethod
  def getInputFile(listFile, dataDir, i):
    print 'filename:', GalaxyParameters.getFilledUrl(listFile, dataDir, i)
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(listFile, dataDir, i))
    inputImage = inputFile[0].data
    print 'opened the input file'
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
  def calculateGrowthCurve(listFile, dataDir, i):
    inputImage = Photometry.getInputFile(listFile, dataDir, i)

    print 'i', i
    distances = Photometry.createDistanceArray(listFile, i, dataDir)
    #i+1 in the next line reflects the fact that CALIFA id's start with 1
    pa = db.dbUtils.getFromDB('PA_align', 'CALIFA.sqlite', 'nadine', ' where califa_id = '+str(i+1))[0][0] #parsing tuples
    print 'pa', pa
    
    ba = db.dbUtils.getFromDB('ba', 'CALIFA.sqlite', 'nadine', ' where califa_id = '+str(i+1))[0][0]#parsing tuples
    print 'ba', ba
    
    ellipseMask = np.zeros((inputImage.shape))
    
    fluxData = np.empty((np.max(distances), 4))
    sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]
    center = Photometry.getCenter(listFile, i, dataDir)
    print 'center', center
    skyMean = np.mean(sky)    
    cumulativeFlux = inputImage[center[1], center[0]] - skyMean #central pixel, sky subtracted: initialising
    print 'center[1]', center[1]
    
    isoA = 1 #initialising    
    distance = 1
    totalNpix = 1		
    oldFlux = inputImage[center[1], center[0]]
    growthSlope = 200
    meanFlux = inputImage[center[1], center[0]]
    print 'central flux', meanFlux

    #print np.where(distances > int(round(Photometry.iso25D)))[0].shape, 'np.where(distances > int(round(iso25D)))[0].shape'
    print skyMean, 'skyMean'
    #the square root of the average of the squared deviations from the mean
    skySD = np.std(sky)
    sky_rms = np.sqrt(np.sum((sky-skyMean)**2)/len(sky))
    print 'skySD', skySD
    print sky_rms, 'sky rms'
    cumulativeFlux = meanFlux-skyMean

    
    while abs(growthSlope) > 0.1*skySD:
    #while abs(growthSlope) > 0.01*skyMean:
    #while isoA < 400:  
      previousCumulativeFlux = cumulativeFlux
      
      currentPixels = ellipse.draw_ellipse(center[1], center[0], pa, isoA, ba)
      ellipseMask[currentPixels] = 1
      #print 'sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
      print 'major axis', isoA
      Npix = len(inputImage[currentPixels])
      
      totalNpix = len(inputImage[np.where(ellipseMask == 1)])
      #print totalNpix
      #print 'Npix', Npix
      oldFlux = meanFlux
      currentFlux = np.sum(inputImage[currentPixels])
      #print 'currFL', currentFlux

      #currentPixels = utils.unique_rows(inputImage[currentPixels])
      #currentFlux = np.sum(currentPixels)
      #print 'currFL unique', currentFlux
      currentFluxSkysub = currentFlux - (Npix*skyMean)
      cumulativeFlux = cumulativeFlux + currentFluxSkysub		
      growthSlope = (cumulativeFlux - previousCumulativeFlux)/Npix
      #print 'slope', growthSlope, 'oldFlux', oldFlux, currentFluxSkysub/Npix
      cumulativeFlux = np.sum(inputImage[np.where(ellipseMask == 1)]) - totalNpix*skyMean
      #print 'cumulative Flux', cumulativeFlux      
      meanFlux = currentFluxSkysub/Npix #mean sky-subtracted flux per pixel at a certain isoA
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
      fluxData[isoA, 1] = cumulativeFlux #sky-subtracted cumulative flux
      fluxData[isoA, 2] = (cumulativeFlux)/totalNpix #sky-subtracted cumulative flux per pixel
      fluxData[isoA, 3] = currentFluxSkysub/Npix #mean sky-subtracted flux per pixel at some isoA
      isoA = isoA +1
    fluxData = fluxData[0:isoA-2,:] #due to indexing and the last isoA value was incremented, so it should be subtracted 
    print fluxData.shape
    totalFlux = cumulativeFlux
    
    
    print Photometry.calculateFlux(totalFlux, listFile, i)
    
    print 'start HLR debug...'
    print fluxData[1], 'cumulativeFlux'
    print totalFlux, 'totalFlux'
    
    #print fluxData[:, 1]
    #print np.round(totalFlux/fluxData[:, 1])
    
    #print np.where(np.round(totalFlux/fluxData[:, 1], 1) == 2)[0]
    
    halfLightRadius = fluxData[np.where(np.round(totalFlux/fluxData[:, 1], 1) == 2)[0]][0][0] #zeroth element of fluxData, i.e. isoA. 
    print halfLightRadius, "halfLightRadius", np.where(np.round(totalFlux/fluxData[:, 1], 1) == 2)
    
    #elliptical mask for total magnitude
    hdu = pyfits.PrimaryHDU(ellipseMask)
    CALIFA_ID = str(i+1)
    hdu.writeto('ellipseMask'+CALIFA_ID+'.fits')

    inputImage[currentPixels] = 1000
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
    plotGrowthCurve.plotGrowthCurve(fluxData)	
    return inputImage
    
    
def main():
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  dataDir = '/media/46F4A27FF4A2713B_/work2/data'
  fitsdir = dataDir+'SDSS'
  #  fitsDir = '../data/SDSS/'
  #  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 938
  i = 0
  CALIFA_ID = str(i+1)

  img = Photometry.calculateGrowthCurve(listFile, dataDir, i)
  hdu = pyfits.PrimaryHDU(img)

  hdu.writeto('CALIFA_'+CALIFA_ID+'.fits')

if __name__ == "__main__":
  main()


