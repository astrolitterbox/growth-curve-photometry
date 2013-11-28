import db
import numpy as np
import os
dbDir = '../db/'
#bands = ['u', 'g', 'r']
from itertools import chain


def flatten(listOfLists):
    "Flatten one level of nesting"
    return chain.from_iterable(listOfLists)      


def getErrors(i, band):
	  dataDir = 'growth_curves/2/'+band	  
	  #get tsField params
	  gain = db.dbUtils.getFromDB('gain_'+band, dbDir+'CALIFA.sqlite', 'field_params', ' where califa_id = '+str(i))[0]
	  dark_variance = db.dbUtils.getFromDB('dark_variance_'+band, dbDir+'CALIFA.sqlite', 'field_params', ' where califa_id = '+str(i))[0]
	  
	  #get sky
	  sky = db.dbUtils.getFromDB('allsky', dbDir+'CALIFA.sqlite', 'gc2_'+band+'_sky', ' where califa_id = '+str(i))[0]
	  skyM = db.dbUtils.getFromDB('mSky', dbDir+'CALIFA.sqlite', 'gc2_'+band+'_sky', ' where califa_id = '+str(i))[0]	
	  
	  #get HLR, R90
	  elHLR = db.dbUtils.getFromDB('elHLR', dbDir+'CALIFA.sqlite', 'gc2_'+band, ' where califa_id = '+str(i))[0]
	  elHLRM = db.dbUtils.getFromDB('elHLRM', dbDir+'CALIFA.sqlite', 'gc2_'+band, ' where califa_id = '+str(i))[0]	  
	  elR90 = db.dbUtils.getFromDB('elR90', dbDir+'CALIFA.sqlite', 'gc2_'+band, ' where califa_id = '+str(i))[0]
	  elR90M = db.dbUtils.getFromDB('elR90M', dbDir+'CALIFA.sqlite', 'gc2_'+band, ' where califa_id = '+str(i))[0]	  
	  #calculate sky error
	  sky_error = abs(sky - skyM)
	  
	  #get Npix, totalFlux
	  dataFile = dataDir+"/gc_profile"+str(i)+".csv"
	  #dataFileOld = dataDirOld+"/test/gc_profile"+str(i)+".csv"
	  data = np.genfromtxt(dataFile)
	  isoA = data[:, 0]	
	  cumFlux = data[:, 1] #current flux
	  Npix = data[:, 2] #npix
	  

	  cumFluxM = data[:, 3]
	  NpixM = data[:, 4]
	  totalNpix = Npix[-1]
	  totalFlux = cumFlux[-1]
	  
	  totalNpixM = NpixM[-1]
	  totalFluxM = cumFluxM[-1]
	  
	  #print totalFlux, totalFluxM, 'total Flux', totalNpix, totalNpixM, 'totalNpix', sky_error, 'sky error', abs(sky - skyM)*totalNpix, 'sky diff' 
	  #difference between sky subtracted flux and sky - sky_err subtracted flux 
	  error_skySub = np.abs((totalFlux - skyM*totalNpix) - (totalFlux - (skyM+sky_error)*totalNpix))
	  
	  #adding 1/2 of the difference between masked and unmasked flux
	  error_mask = np.abs(0.5*((totalFlux - skyM*totalNpix) - (totalFluxM - skyM*totalNpixM)))


	  #calculate counts error (eq. 2 in the .pdf)
	  
	  err_c = np.sqrt((totalFlux/gain) + totalNpix*(dark_variance + sky_error)) +  error_skySub + error_mask
	  print err_c, 'err_c', error_skySub, 'error_sky', sky_error
	  
	  
	  #calculating magnitude error (error(mag) = 2.5 / ln(10) * error(counts) / counts, from SDSS documentation)
	  
	  err_mag = 2.5 / np.log(10) * (err_c /(totalFlux - sky*totalNpix))
	  
	  
	  
	  #calculate HLR uncertainties, in pixels!:
	  skySubCumFlux = cumFlux - skyM*Npix	    
	  skySubCumFlux_low = cumFlux - error_mask - (skyM+sky_error)*Npix	  
	  skySubCumFlux_hi = cumFlux + error_mask - (skyM-sky_error)*Npix	  
	  elHLR_diff = 0.5*abs(elHLR - elHLRM)
	  elR90_diff = 0.5*abs(elR90 - elR90M) 
    
	  try:
	    elHLR_low = data[np.where(np.round(skySubCumFlux_low/skySubCumFlux_low[-1], 1) == 0.5)][0][0] 
	    print elHLR_low, "/", elHLR	    
	    elHLR_err_low = np.abs(elHLR - elHLR_low - elHLR_diff)

	  except IndexError as e:
	    elHLR_err_low = -999

	  try:
	    elHLR_hi = data[np.where(np.round(skySubCumFlux_hi/skySubCumFlux_hi[-1], 1) == 0.5)][0][0] 
	    elHLR_err_hi = np.abs(elHLR - elHLR_hi + elHLR_diff)
	  except IndexError as e:
	    elHLR_err_hi = -999	    
  	  
	  try:
	    elR90_low = data[np.where(np.round(skySubCumFlux_low/skySubCumFlux_low[-1], 1) == 0.9)][0][0] 
	    elR90_err_low = np.abs(elR90 - elR90_low - elR90_diff)
	  except IndexError as e:
	    elR90_err_low = -999
	  try:
	    elR90_hi = data[np.where(np.round(skySubCumFlux_hi/skySubCumFlux_hi[-1], 1) == 0.9)][0][0]
	    elR90_err_hi = np.abs(elR90 - elR90_hi - elR90_diff)
	  except IndexError as e:
	    elR90_err_hi = -999	  
	    
	    #converting to arcseconds:
	    elHLR_err_low = 0.396*elHLR_err_low
	    elHLR_err_hi = 0.396*elHLR_err_
	    elR90_err_low = 0.396*elR90_err_low
	    elR90_err_hi = 0.396*elR90_err_hi

	  return [round(sky_error, 3)]
	  

with open('r_sky_GC_errors.csv', 'a') as f:
  for i in range(1, 940):
    err = []
    for band in ['r']: #0, 1, 2, 3, 4
      err_b = getErrors(i, band)
      err.append(err_b)
    #print str(i+1)+","+str(list(flatten(par)))[1:-1]+os.linesep
    f.write(str(i)+","+str(list(flatten(err)))[1:-1]+os.linesep)
    
f.close()

	  
	  
	  
	  