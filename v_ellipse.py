# -*- coding: utf-8 -*-

import numpy as np
from scipy import pi
import math
import pyfits
import collections #Counter class is necessary, check if your module version is up to date
import itertools
import utils



def ellipse(inputShape, ra,rb,ang,x0,y0,nPoints=5000):
	'''ra - major axis length
	  rb - minor axis length
	  ang - angle
	  x0,y0 - position of centre of ellipse
	  Nb - No. of points that make an ellipse
	  
	  based on matlab code ellipse.m  written by D.G. Long, 
	  Brigham Young University, based on the
	  CIRCLES.m original 
	  written by Peter Blattner, Institute of Microtechnology, 
	  University of 
	  Neuchatel, Switzerland, blattner@imt.unine.ch
	'''
	print nPoints, 'npoints'
	xpos,ypos=x0,y0
#	print 'xpos', xpos, 'ypos', ypos
	radm,radn=ra,rb
	an=np.radians(ang)

	co,si=np.cos(an),np.sin(an)
	print nPoints, 'np', type(nPoints)
	#todo: make it a 2D array
	the = np.empty((radm.shape[0], nPoints.shape[0]))
	#out = np.empty((np.sum(nPoints), 1), dtype = 'object')
	out = []
	print radm.shape[0], 'number of rings'
	for i in range(0, radm.shape[0]): #looping through isoA
	  the=np.linspace(0,2*pi,nPoints[i])	#setting angle values
	  Y = np.round(radm[i]*np.cos(the)*si+co*radn[i]*np.sin(the)+ypos,0).astype('int16')# here we get two vectors of coordinates
	  X = np.round(radm[i]*np.cos(the)*co-si*radn[i]*np.sin(the)+xpos,0).astype('int16')
	  print X.shape, 'x'
	  for a, b in zip(Y, X):
	    out.append((a, b))
	  
	  #print (Y, X), 'xy'
	print 'out', len(out), out[0]
	return out
'''
#input 2D array, input image shape (tuple)
def removeLimits(array, inputShape):
  gc = np.where((array[:, 0] >= 0) & (array[:, 0] < inputShape[0]) & (array[:, 1] >= 0) & (array[:, 1] < inputShape[1]))
  print gc
  return array[gc]
'''



def getPixelEllipseLength(isoA, axisRatio):
  length = len(draw_ellipse((2000, 2000), 1000, 1000, 0, isoA, axisRatio)[0])
  #print 'length', length, 'circumference', get_ellipse_circumference(isoA, axisRatio)
  return length


def get_ellipse_circumference(isoA, axisRatio):
  #Ramanujan's second approximation
  a = isoA
  b = axisRatio*isoA

  h = (a - b)**2/(a + b)**2
  #h = math.pow((a - b), 2)/math.pow((a + b), 2)
  circumference = math.pi * (a + b) * (1.0 + 3*h/(10.0 + np.sqrt(4.0 - 3*h)))
  print circumference, 'circ'
  return np.round(circumference, 0)

def draw_ellipse(inputShape, y0, x0, pa, isoA, axisRatio):
        
	print isoA, axisRatio, 'a, axisRatio'
	nPoints = get_ellipse_circumference(isoA, axisRatio)
	print nPoints, isoA, axisRatio
	#passing an index array for edge clipping as the first argument
	
	#print nPoints*2, 'npoints /////////////////////////////////////////////////////////'
	#print len(rejectDuplicates(ellipse(inputShape, isoA,isoA*axisRatio,pa,x0,y0,nPoints*2))[0])
	ret = rejectDuplicates(ellipse(inputShape, isoA,isoA*axisRatio,pa,x0,y0, np.round(2*pi*nPoints, 0)))
	ret = rejectOutsiders(ret[0], ret[1], inputShape)
	return ret 

def rejectOutsiders(Y, X, inputShape):
  goodRows = []
  print '))))))))))))))))'

  for j, y in enumerate(Y):
	 if ((Y[j] >= 0) & (Y[j] < inputShape[0]) & (X[j] >= 0) & (X[j] < inputShape[1])):
		print 'yahoo'
		goodRows.append(j)
  print goodRows, 'gr'
  Y = Y[goodRows]
  X = X[goodRows]
  return (Y, X)

def rejectDuplicates(ellipseCoords):
  #taking care of the duplicate indices: 
  #for 2D arrays: index array, list of indices
  #returns good indices 
  print len(ellipseCoords), 'len', ellipseCoords[0]
  u= np.unique(ellipseCoords, return_index=False)
  print len(u), 'after rej'
  #print ellipseCoords.shape[0] - ellipseCoords[indices].shape[0], 'Duplicate points rejected'
  #ellipseCoords = ellipseCoords[indices]
  #ellipseCoords = list(itertools.chain(*ellipseCoords))
  #Y = [i[0] for i in ellipseCoords]
  #X = [i[1] for i in ellipseCoords]
  #print '))))))))))))))))'
  #print type(ellipseCoords), 'elc', '\n'
  #return ellipseCoords
  
  
  Y = [i[0] for i in u]
  X = [i[1] for i in u]

  #print ellipseCoords[:, 0], '\n\n\n', ellipseCoords[:, 0]
  return (Y, X)

  
def main():
  '''
  #it's all for testing
  inputImage = np.zeros((50, 49))
  isoA =  np.array(([25], [26], [27], [28], [29]))
  
  print isoA, isoA.shape
  ellipseCoords = draw_ellipse(inputImage.shape, 25, 27, 0, isoA, 0.9)
  
  
  
  #getPixelEllipseLength(150, 0.9)
  
  
  #print X, 'a'
  inputImage[ellipseCoords] = 1000
  hdu = pyfits.PrimaryHDU(inputImage)
  hdu.writeto('ellipse.fits')
  '''
if __name__ == "__main__":
  main()  
