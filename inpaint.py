# -*- coding: utf-8 -*-
import numpy as np
import utils
import pyfits

    
def neighbours(y, x, inputArray):
	shape = inputArray.shape
	out = []		
	if ((y - 1) >= 0):
		if np.isfinite(inputArray[y-1, x]): 
			out.append((y - 1, x))
	if ((x - 1) >= 0):
		if np.isfinite(inputArray[y, x -1]): 
			out.append((y, x - 1))
	if ((y + 1) < shape[0]):
		if np.isfinite(inputArray[y+1, x]): 
			out.append((y+1, x))
	if ((x + 1) < shape[1]): 
		if np.isfinite(inputArray[y, x +1]): 
			out.append((y, x + 1))
	#print len(out)		
	return len(out)
    
    
    
#get the number of non-NaN neighbours
def makeNeighbourArray(inputArray):
	neighbourArray = -1*np.ones((inputArray.shape))
	#print inputArray.shape
	ind = zip(*np.where(np.isnan(inputArray)))
	#neighb = np.concatenate([neighbors(*i) for i in ind])
	for i in ind:
	  #print i
	  neighbourArray[i] = neighbours(i[0], i[1], inputArray)
	#neighbourArray[i] = neighbours(inputArray, *i) for i in ind
	return neighbourArray

def getWeightedAvg(inputArray, y, x):
		kernSize = 2
		kernel = utils.gauss_kern(kernSize)	  
		pixVal = 0 #initialising, pixel value for inpainting
		weightSum = 0 #initialising, value for later normalisation
		#4 adjacent pixels at dist 2 with weight = kernel[2, 0]
		try:	
			if np.isfinite(inputArray[y-2, x]):
				pixVal+= inputArray[y-2, x] * kernel[2, 0]
				weightSum+= kernel[2, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+2, x]):
				pixVal+= inputArray[y+2, x] * kernel[2, 0]
				weightSum+= kernel[2, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y, x+2]):
				pixVal+= inputArray[y, x+2] * kernel[2, 0]
				weightSum+= kernel[2, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y, x-2]):
				pixVal+= inputArray[y, x-2] * kernel[2, 0]
				weightSum+= kernel[2, 0]
		except IndexError:
			pass

		#4 adjacent pixels at dist 1 with weight = kernel[2, 1]
		try:	
			if np.isfinite(inputArray[y-1, x]):
				pixVal+= inputArray[y-1, x] * kernel[2, 1]
				weightSum+= kernel[2, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+1, x]):
				pixVal+= inputArray[y+1, x] * kernel[2, 1]
				weightSum+= kernel[2, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y, x+1]):
				pixVal+= inputArray[y, x+1] * kernel[2, 1]
				weightSum+= kernel[2, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y, x-1]):
				pixVal+= inputArray[y, x-1] * kernel[2, 1]
				weightSum+= kernel[2, 1]
		except IndexError:
			pass

		#4 diagonal pixels with weight = kernel[1, 1]

		try:	
			if np.isfinite(inputArray[y-1, x-1]):
				pixVal+= inputArray[y-1, x-1] * kernel[1, 1]
				weightSum+= kernel[1, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+1, x-1]):
				pixVal+= inputArray[y+1, x-1] * kernel[1, 1]
				weightSum+= kernel[1, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+1, x+1]):
				pixVal+= inputArray[y+1, x+1] * kernel[1, 1]
				weightSum+= kernel[1, 1]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y-1, x+1]):
				pixVal+= inputArray[y-1, x+1] * kernel[1, 1]
				weightSum+= kernel[1, 1]
		except IndexError:
			pass

		#4 diagonal pixels with weight = kernel[0, 0]	
		try:	
			if np.isfinite(inputArray[y-2, x-2]):
				pixVal+= inputArray[y-2, x-2] * kernel[0, 0]
				weightSum+= kernel[0, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+2, x-2]):
				pixVal+= inputArray[y+2, x-2] * kernel[0, 0]
				weightSum+= kernel[0, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+2, x+2]):
				pixVal+= inputArray[y+2, x+2] * kernel[0, 0]
				weightSum+= kernel[0, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y-2, x+2]):
				pixVal+= inputArray[y-2, x+2] * kernel[0, 0]
				weightSum+= kernel[0, 0]
		except IndexError:
			pass

		
		#8 adjacent pixels with weight = kernel[1, 0]		
		try:	
			if np.isfinite(inputArray[y-2, x-1]):
				pixVal+= inputArray[y-2, x-1] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+2, x-1]):
				pixVal+= inputArray[y+2, x-1] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+2, x+1]):
				pixVal+= inputArray[y+2, x+1] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y-2, x+1]):
				pixVal+= inputArray[y-2, x+1] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		# -- just swapping 2 and 1 in y, x:
		try:	
			if np.isfinite(inputArray[y-1, x-2]):
				pixVal+= inputArray[y-1, x-2] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+1, x-2]):
				pixVal+= inputArray[y+1, x-2] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y+1, x+2]):
				pixVal+= inputArray[y+1, x+2] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass
		try:	
			if np.isfinite(inputArray[y-1, x+2]):
				pixVal+= inputArray[y-1, x+2] * kernel[1, 0]
				weightSum+= kernel[1, 0]
		except IndexError:
			pass

		return pixVal/weightSum
		
	  

		
def fill(inputArray, neighbourArray):
	maxNeighbours = np.max(neighbourArray)
	

	
	ind = zip(*np.where(neighbourArray == maxNeighbours))

	print 'working on',  len(np.where(neighbourArray == maxNeighbours)[0]), 'nan pixels out of', len(np.where(np.isnan(inputArray))[0]),' left'
	for i in ind:
	  inputArray[i] = getWeightedAvg(inputArray, i[0], i[1])

	return inputArray	
														
def main():
	#inputArray = np.array([[2, 0.22, 6, 12, 10, 1], [2, 0, 1, 2, 33, 1], [2, 0.2,np.nan, np.nan, 1, 45],  [1, 0.2,4, 0.22, 1, 2],  [2, 0.2,4, 0.22, 1, 4], [1, 0.2,4, 0.22, 1, 2]])
	image = pyfits.open('../data/SDSS/fpC-004517-r5-0107.fit.gz')[0].data - 1000 #soft bias
	#head = pyfits.open('/work2/simona/data/SDSS/fpC-001035-r1-0149.fit.gz')[0].header
	mask = pyfits.open('../data/MASKS/UGC04416_mask_r.fits')[0].data
        inputArray = np.ma.array(image, mask = mask)
	inputArray = inputArray.filled(np.NaN)

	neighbourArray = -1*np.ones((inputArray.shape), dtype = int)
	neighbourArray = makeNeighbourArray(inputArray)
	
	print np.max(neighbourArray), 'maxneighbours'
	while (len(np.where(np.isnan(inputArray))[0]) > 0):
		inputArray = fill(inputArray, neighbourArray)
		neighbourArray = makeNeighbourArray(inputArray)
		print np.max(neighbourArray), 'max'
		#print inputArray	
     	hdu = pyfits.PrimaryHDU(inputArray)
      	hdu.writeto('filled_201.fits')
if __name__ == "__main__":
  main()	
