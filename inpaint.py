# -*- coding: utf-8 -*-
"""
Created on Tue Feb 28 11:56:41 2012

@author: gasagna (https://github.com/gasagna/openpiv-python/blob/master/openpiv/src/lib.pyx), some modifications by astrolitterbox
"""

"""A module for various utilities and helper functions"""

import numpy as np
import utils
#cimport numpy as np
#cimport cython
import pyfits
import scipy.spatial

DTYPEf = np.float64
#ctypedef np.float64_t DTYPEf_t

DTYPEi = np.int32
#ctypedef np.int32_t DTYPEi_t

#@cython.boundscheck(False) # turn of bounds-checking for entire function
#@cython.wraparound(False) # turn of bounds-checking for entire function
def replace_nans(array, max_iter, tol,kernel_size=1,method='localmean'):
    """Replace NaN elements in an array using an iterative image inpainting algorithm.
The algorithm is the following:
1) For each element in the input array, replace it by a weighted average
of the neighbouring elements which are not NaN themselves. The weights depends
of the method type. If ``method=localmean`` weight are equal to 1/( (2*kernel_size+1)**2 -1 )
2) Several iterations are needed if there are adjacent NaN elements.
If this is the case, information is "spread" from the edges of the missing
regions iteratively, until the variation is below a certain threshold.
Parameters
----------
array : 2d np.ndarray
an array containing NaN elements that have to be replaced
max_iter : int
the number of iterations
kernel_size : int
the size of the kernel, default is 1
method : str
the method used to replace invalid values. Valid options are
`localmean`.
Returns
-------
filled : 2d np.ndarray
a copy of the input array, where NaN elements have been replaced.
"""
    
#    cdef int i, j, I, J, it, n, k, l
#    cdef int n_invalids
    
    filled = np.empty( [array.shape[0], array.shape[1]], dtype=DTYPEf)
    kernel = np.empty( (2*kernel_size+1, 2*kernel_size+1), dtype=DTYPEf )
    
#    cdef np.ndarray[np.int_t, ndim=1] inans
#    cdef np.ndarray[np.int_t, ndim=1] jnans
    
    # indices where array is NaN
    inans, jnans = np.nonzero( np.isnan(array) )
    
    # number of NaN elements
    n_nans = len(inans)
    
    # arrays which contain replaced values to check for convergence
    replaced_new = np.zeros( n_nans, dtype=DTYPEf)
    replaced_old = np.zeros( n_nans, dtype=DTYPEf)
    
    # depending on kernel type, fill kernel array
    if method == 'localmean':
      
        print 'kernel_size', kernel_size       
        for i in range(2*kernel_size+1):
            for j in range(2*kernel_size+1):
                kernel[i,j] = 1
        print kernel, 'kernel'

    elif method == 'idw':
        kernel = utils.gauss_kern(2)
        print kernel, 'IDW kernel'		    
    else:
        raise ValueError( 'method not valid. Should be one of `localmean` or idw.')
    
    # fill new array with input elements
    #for i in range(array.shape[0]):
    #    for j in range(array.shape[1]):
    #        filled[i,j] = array[i,j]
    filled = array	 #why loop through the array?
    # make several passes
    # until we reach convergence
    for it in range(max_iter):
        print 'iteration', it
        # for each NaN element
        for k in range(n_nans):
            i = inans[k]
            j = jnans[k]
            
            # initialize to zero
            filled[i,j] = 0.0
            n = 0
            
            # loop over the kernel
            for I in range(2*kernel_size+1):
                for J in range(2*kernel_size+1):
                   
                    # if we are not out of the boundaries
                    if i+I-kernel_size < array.shape[0] and i+I-kernel_size >= 0:
                        if j+J-kernel_size < array.shape[1] and j+J-kernel_size >= 0:
                                                
                            # if the neighbour element is not NaN itself.
                            if filled[i+I-kernel_size, j+J-kernel_size] == filled[i+I-kernel_size, j+J-kernel_size] :
                                
                                # do not sum itself
                                if I-kernel_size != 0 and J-kernel_size != 0:
                                    
                                    # convolve kernel with original array
                                    filled[i,j] = filled[i,j] + filled[i+I-kernel_size, j+J-kernel_size]*kernel[I, J]
                                    n = n + 1*kernel[I,J]
                                    #print n

            # divide value by effective number of added elements
            if n != 0:
                filled[i,j] = filled[i,j] / n
                replaced_new[k] = filled[i,j]
            else:
                filled[i,j] = np.nan
                
        # check if mean square difference between values of replaced
        #elements is below a certain tolerance
        print 'tolerance', np.mean( (replaced_new-replaced_old)**2 )
        if np.mean( (replaced_new-replaced_old)**2 ) < tol:
            break
        else:
            for l in range(n_nans):
                replaced_old[l] = replaced_new[l]
    
    return filled


def sincinterp(image, x,  y, kernel_size=3 ):
    """Re-sample an image at intermediate positions between pixels.
This function uses a cardinal interpolation formula which limits
the loss of information in the resampling process. It uses a limited
number of neighbouring pixels.
The new image :math:`im^+` at fractional locations :math:`x` and :math:`y` is computed as:
.. math::
im^+(x,y) = \sum_{i=-\mathtt{kernel\_size}}^{i=\mathtt{kernel\_size}} \sum_{j=-\mathtt{kernel\_size}}^{j=\mathtt{kernel\_size}} \mathtt{image}(i,j) sin[\pi(i-\mathtt{x})] sin[\pi(j-\mathtt{y})] / \pi(i-\mathtt{x}) / \pi(j-\mathtt{y})
Parameters
----------
image : np.ndarray, dtype np.int32
the image array.
x : two dimensions np.ndarray of floats
an array containing fractional pixel row
positions at which to interpolate the image
y : two dimensions np.ndarray of floats
an array containing fractional pixel column
positions at which to interpolate the image
kernel_size : int
interpolation is performed over a ``(2*kernel_size+1)*(2*kernel_size+1)``
submatrix in the neighbourhood of each interpolation point.
Returns
-------
im : np.ndarray, dtype np.float64
the interpolated value of ``image`` at the points specified
by ``x`` and ``y``
"""
    
    # indices
#    cdef int i, j, I, J
   
    # the output array
    r = np.zeros( [x.shape[0], x.shape[1]], dtype=DTYPEf)
          
    # fast pi
    pi = 3.1419
        
    # for each point of the output array
    for I in range(x.shape[0]):
        for J in range(x.shape[1]):
            
            #loop over all neighbouring grid points
            for i in range( int(x[I,J])-kernel_size, int(x[I,J])+kernel_size+1 ):
                for j in range( int(y[I,J])-kernel_size, int(y[I,J])+kernel_size+1 ):
                    # check that we are in the boundaries
                    if i >= 0 and i <= image.shape[0] and j >= 0 and j <= image.shape[1]:
                        if (i-x[I,J]) == 0.0 and (j-y[I,J]) == 0.0:
                            r[I,J] = r[I,J] + image[i,j]
                        elif (i-x[I,J]) == 0.0:
                            r[I,J] = r[I,J] + image[i,j] * np.sin( pi*(j-y[I,J]) )/( pi*(j-y[I,J]) )
                        elif (j-y[I,J]) == 0.0:
                            r[I,J] = r[I,J] + image[i,j] * np.sin( pi*(i-x[I,J]) )/( pi*(i-x[I,J]) )
                        else:
                            r[I,J] = r[I,J] + image[i,j] * np.sin( pi*(i-x[I,J]) )*np.sin( pi*(j-y[I,J]) )/( pi*pi*(i-x[I,J])*(j-y[I,J]))
    return r
    
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
		print pixVal/weightSum
		return pixVal/weightSum
		
	  

		
def fill(inputArray, neighbourArray):
	maxNeighbours = np.max(neighbourArray)
	

	
	ind = zip(*np.where(neighbourArray == maxNeighbours))
	np.random.shuffle(ind)
	print len(np.where(neighbourArray == maxNeighbours)[0]), 'nans left out of', len(np.where(np.isnan(inputArray))[0])
	for i in ind:
	  inputArray[i] = getWeightedAvg(inputArray, i[0], i[1])

	return inputArray	
														
def main():
	#inputArray = np.array([[2, 0.22, 6, 12, 10, 1], [2, 0, 1, 2, 33, 1], [2, 0.2,np.nan, np.nan, 1, 45],  [1, 0.2,4, 0.22, 1, 2],  [2, 0.2,4, 0.22, 1, 4], [1, 0.2,4, 0.22, 1, 2]])
	image = pyfits.open('/work2/simona/data/SDSS/fpC-006371-r6-0151.fit.gz')[0].data - 1000 #soft bias
	#head = pyfits.open('/work2/simona/data/SDSS/fpC-001035-r1-0149.fit.gz')[0].header
	mask = pyfits.open('/work2/simona/data/MASKS/UGC00005_mask_r.fits')[0].data
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
      	hdu.writeto('filled_1.fits')
if __name__ == "__main__":
  main()	
