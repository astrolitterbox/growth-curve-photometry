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
from sgolay2d import sgolay2d
import readAtlas
#from  circle import drawEllipse
import db 
import ellipse
from utils import convert
  
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
    WCS=astWCS.WCS(GalaxyParameters.getSDSSUrl(listFile, dataDir, ID))
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
      errmsg = 'file already exists!', dataDir+'/filled/'+outputFilename
      print errmsg
      log.append(errmsg)
    return log
    
    
class Photometry():
  	

  @staticmethod
  def getCenter(listFile, i, dataDir):
  	   ra = Astrometry.getCenterCoords(listFile, i)[0]
	   dec = Astrometry.getCenterCoords(listFile, i)[1]
  	   return Astrometry.getPixelCoords(listFile, i, dataDir)
  @staticmethod
  def createDistanceArray(listFile, i, dataDir, center):
    print 'center coords', center, 'coords', center[1], center[0]
    inputImage = Photometry.getInputFile(listFile, dataDir, i)
    distances = Astrometry.makeDistanceArray(inputImage, Astrometry.getPixelCoords(listFile, i, dataDir))
    return distances
  @staticmethod
  def compareWithSDSS(listFile, dataDir, i):
   ra = Astrometry.getCenterCoords(listFile, i)[0]
   dec = Astrometry.getCenterCoords(listFile, i)[1]
   print ra, dec, 'ra, dec'
   band = 'r'
   return sdss.get_sdss_photometry([ra, dec, band, 10])
  @staticmethod
  def circleContours(inputFile, distances, center, iso25D):
    iso25D = round(iso25D, 1)
    print 'aa', distances.shape
    circleLength = len(inputFile[np.where(distances == iso25D)])
    print circleLength, 'clen'	
    circle.drawOuterLimit(circleLength, center[0], center[1], iso25D)  
  @staticmethod
  def ellipseContours(y0, x0, pa, isoA, axisRatio, nPoints):
	#ellipseY, ellipseX = ellipse.draw_ellipse(y0, x0, pa, isoA, axisRatio, nPoints)
	ellipseY, ellipseX = ellipse.draw_ellipse(y0, x0, pa, 60, 0.5, nPoints)
	return (ellipseY, ellipseX)
	
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
    print 'i', i

    
    #fit_sky_rows = sgolay2d(inputImage, 51, 1, 'row')
    
    #hdu = pyfits.PrimaryHDU(fit_sky_rows)
    #hdu.writeto('fit_sky_row.fits')
    fluxData = np.empty((np.max(distances), 4))
    sky = inputImage[np.where(distances > int(round(Photometry.iso25D)))]	
   
    skyMean = np.mean(sky)    
    cumulativeFlux = inputImage[center[1], center[0]] - skyMean #central pixel, sky subtracted
    
    distance = 1
    oldFlux = inputImage[center[1], center[0]]
    growthSlope = 200
    meanFlux = inputImage[center[1], center[0]]
    print 'central flux', meanFlux

    print np.where(distances > int(round(Photometry.iso25D)))[0].shape, 'np.where(distances > int(round(iso25D)))[0].shape'
    print skyMean, 'skyMean'
    
    sky_rms = np.sqrt(np.sum(sky**2)/len(sky))
    print sky_rms, 'sky rms'
    while abs(growthSlope) > sky_rms:
    #while distance < 300:
      print 'SLOPE:', growthSlope
      print '\n sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
      print 'distance', distance
      currentPixels = np.where(distances == distance)
      Npix = len(inputImage[currentPixels])
      print 'Npix', Npix
      #oldFlux = meanFlux
      currentFlux = np.sum(inputImage[currentPixels])
      currentFluxSkysub = currentFlux - (Npix*skyMean)
      growthSlope = ((currentFlux - oldFlux)/(distance - (distance - 1))/Npix)
      cumulativeFlux = cumulativeFlux+currentFluxSkysub
      print 'cumulative Flux', cumulativeFlux      
      meanFlux = currentFluxSkysub/Npix
      print 'meanFlux', meanFlux
      totalNpix = len(inputImage[np.where(distances < distance)])
      #  print 'oldFlux - meanFlux', oldFlux - meanFlux
      rms = np.sqrt((np.sum(inputImage[currentPixels]**2))/Npix)/Npix
      print rms, 'rms'
      stDev = np.sqrt(np.sum((inputImage[currentPixels] - meanFlux)**2)/Npix)/Npix
      print stDev, 'stDev'
      fluxData[distance, 0] = distance
      fluxData[distance, 1] = cumulativeFlux
      fluxData[distance, 2] = (cumulativeFlux)/totalNpix
      fluxData[distance, 3] = currentFluxSkysub/Npix
      distance = distance +1
    fluxData = fluxData[0:distance,:] 
    totalNpix = len(inputImage[np.where(distances < distance)])
    totalFlux = np.sum(inputImage[np.where(distances < distance)]) - totalNpix * skyMean - inputImage[center[1], center[0]]
    print totalFlux, 'totalFlux'
    print totalNpix, 'total Npix'
    skysub = np.mean(inputImage[np.where(distances < distance)])
    print np.mean(skysub), 'np.mean(skysub)'
    print head['EXPTIME'], 'head[EXPTIME]'
    print head['NAXIS1'], 'NAXIS1'
    print 'head[FLUX20]', head['FLUX20']
    fluxRatio2 = totalFlux/(10**8 * head['FLUX20'])
    fluxRatio = totalFlux/(53.9075*10**(-0.4*(-23.98+0.07*1.19)))
    mag = -2.5 * np.log10(fluxRatio)
    mag2 = -2.5 * np.log10(fluxRatio2)
    print 'full magnitude', mag, 'flux 20 mag', mag2
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'r', 'best')
    currentFluxSkySubPPData = plot.GraphData(((fluxData[:,0], fluxData[:,2])), 'b', 'best')
    currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,3])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], "Sky subtracted cumulative Flux", plot.PlotTitles("Sky subtracted cumulativeFlux", "distance", "Flux"))
    graph.plotScatter([currentFluxSkySubPPData], "Sky subtracted cumulative flux per pixel", plot.PlotTitles("cumulative_flux_skysub_per_pixel", "distance", "Flux per pixel"))
    graph.plotScatter([currentFluxData], "Sky subtracted flux per pixel", plot.PlotTitles("flux_per_pixel", "distance", "Flux per pixel"))
    
    
    
def main():
  dbFile = '/home/opit/Desktop/PhD/CALIFA/data/CALIFA.sqlite'
  iso25D = 40 / 0.396
  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  simpleFile = '../data/CALIFA_mother_simple.csv'
  maskFile = '../data/maskFilenames.csv'
  noOfGalaxies = 939
  i = 0

  
  
  ra = convert(db.dbUtils.getFromDB('ra', dbFile, 'mothersample', ' where CALIFA_id = 1'))
  dec = convert(db.dbUtils.getFromDB('dec', dbFile, 'mothersample', ' where CALIFA_id = 1'))
  
  print ra, dec
  #exit()
  x0 = Astrometry.getPixelCoords(listFile, 0, dataDir)[1]
  y0 = Astrometry.getPixelCoords(listFile, 0, dataDir)[0]
  print 'pixel coords', y0, x0
  sdssPA = convert(db.dbUtils.getFromDB('isoPhi_r', dbFile, 'mothersample', ' where CALIFA_id = 1'))
  sdss_ba = convert(db.dbUtils.getFromDB('isoB_r', dbFile, 'mothersample', ' where CALIFA_id = 1'))/convert(db.dbUtils.getFromDB('isoA_r', dbFile, 'mothersample', ' where CALIFA_id = 1'))
  sdss_isoA = convert(db.dbUtils.getFromDB('isoA_r', dbFile, 'mothersample', ' where CALIFA_id = 1'))
  
  nadinePA = convert(db.dbUtils.getFromDB('PA', dbFile, 'nadine', ' where CALIFA_id = 1'))
  print nadinePA, 'pa'
  nadine_ba = convert(db.dbUtils.getFromDB('ba', dbFile, 'nadine', ' where CALIFA_id = 1'))
  nadineR_90 = convert(db.dbUtils.getFromDB('R90', dbFile, 'nadine', ' where CALIFA_id = 1'))/0.396
  print nadine_ba
  nPoints = 3000000
  
  #Photometry.createDistanceArray(listFile, i, dataDir, center)
  #Photometry.ellipseContours(x0, y0, angle, isoA, axisRatio, nPoints)
  inputFileName = '../data/filled/fpC-004152-r6-0064.fits'
  inputFile = pyfits.open(inputFileName)
  inputImage = inputFile[0].data
  inputImage[:] = 1000
  #inputImage = np.zeros((50, 50))

  print y0, x0
  ellipseCoords = np.round(Photometry.ellipseContours(y0, x0, nadinePA, nadineR_90, nadine_ba, nPoints), 0).astype('int8')
  print ellipseCoords[0], ellipseCoords[1], 'ellipseCoords'
 
  inputImage[ellipseCoords[0], ellipseCoords[1]] = 100000

  #distances = Astrometry.makeDistanceArray(inputImage, (y0, x0))

  #inputImage[np.where(distances < iso25D)] = 10000000
  #inputImage[np.where(distances == iso25D+1)] = 10000000
  #inputImage[np.where(distances == iso25D-1)] = 10000000
  #inputImage[np.where(distances == iso25D-2)] = 10000000
  head = inputFile[0].header
  hdu = pyfits.PrimaryHDU(inputImage, header = head)
  hdu.writeto('ellipse.fits')
  

  #print GalaxyParameters.getNedName(listFile, simpleFile, 0).NedName, 'url:', GalaxyParameters.getSDSSUrl(listFile, dataDir, 0)
  #print Astrometry.getCenterCoords(listFile, 0)
  #print Astrometry.getPixelCoords(listFile, 0, dataDir)
  #log = []
  #for i in range(766, 938):  
  #  print i, 'galaxy'
  #  Interpolation.runInpainting(maskFile, listFile, dataDir, i, log)  
  #  print GalaxyParameters.getSDSSUrl(listFile, dataDir, i)
  #np.savetxt('errorlog.txt', log)  
  #Photometry.calculateGrowthCurve(listFile, dataDir, 4)
  #print GalaxyParameters.getFilledUrl(listFile, dataDir, 2)
  #print Photometry.compareWithSDSS(listFile, dataDir, 4)
  #ra = float(GalaxyParameters.SDSS(listFile, 4).ra)
  #dec = float(GalaxyParameters.SDSS(listFile, 4).dec)
  
  #print readAtlas.find_mag(ra, dec)

  
if __name__ == "__main__":
  main()
