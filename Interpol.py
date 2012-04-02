# -*- coding: utf-8 -*-
#@author: astrolitterbox
import numpy as np
import pyfits
from scipy import ndimage
from scipy.interpolate import RectBivariateSpline
#from PIL import Image
import scipy as sp
import matplotlib.pyplot as plt
import math

#import cv
#from scipy.spatial import KDTree

imgFile = pyfits.open('fpC-005115-r2-0103.fit')
maskFile = pyfits.open('data/masks/IC3376_mask_r.fits')
imgFile.info()
img = imgFile[0].data
img = img - 1000 #soft bias subtraction, comment out if needed
head = imgFile[0].header
mask = maskFile[0].data



maskedImg = np.ma.array(img, mask = mask)
NANMask =  maskedImg.filled(np.NaN)


badArrays, num_badArrays = sp.ndimage.label(mask)
print num_badArrays
data_slices = sp.ndimage.find_objects(badArrays)
#data_slices = np.ma.extras.notmasked_contiguous(maskedImg)
import inpaint

#def replace_nans(array, max_iter, tol,kernel_size=1,method='localmean'):

#data = np.array([[11,22.0,353],[1,np.NaN,343],[11,0,343]])



filled = inpaint.replace_nans(NANMask, 5, 0.5, 2, 'idw')
hdu = pyfits.PrimaryHDU(filled, header = head)
hdu.writeto('IC3376R_masked.fits')
  
#hdu = pyfits.PrimaryHDU(NANMask)
#hdu.writeto('NanMask.fits')

#invdisttree = idw.Invdisttree(maskedImg, maskedImg)
#print data_slices

#for slice in data_slices:
#  dy, dx = slice
#  coords = float(dy.start), float(dy.stop), float(dx.start), float(dx.stop)
#  print 'slice', coords
#  submask = cutoutMask[(dy.start):(dy.stop),(dx.start):(dx.stop)]
#  subarray = cutout[(dy.start):(dy.stop+1),(dx.start):(dx.stop+1)]
  #print np.where(submask == 1)   
  #print maskCoords, 'maskCoords'
#y = np.where(cutoutMask == 1)[0]
#x = np.where(cutoutMask == 1)[1]
#print y, x, 'xy'
#points = np.zeros((y.shape[0], 2))
#for i in range(0, y.shape[0]-1):
#   points[i] = [y[i], x[i]]
#   print points
#ret = sp.ndimage.interpolation.map_coordinates(maskedImg, points, output=None, order=3, mode='nearest', cval=0.0, prefilter=True)




