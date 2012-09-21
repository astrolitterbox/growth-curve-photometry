# -*- coding: utf-8 -*-
import os
import pyfits
import csv
import numpy
import string
import gzip
from astLib import astWCS
from math import ceil


#awk < mothersample.csv 'BEGIN { FS="," }; { print $1,",",$2,",",$3,",",$9,",",$10,",",$11,",",$12}' > list.txt

dataFile = 'list.txt'
band = 'g'

#the next three functions are from sdsspy library (http://code.google.com/p/sdsspy/)

def run2string(runs):
    """
    rs = run2string(runs)
    Return the string version of the run.  756->'000756'
    Range checking is applied.
    """
    return tostring(runs,0,999999)

def field2string(fields):
    """
    fs = field2string(field)
    Return the string version of the field.  25->'0025'
    Range checking is applied.
    """
    return tostring(fields,0,9999)


def tostring(val, nmin=None, nmax=None):
    if not numpy.isscalar(val):
        return [tostring(v,nmin,nmax) for v in val]
    if isinstance(val, (str,unicode)):
	nlen = len(str(nmax))
	vstr = str(val).zfill(nlen)
	return vstr
    if nmax is not None:
        if val > nmax:
            raise ValueError("Number ranges higher than 
            max value of %s\n" % nmax)
    if nmax is not None:
        nlen = len(str(nmax))
        vstr = str(val).zfill(nlen)
    else:
        vstr = str(val)
    return vstr        




def getShiftedImage(img, shift):     
  '''
  if (shift[0] == 0):
    print 'zero y shift'
    shift[0] = -1*(img.shape[0])
    print shift, 'shift'
  if (shift[1] == 0):
    print 'zero x shift'
    shift[1] = -1*(img.shape[1])
    print shift, 'shift' 
   
  if (shift[0] > 0):  
    if (shift[1] > 0): #(+, +) case
      print 'plus plus'
      ret = img[0:-shift[0], 0:-shift[1]]
    else: #(+, -)
      print 'plus minus'
      ret = img[0:-shift[0], -(shift[1]):]
  if (shift[0] <= 0):
    if (shift[1] > 0): #(-, +) case
      print 'minus plus'
      ret = img[-(shift[0]):, 0:-shift[1]]
    else: #(-, -) case
      print 'negative', img.shape, shift[0]
      ret = img[-(shift[0]):, -(shift[1]):]
      '''
      
  if (shift[0] > 0):  
    if (shift[1] > 0): #(+, +) case
      print 'plus plus'
      ret = img[0:-shift[0], 0:-shift[1]]
    else: #(+, -)
      print 'plus minus'
      ret = img[0:-shift[0], -(shift[1]):]
  if (shift[0] <= 0):
    if (shift[1] > 0): #(-, +) case
      print 'minus plus'
      ret = img[-(shift[0]):, 0:-shift[1]]
    else: #(-, -) case
      print 'negative', img.shape, shift[0]
      ret = img[-(shift[0]):, -(shift[1]):]
      
  print ret.shape
  return ret	  
  




	
    
      
      
      
      