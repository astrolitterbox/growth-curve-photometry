#USAGE: python read_SB_profiles.py > outputFile.txt

import numpy as np
import matplotlib.pyplot as plt
import math
import db
import getTSFieldParameters
import sys 

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

mags = []
lim_lo = int(sys.argv[1])
lim_hi = int(sys.argv[2])
for i in range(lim_lo, lim_hi):
	
	#z = db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+str(i))
	#outerRadius_curr = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id = '+str(i))[0]
	#outerRadius_r = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_r', ' where califa_id = '+str(i))[0]
	sky = 110#db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]
	skyM = db.dbUtils.getFromDB('skyMasked', dbDir+'CALIFA.sqlite', 'sky_new', ' where califa_id = '+str(i))[0]	
	print sky, skyM
	##sky = 108
	dataFile = dataDir+"/gc_profile"+str(i)+".csv"
	dataFileOld = dataDirOld+"/gc_profile"+str(i)+".csv"
	data = np.genfromtxt(dataFile)
	oldData = np.genfromtxt(dataFileOld)
	newSize = min(data.shape[0], oldData.shape[0])
	data = data[:newSize,:]
	oldData = oldData[:newSize,:]
	isoA = oldData[:, 0]
	
	NpixOld = oldData[:, 4]		
	isoANew = data[:, 0]	
	currentFlux = data[:, 1] #current flux
	Npix = data[:, 2] #npix
	#currentFluxM = data[:, 3] #current flux
	#NpixM = data[:, 4]
	#print currentFlux
	currentFlux = np.subtract(currentFlux, Npix*sky)
	cumFlux = np.cumsum(currentFlux) 
	
	#cumFluxOld = oldData[:, 1]
	print Npix.shape, 'npx'
	currFluxOld = (oldData[:, 3])
	
	#currFluxOld = np.subtract(currFluxOld, NpixOld*sky)
	cumFluxOld = np.cumsum(currFluxOld)
	
	
	#ell = data[:, 3]
	print cumFluxOld[-1], 'cfo'
	#sky+= 2
	#currentFlux = np.subtract(currentFlux, Npix*sky)
	
	#print np.sum(currentFlux), 'sum curr'

	#print currentFlux[1]	
	#cumFlux = np.cumsum(currentFlux) 
	#cumFluxM = np.cumsum(currentFlux)
	#print currFluxOld
	
	totalFlux = np.sum(currentFlux)
	#totalFluxM = np.sum(currentFlux)# - skyM*np.sum(Npix)
	#print totalFlux, 'total'
	#print cumFlux[-1], 'cum'
	elMagOld = calculateFlux(cumFluxOld[-1], i)
	elMag = calculateFlux(totalFlux, i)
	print elMagOld, 'old', elMag, 'now'
	#exit()	
	fig = plt.figure()
	ax = fig.add_subplot(221)
	#ax.plot(isoA, cumFluxOld, c="b")
	ax.plot(isoANew, cumFlux, c="r")

	ax = fig.add_subplot(222)
	ax.plot(isoA, cumFluxOld, c="b")	
	#ax.plot(isoANew, currentFlux, c="r")
	
	ax = fig.add_subplot(223)
	ax.plot(isoANew, Npix, c="r")
	#ax.plot(isoANew, ell, c="b")
	

	#mags.append((i, elMag))
	
	ax = fig.add_subplot(224)
	ax.plot(isoA, NpixOld, c="b")

	plt.savefig('img/curves/'+band+"/"+str(i))
	
	fig = plt.figure()
	old = db.dbUtils.getFromDB("r_mag", dbDir+'CALIFA.sqlite', 'gc', ' where califa_id < 100')
	new = db.dbUtils.getFromDB("mag", dbDir+'CALIFA.sqlite', 'mags')
	plt.scatter(old, new)
	plt.savefig('mags_comparison')
	#sc_index = np.where(np.round(flux, 0) == round(flux[0]/math.e, 0))
        #sc_index = np.where([(np.divide(centralFlux, flux) > math.e) & (isoA > maxFluxIsoA)])[1][0] #the first index after the maximum	   
 	#lsc = isoA[sc_index]*0.396 #in arcseconds

	#phys_lsc = cosm.angular2physical(lsc, z)
	#print str(i)+","+ str(lsc)+","+ str(phys_lsc[0])+","+ str(z[0])#+","+str(maxFluxIsoA)+","+ str(lsc)# -- testing
#np.savetxt("mags.csv", mags, fmt="%i,%f")