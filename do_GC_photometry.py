#USAGE: python read_SB_profiles.py > outputFile.txt

import numpy as np
import matplotlib.pyplot as plt
import math
import db
import getTSFieldParameters

#import cosm
dbDir = '../db/'
band = 'r'
dataDir = 'growth_curves/new/'+band
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

for i in range(2, 3):
	#z = db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+str(i))
	#outerRadius_curr = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+str(i))[0]
	#outerRadius_r = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+str(i))[0]
	sky = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]
	skyM = db.dbUtils.getFromDB('skyMasked', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]	
	print sky, skyM
	##sky = 108
	dataFile = dataDir+"/gc_profile"+str(i)+".csv"
	data = np.genfromtxt(dataFile)
	isoA = data[:, 0]
	currentFlux = data[:, 1] #current flux
	Npix = data[:, 2] #current flux
	currentFluxM = data[:, 3] #current flux
	NpixM = data[:, 4] 
	#print np.sum(currentFlux), 'sum curr'
	#sky+= 2
	currentFlux = np.subtract(currentFlux, Npix*sky)
	
	#print np.sum(currentFlux), 'sum curr'

	#print currentFlux[1]	
	cumFlux = np.cumsum(currentFlux) 
	cumFluxM = np.cumsum(currentFlux)
	
	#totalFlux = np.sum(currentFlux) #- sky*np.sum(Npix)
	#totalFluxM = np.sum(currentFlux)# - skyM*np.sum(Npix)
	#print totalFlux, 'total'
	print cumFlux[-1], 'cum'
	
	elMag = calculateFlux(cumFlux[-1], i)
	#elMagM = calculateFlux(totalFluxM, i)
	print elMag, elMagM
	#exit()	
	fig = plt.figure()
	plt.scatter(isoA, cumFlux)
	plt.savefig('img/curves/'+band+"/"+str(i))
	#exit()
	
	#sc_index = np.where(np.round(flux, 0) == round(flux[0]/math.e, 0))
        #sc_index = np.where([(np.divide(centralFlux, flux) > math.e) & (isoA > maxFluxIsoA)])[1][0] #the first index after the maximum	   
 	#lsc = isoA[sc_index]*0.396 #in arcseconds

	#phys_lsc = cosm.angular2physical(lsc, z)
	#print str(i)+","+ str(lsc)+","+ str(phys_lsc[0])+","+ str(z[0])#+","+str(maxFluxIsoA)+","+ str(lsc)# -- testing
