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
            raise ValueError("Number ranges higher than max value of %s\n" % nmax)
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
  



csvReader = csv.reader(open(dataFile, "rU"), delimiter=',')
#f = csv.writer(open('pix.txt', 'w'), delimiter=',')
for row in csvReader:
      #print '********************************', row[0]      
      ID = string.strip(row[0])
      ra = string.strip(row[1])
      dec = string.strip(row[2])
      run = string.strip(row[3])
      rerun = string.strip(row[4])
      camcol = string.strip(row[5])
      field = string.strip(row[6])
      runstr = run2string(run)
      field_str = field2string(field)
      #print 'wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-g'+camcol+'-'+field_str+'.fit.gz'
      #os.system('wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-g'+camcol+'-'+field_str+'.fit.gz')     
      #os.system('pwd')
      try:
	print ID
	gz = gzip.open('fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz')
	imgFile = pyfits.open(gz, mode='readonly')
	print 'getting header info...'
	rgz = gzip.open('../fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
	imgFiler = pyfits.open(rgz, mode='readonly')
	WCSr=astWCS.WCS('../fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')	
	WCS=astWCS.WCS('fpC-'+runstr+'-'+band+camcol+'-'+field_str+'.fit.gz')
	band_center = WCS.wcs2pix(WCS.getCentreWCSCoords()[0], WCS.getCentreWCSCoords()[1]) #'other band image center coords in r image coordinate system'
	r_center = WCS.wcs2pix(WCSr.getCentreWCSCoords()[0], WCSr.getCentreWCSCoords()[1]) #'r center coords in r image coordinate system'
	shift = [band_center[0] - r_center[0], band_center[1] - r_center[1]]
	print type(shift)
	shift = [ceil(shift[0]), ceil(shift[1])]
	print shift, img.shape
	a= getShiftedImage(img, shift)

      except IOError:
	print ID,  'is missing'
	
    
      
      
      
      