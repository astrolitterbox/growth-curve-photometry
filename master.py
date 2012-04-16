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
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(listFile, dataDir, ID))
    centerCoords = Astrometry.getCenterCoords(listFile, ID)
    print centerCoords
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

  
#class Inpaint():  
  
class Interpolation():

  @staticmethod
  def runInpainting(maskFile, listFile, dataDir, ID, log):
    maskFilename = utils.getMask(maskFile, ID)
    sdssFilename = GalaxyParameters.getSDSSUrl(listFile, dataDir, ID)
    outputFilename = utils.createOutputFilename(sdssFilename)
    sdssImage = pyfits.open(sdssFilename)
    imageData = sdssImage[0].data
    imageData = imageData - 1000 #soft bias subtraction, comment out if needed
    head = sdssImage[0].header
    maskFile = pyfits.open(maskFilename)
    mask = maskFile[0].data
    maskedImg = np.ma.array(imageData, mask = mask)
    NANMask =  maskedImg.filled(np.NaN)
    filled = inpaint.replace_nans(NANMask, 15, 0.1, 2, 'idw')
    hdu = pyfits.PrimaryHDU(filled, header = head)
    try:
      hdu.writeto(dataDir+'/filled/'+outputFilename)
    except IOError:
      print 'file already exists!', dataDir+'/filled/'+outputFilename
      log.append(sdssFilename, outputFilename)
    return log
    
    
class Photometry():
  iso25D = 80 / 0.396
  @staticmethod
  def compareWithSDSS(listFile, dataDir, i):
   ra = Astrometry.getCenterCoords(listFile, 0)[0]
   dec = Astrometry.getCenterCoords(listFile, 0)[1]
   band = 'r'
   return sdss.get_sdss_photometry([ra, dec, band, 10])  
  @staticmethod
  def calculateGrowthCurve(listFile, dataDir, i):
    print 'input image', GalaxyParameters.getFilledUrl(listFile, dataDir, i), '\n'
    inputFile = pyfits.open(GalaxyParameters.getFilledUrl(listFile, dataDir, i))
    inputImage = inputFile[0].data
    head = inputFile[0].header
    center = Astrometry.getPixelCoords(listFile, i, dataDir)
    print 'center coords', center
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(listFile, 0, dataDir))
    fluxData = np.empty((np.max(distances), 4))
    print fluxData.shape
    cumulativeFlux = 0
    #meanFlux = inputImage[center[1], center[0]]
    distance = 0
    oldFlux = 2
    meanFlux = inputImage[center[1], center[0]]
    skyMean = np.mean(inputImage[np.where(distances > int(round(Photometry.iso25D)))])
    print np.where(distances > int(round(Photometry.iso25D)))[0].shape, 'np.where(distances > int(round(iso25D)))[0].shape'
    print skyMean, 'skyMean'
    while round(skyMean, 1) <= round(meanFlux, 1):  
      print '\n sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
      print 'distance', distance
      currentPixels = np.where(distances == distance)
      Npix = len(inputImage[currentPixels])
      print 'Npix', Npix
      #oldFlux = meanFlux
      currentFlux = np.sum(inputImage[currentPixels])
      cumulativeFlux = cumulativeFlux+currentFlux
      print 'cumulative Flux', cumulativeFlux      
      meanFlux = np.sum(inputImage[currentPixels])/Npix
      print 'meanFlux', meanFlux
    #  print 'oldFlux - meanFlux', oldFlux - meanFlux
      rms = np.sqrt((np.sum(inputImage[currentPixels]**2))/Npix)/Npix
      print rms, 'rms'
      stDev = np.sqrt(np.sum((inputImage[currentPixels] - meanFlux)**2)/Npix)/Npix
      print stDev, 'stDev'
      fluxData[distance, 0] = distance
      fluxData[distance, 1] = cumulativeFlux
      fluxData[distance, 2] = rms
      fluxData[distance, 3] = currentFlux
      distance = distance +1
    totalNpix = len(inputImage[np.where(distances < distance)])
    totalFlux = np.sum(inputImage[np.where(distances < distance)]) - totalNpix * skyMean - inputImage[center[1], center[0]]
    print totalFlux, 'totalFlux'
    print totalNpix, 'total Npix'
    skysub = np.mean(inputImage[np.where(distances < distance)])
    print np.mean(skysub), 'np.mean(skysub)'
    print head['EXPTIME'], 'head[EXPTIME]'
    print 'head[FLUX20]', head['FLUX20']
    fluxRatio2 = totalFlux/(10**8 * head['FLUX20'])
    fluxRatio = totalFlux/(53.9075*10**(-0.4*(-23.98+0.07*1.19)))
    mag = -2.5 * np.log10(fluxRatio)
    mag2 = -2.5 * np.log10(fluxRatio2)
    print 'full magnitude', mag, 'flux 20 mag', mag2
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'r', 'best')
    currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,3])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], "cumulativeFlux", plot.PlotTitles("CumulativeFlux", "distance", "Flux"))

    
    
def main():

  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 939
  
  #print GalaxyParameters.getNedName(listFile, simpleFile, 0).NedName, 'url:', GalaxyParameters.getSDSSUrl(listFile, dataDir, 0)
  #print Astrometry.getCenterCoords(listFile, 0)
  #print Astrometry.getPixelCoords(listFile, 0, dataDir)
#  log = []
#  for i in range(248, 938):  
#    print i, 'galaxy'
#    Interpolation.runInpainting(maskFile, listFile, dataDir, i, log)  
#    print GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
#  np.savetxt('errorlog.txt', log)  
  Photometry.calculateGrowthCurve(listFile, dataDir, 0)
  print GalaxyParameters.getFilledUrl(listFile, dataDir, 0)
  print Photometry.compareWithSDSS(listFile, dataDir, 0)
if __name__ == "__main__":
  main()
