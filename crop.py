import numpy as np
import pyfits
from astLib import astWCS
import matplotlib.pyplot as plt

def crop(inputImage, coords, side):
	#note that y-direction is backwards, due to compatibility with ds9!
	if side == 'TL':
		inputImage = inputImage[coords[0]:, coords[1]:]
	elif side == 'BL':
		inputImage = inputImage[coords[0]:, coords[1]:]
	elif side == 'TR':
		inputImage = inputImage[coords[0]:, :coords[1]]
	elif side == 'BR':
		inputImage = inputImage[coords[0]:, :coords[1]]
	else:
		 print 'problems with crop coordinates, check where is the center'
	return inputImage

def ds9toNumPyCoords(coords, shape):
	x, y = coords
	y = shape[0] - y
	print y, x
	return (y, x)

def getCroppedCenter(shape, ylim, xlim, center):
	return 0

def setSide(center, cropCoords):

	if (center[0] >= cropCoords[0]):
		out = 'T'
	else:
		out = 'B'
	if (center[1] >= cropCoords[1]):
		return out+'L'
	else:
		return out+'R'


inputImage = pyfits.open('../data/filled/fpC-001729-r2-0262.fits')[0].data
center = (501, 881)
print inputImage.shape
print center
cropCoords = (900, 800)
center = ds9toNumPyCoords(center, inputImage.shape)
cropCoords = ds9toNumPyCoords(cropCoords, inputImage.shape)

print 'center:', center, 'crop', cropCoords
side = setSide(center, cropCoords)
print side
inputImage = crop(inputImage, cropCoords, side)


hdu = pyfits.PrimaryHDU(inputImage)
hdu.writeto('out.fits')



