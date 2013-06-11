# -*- coding: utf-8 -*-

import numpy as np
from scipy import pi,sin,cos
import math
import pyfits
import collections #Counter class is necessary, check if your module version is up to date
import itertools
import utils


def ellEquation(the, a, b, si, co, ypos, xpos):
	Y = np.round(a*np.cos(the)*si+co*b*np.sin(the)+ypos,0).astype('int16')
	X = np.round(a*np.cos(the)*co-si*b*np.sin(the)+xpos,0).astype('int16')
	return Y, X

def cleanEllipse(out, inputShape, Y, X):
        #print out.shape, out.dtype
        out[:, 0] = Y
        out[:, 1] = X
	goodRows = np.where(((out[:, 0] >= 0) & (out[:, 0] < inputShape[0]) & (out[:, 1] >= 0) & (out[:, 1] < inputShape[1])))
	outList = []
	out = out[goodRows]
	#outList = np.empty((goodRows[0].shape[0], 1), dtype='object')
	for row in out:
	  #print row, tuple(row)
	  outList.append(tuple(row))
	  #out = (Y[goodRows], X[goodRows])
	outList = list(set(outList))
	#for i, x in enumerate(np.asarray(outList, dtype='object'):
	  
	
	#print outList, 'out'
	
	return outList


def ellipse(inputShape, a, b,angle,x0,y0,nPoints=50):
	'''a - major axis length
	  b - minor axis length	  
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
	radm,radn=a,b
	an=np.radians(angle)
	co,si=cos(an),sin(an)
	the=np.linspace(0,2*pi,nPoints)
	Y, X = ellEquation(the, a, b, si, co, ypos, xpos)
	out = np.empty((Y.shape[0], 2))
	#out = out[:Y.shape[0],:]
	outList = cleanEllipse(out, inputShape, Y, X)

	return outList
'''
#input 2D array, input image shape (tuple)
def removeLimits(array, inputShape):
  gc = np.where((array[:, 0] >= 0) & (array[:, 0] < inputShape[0]) & (array[:, 1] >= 0) & (array[:, 1] < inputShape[1]))
  print gc
  return array[gc]
'''



def getPixelEllipseLength(isoA, axisRatio):
  length = len(draw_ellipse((8000, 8000), 4000, 4000, 0, isoA, axisRatio)[0])
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
	ret = rejectDuplicates(ellipse(inputShape, isoA,isoA*axisRatio,pa,x0,y0,6*pi*nPoints))

	return ret

def rejectDuplicates(ellipseCoords):
  #taking care of the duplicate indices: 
  #for 2D arrays: index array, list of indices
  #returns good indices 
   
  #u, indices = np.unique(ellipseCoords, return_index=True)
  
  #print ellipseCoords.shape[0] - ellipseCoords[indices].shape[0], 'Duplicate points rejected'
  
  
  #ellipseCoords = ellipseCoords[indices]
  X = []
  Y = []
  for i in ellipseCoords:
    Y.append(i[0])
    X.append(i[1])
  
  
  return (Y, X)

  
#def main():
  
#if __name__ == "__main__":
#  main()  
