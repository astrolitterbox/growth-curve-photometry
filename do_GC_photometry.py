#USAGE: python read_SB_profiles.py > outputFile.txt

import numpy as np
import matplotlib.pyplot as plt
import math
import db
import getTSFieldParameters
import sys 
import pyfits


#import cosm
dbDir = '../db/'
band = 'r'
dataDir = 'growth_curves/new/'+band
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

def subtractSky(sky, Npix, totalFlux):
  totalSky = sky*Npix
  return totalFlux - totalSky

mags = []
lim_lo = int(sys.argv[1])
lim_hi = int(sys.argv[2])
for i in range(lim_lo, lim_hi):
	
	#z = db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+str(i))
	#outerRadius_curr = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+str(i))[0]
	#outerRadius_r = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+str(i))[0]
	sky = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]
	skyM = db.dbUtils.getFromDB('skyMasked', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]	
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
	
	print totalFlux - totalFluxM, 'total Flux', totalNpix, totalNpixM, 'totalNpix'
	#maskFile = pyfits.open("ellipseMask6.fits")
	#mask = maskFile[0].data

	
	#totalOldNpix = np.sum(mask[np.where(mask == 1)])
	
	#print totalSky, 'sky sum', totalNpix, 'Npix'
	skySubFlux = subtractSky(sky, totalNpix, cumFlux)
	skySubFluxM = subtractSky(skyM, totalNpixM, cumFluxM)
	print skySubFlux[-1], skySubFluxM[-1], 'sky subtracted flux'
	elMag = calculateFlux(skySubFlux[-1], i)
	elMagM = calculateFlux(skySubFluxM[-1], i)  
	print elMag, elMagM
	try:
	  elHLR = data[np.where(np.round(skySubFlux/skySubFlux[-1], 1) == 0.5)][0][0] 
	except IndexError as e:
	  elHLR = e	    
	
	try:
	  elR90 = data[np.where(np.round(skySubFlux/skySubFlux[-1], 1) == 0.9)][0][0] 
	except IndexError as e:
	  elR90 = e	    
	try:
	  elHLRM = data[np.where(np.round(skySubFluxM/skySubFluxM[-1], 1) == 0.5)][0][0] 
	except IndexError as e:
	  elHLRM = e	    
	
	try:
	  elR90M = data[np.where(np.round(skySubFluxM/skySubFluxM[-1], 1) == 0.9)][0][0] 
	except IndexError as e:
	  elR90M = e	    



	print elHLR, 0.396*elHLR, elR90, 0.396*elR90
	print elHLRM, elR90M
	mags.append((i, elMag, elMagM, 0.396*elHLR, 0.396*elR90))

	
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.plot(isoA, skySubFlux, c="b")
	ax.plot(isoA, skySubFluxM, c="r")

	plt.savefig('img/curves/'+band+"/"+str(i))
	
	#fig = plt.figure()
	#old = db.dbUtils.getFromDB("r_mag", dbDir+'CALIFA.sqlite', 'gc', ' where califa_id < 100')
	#new = db.dbUtils.getFromDB("mag", dbDir+'CALIFA.sqlite', 'mags')
	#plt.scatter(old, new)
	#plt.savefig('mags_comparison')
	#sc_index = np.where(np.round(flux, 0) == round(flux[0]/math.e, 0))
        #sc_index = np.where([(np.divide(centralFlux, flux) > math.e) & (isoA > maxFluxIsoA)])[1][0] #the first index after the maximum	   
 	#lsc = isoA[sc_index]*0.396 #in arcseconds

	#phys_lsc = cosm.angular2physical(lsc, z)
	#print str(i)+","+ str(lsc)+","+ str(phys_lsc[0])+","+ str(z[0])#+","+str(maxFluxIsoA)+","+ str(lsc)# -- testing
np.savetxt("mags.csv", mags, fmt="%i,%f, %f, %f, %f")