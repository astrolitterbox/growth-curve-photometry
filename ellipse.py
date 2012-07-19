from numpy import linspace
from scipy import pi,sin,cos


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
	print 'xpos', xpos, 'ypos', ypos
	radm,radn=ra,rb
	an=ang

	co,si=cos(an),sin(an)

	the=linspace(0,2*pi,nPoints)
	X=radm*cos(the)*co-si*radn*sin(the)+xpos
	Y=radm*cos(the)*si+co*radn*sin(the)+ypos
	return Y,X

def draw_ellipse(y0, x0, pa, isoA, axisRatio, nPoints):
	print isoA, axisRatio, 'a, axisRatio'
	#return ellipse(10,5,7510,10,300)
	return ellipse(isoA,isoA*axisRatio,pa,x0,y0,nPoints)


