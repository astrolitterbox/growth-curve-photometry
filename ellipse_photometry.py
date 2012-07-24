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
     sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
     return '../data/filled/'+utils.createOutputFilename(sdssFilename)
  @staticmethod
  def getMaskUrl(listFile, dataDir, simpleFile, ID):
     NedName = GalaxyParameters.getNedName(listFile, simpleFile, ID).NedName
     print NedName
     maskFile = dataDir+'/MASKS/'+NedName+'_mask_r.fits'
     return maskFile
  
  @staticmethod
  def getZeropoint(listFile, ID):
      filterNumber = 2 #(0, 1, 2, 3, 4 - ugriz SDSS filters)     
      run = GalaxyParameters.SDSS(listFile, ID).run
      rerun = GalaxyParameters.SDSS(listFile, ID).rerun
      camcol = GalaxyParameters.SDSS(listFile, ID).camcol
      field = GalaxyParameters.SDSS(listFile, ID).field
      runstr = GalaxyParameters.SDSS(listFile, ID).runstr
      field_str = GalaxyParameters.SDSS(listFile, ID).field_str
	#http://das.sdss.org/imaging/5115/40/calibChunks/2/tsField-005115-2-40-0023.fit
      print 'http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
      tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')
      print 'opened'
      img = tsFile[1].data
      head = tsFile[1].header
      zpt_r = list(img.field(27))[0][filterNumber]
      return zpt_r
	
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
    
    sky_rms = np.sqrt(np.sum(sky**2)/len(sky))
    print sky_rms, 'sky rms'    
    while abs(growthSlope) > sky_rms:
      
      currentPixels = ellipse.draw_ellipse(center[1], center[0], pa, isoA, ba)
      ellipseMask[currentPixels] = 10
      print 'SLOPE:', growthSlope
      print '\n sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
      print 'major axis', isoA
      Npix = len(inputImage[currentPixels])
      #totalNpix = totalNpix + Npix #this is actually wrong -- we may not have all the pixels at larger distances!
      totalNpix = len(inputImage[np.where(ellipseMask == 10)])
      print totalNpix
      print 'Npix', Npix
      #oldFlux = meanFlux
      currentFlux = np.sum(currentPixels)
      print 'currFL', currentFlux
      currentPixels = utils.unique_rows(inputImage[currentPixels])
      currentFlux = np.sum(currentPixels)
      print 'currFL unique', currentFlux
      currentFluxSkysub = currentFlux - (Npix*skyMean)
      growthSlope = ((currentFlux - oldFlux)/(distance - (distance - 1))/Npix)
      cumulativeFlux = np.sum(inputImage[np.where(ellipseMask == 10)]) - totalNpix*skyMean
      print 'cumulative Flux', cumulativeFlux      
      #meanFlux = currentFluxSkysub/Npix
      #print 'meanFlux', meanFlux
      #totalNpix = len(inputImage[np.where(distances < distance)])
      #  print 'oldFlux - meanFlux', oldFlux - meanFlux
      rms = np.sqrt((np.sum(inputImage[currentPixels]**2))/Npix)/Npix
      print rms, 'rms'
      #stDev = np.sqrt(np.sum((inputImage[currentPixels] - meanFlux)**2)/Npix)/Npix
      #print stDev, 'stDev'
      fluxData[isoA, 0] = isoA
      fluxData[isoA, 1] = cumulativeFlux #sky-subtracted cumulative flux
      fluxData[isoA, 2] = (cumulativeFlux)/totalNpix #sky-subtracted cumulative flux per pixel
      fluxData[isoA, 3] = currentFluxSkysub/Npix
      isoA = isoA +1
    fluxData = fluxData[0:207,:]
    print fluxData.shape
    totalFlux = cumulativeFlux
    
    fluxRatio = totalFlux/(53.9075*10**(-0.4*(-23.98+0.07*1.19)))
    mag = -2.5 * np.log10(fluxRatio)
    #mag2 = -2.5 * np.log10(fluxRatio2)
    print 'full magnitude', mag
    
    print 'start HLR debug...'
    print fluxData[1], 'cumulativeFlux'
    print totalFlux, 'totalFlux'
    
    #print fluxData[:, 1]
    #print np.round(totalFlux/fluxData[:, 1])
    
    #print np.where(np.round(totalFlux/fluxData[:, 1], 1) == 2)[0]
    
    halfLightRadius = fluxData[np.where(np.round(totalFlux/fluxData[:, 1], 1) == 2)[0]][0][0]
    print halfLightRadius, "halfLightRadius"
    
    #elliptical mask for total magnitude
    #hdu = pyfits.PrimaryHDU(ellipseMask)
    #hdu.writeto('ellipseMask.fits')

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

    #graph = plot.Plots()
    #cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'r', 'best')
    #currentFluxSkySubPPData = plot.GraphData(((fluxData[:,0], fluxData[:,2])), 'b', 'best')
    #currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,3])), 'b', 'best')
    #graph.plotScatter([cumulativeFluxData], "Sky subtracted cumulative Flux", plot.PlotTitles("Sky subtracted cumulativeFlux", "distance", "Flux"))
    #graph.plotScatter([currentFluxSkySubPPData], "Sky subtracted cumulative flux per pixel", plot.PlotTitles("cumulative_flux_skysub_per_pixel", "distance", "Flux per pixel"))
    #graph.plotScatter([currentFluxData], "Sky subtracted flux per pixel", plot.PlotTitles("flux_per_pixel", "distance", "Flux per pixel"))
    return inputImage
    
    
def main():
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 938
  i = 0


  img = Photometry.calculateGrowthCurve(listFile, dataDir, i)
  #hdu = pyfits.PrimaryHDU(img)
  #hdu.writeto('ellipse.fits')

if __name__ == "__main__":
  main()


