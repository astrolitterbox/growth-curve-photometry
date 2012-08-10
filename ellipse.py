# -*- coding: utf-8 -*-

import numpy as np
from scipy import pi,sin,cos
import math
import pyfits

def ellipse(ra,rb,ang,x0,y0,nPoints=50):
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
	X=radm*cos(the)*co-si*radn*sin(the)+xpos	
	Y=radm*cos(the)*si+co*radn*sin(the)+ypos
	print X.shape, X.dtype
	
	return [np.round(Y,0).astype('int16'), np.round(X, 0).astype('int16')]


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
	#return ellipse(10,5,7510,10,300)
	
	return cropCoords(inputShape, ellipse(isoA,isoA*axisRatio,pa,x0,y0,nPoints))



def cropCoords(inputShape, ellipseCoords):
  #taking care of the boundaries: 
   #for 2D arrays: shape of the array, list of indices
  #checks if the indices are between 0 and ylim and xlim, rejects the bad coordinates
  #returns good indices 
  
  maxY = inputShape[0]
  maxX = inputShape[1]
  print maxY, maxX, 'maxes' 
  length = len(ellipseCoords[0])
  print 'len', length 
  coords = zip(ellipseCoords[0], ellipseCoords[1])
  print coords
  print '____________'
  
  
  exit()
  
  cond = np.where([((0 <= ellipseCoords[0]) & (ellipseCoords[0] <= maxY)) & ((0 <= ellipseCoords[1]) & (ellipseCoords[1]<= maxX))])
  
  goodCoords = ellipseCoords[cond]
  
  return goodCoords
  #goodCoords[0] = ellipseCoords[np.where(where)][0]
  
  
       
  #  if [(ellipseCoords[0][i] in range(0, maxY)) & (ellipseCoords[1][i] in range(0, maxX))]:
 #     goodCoords[0].append(ellipseCoords[0][i])
  #    goodCoords[1].append(ellipseCoords[1][i])
      
  
  #print len(goodCoords[0]), 'goodcoords', len(ellipseCoords[0]), 'ell coords'
  return goodYCoords
  
def main():
  inputImage = np.zeros((51, 51))
  
    
  ellipseCoords = draw_ellipse(inputImage.shape, 26, 25, 0, 26, 1)
  
  print len(ellipseCoords), ellipseCoords[0].shape[0]
  inputImage[goodCoords[0], goodCoords[1]] = 1000
  hdu = pyfits.PrimaryHDU(inputImage)
  hdu.writeto('ellipse.fits')
  
if __name__ == "__main__":
  main()  
