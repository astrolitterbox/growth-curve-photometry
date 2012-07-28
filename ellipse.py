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
	an=ang

	co,si=cos(an),sin(an)

	the=np.linspace(0,2*pi,nPoints)
	X=radm*cos(the)*co-si*radn*sin(the)+xpos
	Y=radm*cos(the)*si+co*radn*sin(the)+ypos
	return [np.round(Y,0).astype('int16'), np.round(X, 0).astype('int16')]


def get_ellipse_circumference(isoA, axisRatio):
  #Ramanujan's second approximation
  a = isoA
  b = axisRatio*isoA
  h = math.pow((a - b), 2)/math.pow((a + b), 2)
  circumference = math.pi * (a + b) * (1.0 + 3*h/(10.0 + math.sqrt(4.0 - 3*h)))
  #print circumference 
  return np.round(circumference, 0)

def draw_ellipse(y0, x0, pa, isoA, axisRatio):
	#print isoA, axisRatio, 'a, axisRatio'
	nPoints = get_ellipse_circumference(isoA, axisRatio)
	#return ellipse(10,5,7510,10,300)
	#pa - 90: ellipse code uses x axis as 0 deg, while SDSS and Nadine's data gives the North direction as the 0 deg reference  
	return ellipse(isoA,isoA*axisRatio,pa+90,x0,y0,nPoints)


#border case, solve later if necessary

def getMaxIndices(inputImage):
    maxY = inputImage.shape[0]
    print len(inputImage[0,:]), len(inputImage[:, 0])
    maxX = inputImage.shape[1]
    return maxY-1, maxX-1 #indexing starts from 0, so the array indices go to max-1

def getGoodCoords(inputImage, ellipseCoords):
  #taking care of the boundaries: 
  #clipping all points on the ellipse whose coordinates > the indices of the input image.
  
  #goodCoords = np.where((ellipseCoords[0] in np.arange(0, getMaxIndices(inputImage)[0])))
  maxY = getMaxIndices(inputImage)[0]
  maxX = getMaxIndices(inputImage)[1]
  print maxY, maxX, 'maxes' 
  length = ellipseCoords[0]
  print 'len', length
  Ycond = [((0 <= ellipseCoords[0]) & (ellipseCoords[0] <= maxY)) & ((0 <= ellipseCoords[1]) & (ellipseCoords[1]<= maxX))]
  print ellipseCoords
  print np.where(cond == True), 'where'
  goodCoords = ellipseCoords[np.where(cond == True)]
  print goodCoords
  
  #goodCoords[0] = ellipseCoords[np.where(where)][0]
  
 
  
  
  
       
  #  if [(ellipseCoords[0][i] in range(0, maxY)) & (ellipseCoords[1][i] in range(0, maxX))]:
 #     goodCoords[0].append(ellipseCoords[0][i])
  #    goodCoords[1].append(ellipseCoords[1][i])
      
  
  #print len(goodCoords[0]), 'goodcoords', len(ellipseCoords[0]), 'ell coords'
  return goodYCoords
  
def main():
  inputImage = np.zeros((51, 51))
  
    
  ellipseCoords = draw_ellipse(25, 25, 0, 26, 1)
  
  print len(ellipseCoords), ellipseCoords[0].shape[0]
  
  
  #goodCoords = np.where((ellipseCoords < 
  goodCoords = getGoodCoords(inputImage, ellipseCoords)
  
  inputImage[goodCoords[0], goodCoords[1]] = 1000
  hdu = pyfits.PrimaryHDU(inputImage)
  hdu.writeto('ellipse.fits')
  
if __name__ == "__main__":
  main()  
