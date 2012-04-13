# -*- coding: utf-8 -*-
#@author: astrolitterbox

import numpy as np
import pyfits
from astLib import astWCS
import matplotlib.pyplot as plt
import plot_survey

def plotScatter(data, xlabel, ylabel, filename):
  fig = plt.figure()
  ax = fig.add_subplot(111)
  #print data.shape
  for i in range(1, data.shape[0]):
    ax.plot(data[0,:], data[i,:], ',', markersize=1, color='red', mec='red', alpha = 0.9)
#  p2 = ax.plot(data[2], data[3], ',', markersize=1, color=blue, mec=blue, alpha = 0.9)
  #p3 = ax.plot(x3, y3, ',', markersize=1, color=color3, mec=color3, alpha = 0.9)
  #p4 = ax.plot(x4, y4, ',', markersize=1, color=color4, mec=color4, alpha = 0.9)
  #prop = matplotlib.font_manager.FontProperties(size=8) 
  #plt.legend([p1[0]], legend,  loc=0, markerscale=10, fancybox=True, labelspacing = 0.2, prop=prop, shadow=True)
  #plt.title(title)
  #plt.ylabel = ylabel
  #plt.xlabel = xlabel
  plt.savefig(filename)
  #plt.show()

imgFile = pyfits.open('IC3376R.fits_filled.fits')
img = imgFile[0].data
head = imgFile[0].header
#wcs = pywcs.WCS(head)
#print wcs.wcs.crval[0]  

#print np.asarray([186, 29])

#wcs.wcs.print_contents()
#pixcrd = np.array([[head['ra'], head['dec']]], np.float_)

#x = np.array([head['ra']])
#y = np.array([head['dec']])
#print head['ra'], head['dec']


#WCS=astWCS.WCS(head, mode = "pyfits")
WCS=astWCS.WCS("IC3376R_masked.fits")
#print head['ra'], head['dec']
#center = WCS.wcs2pix(186.95977, 26.99345)
center = WCS.wcs2pix(186.9597481,26.99352614)
print center
print 'brightness at the galaxy center', img[center[1], center[0]] #thanks, numpy





  
#distances = Astrometry.makeDistanceArray(img, center)



fluxData = np.empty((np.max(distances), 4))
print fluxData.shape
cumulativeFlux = 0.
meanFlux = img[center[1], center[0]]
distance = 0
oldFlux = 2

#maxDist = np.max(distances)
#print 'maxDist', maxDist

iso25D = 80 / 0.396 #maximum CALIFA galaxies Iso25 radius by selection
#print iso25D

print 'fluxdata', fluxData.shape
#fluxData = np.genfromtxt('fluxData.txt')
#fluxData = fluxData[0:distance,:]

skyMean = np.mean(img[np.where(distances > int(round(iso25D)))])
print np.where(distances > int(round(iso25D)))[0].shape, 'np.where(distances > int(round(iso25D)))[0].shape'
skyrms = np.sqrt((np.sum(img[np.where(distances > int(round(iso25D)))]**2)/np.where(distances > int(round(iso25D)))[0].shape/np.where(distances > int(round(iso25D)))[0].shape))
print skyMean, 'skyMean'



#while (abs(oldFlux - meanFlux) > 0.002):
while round(skyMean, 1) <= round(meanFlux, 1):
  
  print '\n sky', round(skyMean, 2), 'flux', round(meanFlux, 2)
  print 'distance', distance
  currentPixels = np.where(distances == distance)
  Npix = len(img[currentPixels])
  print 'Npix', Npix
  #oldFlux = meanFlux
  currentFlux = np.sum(img[currentPixels])
  cumulativeFlux = cumulativeFlux+currentFlux
  print 'cumulative Flux', cumulativeFlux
  
  meanFlux = np.sum(img[currentPixels])/Npix
  print 'meanFlux', meanFlux
#  print 'oldFlux - meanFlux', oldFlux - meanFlux
  rms = np.sqrt((np.sum(img[currentPixels]**2))/Npix)/Npix
  print rms, 'rms'
  stDev = np.sqrt(np.sum((img[currentPixels] - meanFlux)**2)/Npix)/Npix
  print stDev, 'stDev'
  fluxData[distance, 0] = distance
  fluxData[distance, 1] = cumulativeFlux
  fluxData[distance, 2] = rms
  fluxData[distance, 3] = currentFlux
  distance = distance +1




totalNpix = len(img[np.where(distances < distance)])

totalFlux = np.sum(img[np.where(distances < distance)]) - totalNpix * skyMean - img[center[1], center[0]]

print totalFlux, 'totalFlux'
print totalNpix, 'total Npix'

#img = img - skyMean
#hdu = pyfits.PrimaryHDU(skySub)
#hdu.writeto('sub.fits')

skysub = np.mean(img[np.where(distances < distance)])

print np.mean(skysub), 'np.mean(skysub)'

#img[np.where(distances == distance)] = 10000
#print np.where(distances == int(round(iso25D)))
#img[np.where(distances == int(round(iso25D)))] = -100
#np.savetxt('fluxData', fluxData)

#from http://www.sdss.org/dr7/algorithms/fluxcal.html#counts2mag:

#-2.5*numpy.log10(10**(-5))
#(6.6895*10**6)/((10**8) * 1.9327*10**3)

print head['EXPTIME'], 'head[EXPTIME]'
print 'head[FLUX20]', head['FLUX20']
fluxRatio2 = totalFlux/(10**8 * head['FLUX20'])
fluxRatio = totalFlux/(53.9075*10**(-0.4*(-23.98+0.07*1.19)))



mag = -2.5 * np.log10(fluxRatio)
mag2 = -2.5 * np.log10(fluxRatio2)
print 'full magnitude', mag, 'flux 20 mag', mag2



#print fluxData[1]
#print fluxData.shape
#print np.mean(img[np.where(distances > int(round(iso25D)))])
plotScatter(np.array((fluxData[:,0], fluxData[:,1])), 'distance', 'cumulativeFlux', 'cumulativeFlux')
plotScatter(np.array((fluxData[:,0], fluxData[:,3])), 'distance', 'Flux', 'Flux')

#plotScatter(np.array((fluxData[:,0], fluxData[:, 2], fluxData[:, 3])), 'distance', 'cumulativeFlux', 'stats')
hdu = pyfits.PrimaryHDU(img)
hdu.writeto('test0.fits')






'''
x = xy[:, 0:1]
y = xy[:, 1:]
r = np.sqrt(x*x + y*y)
theta = npy.arccos(x / r)
theta = npy.where(y > 0, 2 * npy.pi - theta, theta)
return np.concatenate((theta, r), 1

'''