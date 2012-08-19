#from http://www.janeriksolem.net/2009/06/histogram-equalization-with-python-and.html
import numpy as np

def histeq(array,nbr_bins=4096):

   #get image histogram
   imhist,bins = np.histogram(array.flatten(),nbr_bins,normed=True)
   cdf = imhist.cumsum() #cumulative distribution function
   cdf = 4095 * cdf / cdf[-1] #normalize

   #use linear interpolation of cdf to find new pixel values
   im2 = np.interp(array.flatten(),bins[:-1],cdf)

   return np.reshape(im2, array.shape), cdf

    
