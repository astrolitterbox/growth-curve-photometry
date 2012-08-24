import numpy as np
import numpy.ma as ma
import utils
import pyfits

def getWeightedAvg(a, neighbourArray):
	kernSize = 2
	kernel = utils.gauss_kern(kernSize)	  
	pixVal = np.zeros((a.shape)) #initialising, pixel value for inpainting
	weightSum = np.zeros((a.shape)) #initialising, value for later normalisation
	#for pixels further away from the edges:
	maxNeighbours = np.max(neighbourArray)
	print np.max(neighbourArray)
	neighbours = ((-2, -2), (-2, -1), (-2, 0), (-2, 1), (-2, 2), (-1, -2), (-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, -2), (0, -1), (0, 1), (0, 2), (1, -2), (1, -1), (1, 0), (1, 1), (1, 2), (2, -2), (2, -1), (2, 0), (2, 1), (2, 2))
	a_reduced = a[2:-2, 2:-2].copy()
	maxNMask = ma.make_mask_none((a.shape))
	
	maxNMask[np.where(neighbourArray == maxNeighbours)] = 1
	print a_reduced.shape
	for hor_shift,vert_shift in neighbours:
	    #if not np.any(a.mask): break
	    a_shifted = np.roll(a_reduced, shift = hor_shift, axis = 1)
	    a_shifted = np.roll(a_shifted, shift = vert_shift, axis = 0)
	    idx=~a_shifted.mask*maxNMask[2:-2, 2:-2]

	    weightSum = weightSum + kernel[2-vert_shift, 2-hor_shift]
	    pixVal[idx] = pixVal[idx]+ a_shifted[idx]*kernel[2-vert_shift, 2-hor_shift]
	b = a.copy()
	b[idx] = np.divide(pixVal[idx], weightSum[idx])    
	edgesTop = a[0:2, :]
	edgesLeft = a[:, 0:2]
	edgesRight = a[:, -1:-3:-1]
	edgesBottom = a[-1:-3:-1, :]
	for i in range(0, 3):
		for j in range(0, a.shape[1]):
			if neighbourArray[i, j] == maxNeighbours:
				b[i, j] = getWeightedAvgEdges(inputArray, i, j)
	for i in range(a.shape[0] - 2, a.shape[0]):
		for j in range(0, a.shape[1]):
			if neighbourArray[i, j] == maxNeighbours:
				b[i, j] = getWeightedAvgEdges(inputArray, i, j)	
	for i in range(0, a.shape[0]):
		for j in range(0, 3):
			if neighbourArray[i, j] == maxNeighbours:
				b[i, j] = getWeightedAvgEdges(inputArray, i, j)
	for i in range(0, a.shape[0]):
		for j in range(a.shape[1] - 2, a.shape[1]):
			if neighbourArray[i, j] == maxNeighbours:
				b[i, j] = getWeightedAvgEdges(inputArray, i, j)														
	return b


def makeNeighbourArray(a):
	neighbourArray = -1* np.ones((a.shape))
	neighbourArray[a.mask] = 0
	for shift in (-1, 1):
		for axis in (0, 1):
			a_shifted = np.roll(a, shift=shift, axis = axis)
		        idx=~a_shifted.mask * a.mask
			neighbourArray[idx] = neighbourArray[idx]+1
	neighbourArray[0, :] = neighbourArray[0, :] - 1
	neighbourArray[-1, :] = neighbourArray[-1, :] - 1
	neighbourArray[:, 0] = neighbourArray[:, 0] - 1
	neighbourArray[:, -1] = neighbourArray[:, -1] - 1			
	return neighbourArray	


a = np.arange(100).reshape(10,10)
fill_value=-99
a[2:4,3:8] = fill_value
a[9,8] = fill_value
a[9,9] = fill_value

a = ma.masked_array(a,a==fill_value)


image = pyfits.open('/media/46F4A27FF4A2713B_/work2/data/SDSS/fpC-006371-r6-0151.fit.gz')[0].data - 1000 #soft bias
mask = pyfits.open('/media/46F4A27FF4A2713B_/work2/data/MASKS/UGC00005_mask_r.fits')[0].data
inputArray = np.ma.array(image, mask = mask)
neighbourArray = makeNeighbourArray(inputArray)
inputArray.mask[0, 1] = 1
neighbourArray[0, 1] = 5
print neighbourArray
print np.max(neighbourArray), 'max'
c = getWeightedAvg(inputArray, neighbourArray)
print c
