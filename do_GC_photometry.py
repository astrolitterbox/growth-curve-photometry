import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import math
import db
import getTSFieldParameters
import sys 
import pyfits
import matplotlib.image as image
import matplotlib.cm as cm

plt.rc('legend',**{'fontsize':11})

#import cosm
dbDir = '../db/'
band = sys.argv[3]
dataDir = 'growth_curves/2/'+band
dataDirOld = 'growth_curves/test/'+band
'''
    # --------------------------------------- starting ellipse GC photometry

    print 'ELLIPTICAL APERTURE'
#flux, fluxM, fluxData, sky    

    elMajAxis = fluxData.shape[0]
    elMagMasked = Photometry.calculateFlux(totalMaskedFlux, i)
    try:
	elHLR = fluxData[np.where(np.floor(totalFlux/fluxData[:, 1]) == 1)][0][0] - 1 #Floor() -1 -- last element where the ratio is 2
	print elHLR  
    except IndexError as e:
        print 'err'
	elHLR = e
    
    plotGrowthCurve.plotGrowthCurve(fluxData, Settings.getConstants().band, CALIFA_ID)
'''



def calculateFlux(flux, i):
  	tsFieldParams = getTSFieldParameters.getParams(i, band)
  	zpt = tsFieldParams[0]
  	ext_coeff = tsFieldParams[1]
  	airmass = tsFieldParams[2]
  	print zpt, ext_coeff, airmass, 'tsparams'    
	fluxRatio = flux/(53.9075*10**(-0.4*(zpt+ext_coeff*airmass)))
    	mag = -2.5 * np.log10(fluxRatio)
    	#mag2 = -2.5 * np.log10(fluxRatio2)
    	print 'full magnitude', mag
	return mag

def checkMissing(dataDir, lim_lo, lim_hi):
  missing = []
  for i in range(lim_lo, lim_hi):
	try:
	  dataFile = dataDir+"/gc_profile"+str(i)+".csv"
	  d = np.genfromtxt(dataFile)
	except IOError as e:
	  missing.append(i)
  np.savetxt('missing_curves.csv', missing, fmt='%i')

def main():
  mags = []
  lim_lo = int(sys.argv[1])
  lim_hi = int(sys.argv[2])



  #checkMissing(dataDir, lim_lo, lim_hi)


  for i in range(lim_lo, lim_hi):
	  #z = db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+str(i))
	  #outerRadius_curr = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+str(i))[0]
	  #outerRadius_r = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+str(i))[0]
	  sky = db.dbUtils.getFromDB('allsky', dbDir+'CALIFA.sqlite', 'gc2_'+band+'_sky', ' where califa_id = '+str(i))[0]
	  skyM = db.dbUtils.getFromDB('mSky', dbDir+'CALIFA.sqlite', 'gc2_'+band+'_sky', ' where califa_id = '+str(i))[0]	
	  print sky, skyM
	  ##sky = 108
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
	  
	  print totalFlux, totalFluxM, 'total Flux', totalNpix, totalNpixM, 'totalNpix'
	  #maskFile = pyfits.open("ellipseMask6.fits")
	  #mask = maskFile[0].data
	  
	  skySubCumFlux = cumFlux - skyM*Npix
	  skySubCumFluxM = cumFluxM - skyM*NpixM
	  #totalOldNpix = np.sum(mask[np.where(mask == 1)])
	  
	  totalSky = totalNpix*sky
	  totalSkyM = totalNpixM*sky
	  #print totalSky, 'sky sum', totalNpix, 'Npix'
	  skySubFlux = totalFlux - totalSky
	  skySubFluxM = totalFluxM - totalSkyM
	  print skySubFlux, skySubFluxM, 'sky subtracted flux'
	  elMag = calculateFlux(skySubFlux, i-1)
	  elMagM = calculateFlux(skySubFluxM, i-1)  
	  print elMag, elMagM
	  try:
	    elHLR = data[np.where(np.round(skySubCumFlux/skySubCumFlux[-1], 1) == 0.5)][0][0] 
	  except IndexError as e:
	    elHLR = e      
	  try:
	    elHLRM = data[np.where(np.round(skySubCumFluxM/skySubCumFluxM[-1], 1) == 0.5)][0][0] 
	  except IndexError as e:
	    elHLRM = e  
	  try:
	    elR90 = data[np.where(np.round(skySubCumFlux/skySubCumFlux[-1], 1) == 0.9)][0][0] 
	  except IndexError as e:
	    elR90 = e
	  try:
	    elR90M = data[np.where(np.round(skySubCumFluxM/skySubCumFluxM[-1], 1) == 0.9)][0][0] 
	  except IndexError as e:
	    elR90M = e  	  
	    
	  print i, elMag, elMagM, elHLR, elHLRM, elR90, elR90M
	  
	  
	  out = (i, elMag, elMagM, elHLR,elHLRM, elR90, elR90M)
	  
	  #mags.append(out) 

	  
	  fig = plt.figure(figsize=(12, 12))
	  ax = fig.add_subplot(221)
	  ax.plot(isoA, skySubCumFlux, c="r", label='Total cum. flux')
	  
	  ax.plot(isoA, skySubCumFluxM, c="b", label='Total flux of unmasked pixels')
	  plt.legend(loc=8)
	  ax = fig.add_subplot(222)
	  ax.plot(isoA[1:], np.diff(skySubCumFlux), c="r", label='Total flux')
	  ax.plot(isoA[1:], np.diff(skySubCumFluxM), c="b", label='Total flux of unmasked pixels')
	  plt.axhline(c='k')
	  plt.legend(loc=1)
	  
  	  ax = fig.add_subplot(223)
	  ax.plot(isoA[1:], np.diff(Npix), c="r", label='Npix')
	  ax.plot(isoA[1:], np.diff(NpixM), c="b", label='No. of unmasked pixels')
	  plt.axhline(c='k')
	  plt.legend(loc=2)

	  
	  ax = fig.add_subplot(224)
	  im = image.imread('img/2/snapshots/'+band+"/"+str(i)+".jpg")
	  ax.imshow(im, cmap = cm.afmhot)
	  plt.savefig('img/2/curves_diff/'+band+"/"+str(i))
	  plt.close(fig)
	  
	  with open("mags_"+band+".csv", 'a') as f:
	    f.write(str(i)+","+str(elMag)+","+str(elMagM)+","+str(elHLR)+","+str(elHLRM)+","+str(elR90)+","+str(elR90M)+"\n")    
	  f.close()
	 
if __name__=="__main__":
  main()