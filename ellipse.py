# -*- coding: utf-8 -*-

import numpy as np
from scipy import pi,sin,cos
import math
import pyfits
import collections #Counter class is necessary, check if your module version is up to date
import itertools
import utils


def ellipse(inputShape, ra,rb,ang,x0,y0,nPoints=50):
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
	xpos,ypos=x0,y0
#	print 'xpos', xpos, 'ypos', ypos
	radm,radn=ra,rb
	an=np.radians(ang)

	co,si=cos(an),sin(an)

	the=np.linspace(0,2*pi,nPoints)
	out = np.empty((len(the), 1), dtype = 'object')
	#enumerate #TODO
	Y = np.round(radm*cos(the)*si+co*radn*sin(the)+ypos,0).astype('int16')
	X = np.round(radm*cos(the)*co-si*radn*sin(the)+xpos,0).astype('int16')
	
	#Y = removeLimits(Y, inputImage.shape[0])
	#X = removeLimits(X, inputImage.shape[1])
	out = out[:Y.shape[0],:]
	
	goodRows = []
	for i, v in enumerate(out):
	
	  if ((Y[i] >= 0) & (Y[i] < inputShape[0]) & (X[i] >= 0) & (X[i] < inputShape[1])):	    
	    out[i, 0] = (Y[i], X[i])	
	    goodRows.append(i)	  
	out = out[goodRows]
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
  h = math.pow((a - b), 2)/math.pow((a + b), 2)
  circumference = math.pi * (a + b) * (1.0 + 3*h/(10.0 + math.sqrt(4.0 - 3*h)))
  #print circumference 
  return np.round(circumference, 0)

def draw_ellipse(inputShape, y0, x0, pa, isoA, axisRatio):
        
	#print isoA, axisRatio, 'a, axisRatio'
	nPoints = get_ellipse_circumference(isoA, axisRatio)
	#passing an index array for edge clipping as the first argument
	
	#print nPoints*2, 'npoints /////////////////////////////////////////////////////////'
	#print len(rejectDuplicates(ellipse(inputShape, isoA,isoA*axisRatio,pa,x0,y0,nPoints*2))[0])
	return rejectDuplicates(ellipse(inputShape, isoA,isoA*axisRatio,pa,x0,y0,nPoints))

def rejectDuplicates(ellipseCoords):
  #taking care of the duplicate indices: 
  #for 2D arrays: index array, list of indices
  #returns good indices 
  
  u, indices = np.unique(ellipseCoords, return_index=True)
  
  #print ellipseCoords.shape[0] - ellipseCoords[indices].shape[0], 'Duplicate points rejected'
  
  
  ellipseCoords = ellipseCoords[indices]
  ellipseCoords = list(itertools.chain(*ellipseCoords))
  Y = [i[0] for i in ellipseCoords]
  X = [i[1] for i in ellipseCoords]
  #print '))))))))))))))))'
  #print ellipseCoords[:, 0], '\n\n\n', ellipseCoords[:, 0]
  return (Y, X)

  
def main():
  
  #it's all for testing
  inputImage = np.zeros((50, 49))
  ellipseCoords = draw_ellipse(inputImage.shape, 25, 27, 0, 27, 0.9)
  
  
  
  getPixelEllipseLength(150, 0.9)

  
  #print X, 'a'
  #inputImage[(Y, X)] = 1000
  #hdu = pyfits.PrimaryHDU(inputImage)
  #hdu.writeto('ellipse.fits')
  
if __name__ == "__main__":
  main()  
