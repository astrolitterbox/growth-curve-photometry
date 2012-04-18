# -*- coding: utf-8 -*-
import numpy
import string
import csv
import scipy

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

def checkFilenames(noOfGalaxies, listFile, dataDir, simpleFile):
  with open('../data/maskFilenames.csv', 'wb') as f:
    writer = csv.writer(f)
    maskFilenames = []
    for i in range(0, noOfGalaxies):
      maskFile = GalaxyParameters.getMaskUrl(listFile, dataDir, simpleFile, i)
      try:
	a = open(maskFile)
	print "maskfile exists:", maskFile
	out = (GalaxyParameters.SDSS(listFile, i).CALIFAID, maskFile)
	writer.writerow(out)
      except IOError as e:
	out = (GalaxyParameters.SDSS(listFile, i).CALIFAID, '***************************')
	writer.writerow(out)
	maskFilenames.append(maskFile)
	print GalaxyParameters.SDSS(listFile, i).ra, GalaxyParameters.SDSS(listFile, i).dec
  return maskFilenames
  
def getMask(maskFile, ID):
   with open(maskFile, 'rb') as f:
     fname_col = 2
     reader = csv.reader(f)
     mycsv = list(reader)
     fname = string.strip(mycsv[ID][1])
   return fname  
   
def createOutputFilename(sdssFilename):
  sdssFilename = sdssFilename.lstrip('../data/SDSS/')
  outputFilename = sdssFilename[:-3]+'s'
  return outputFilename
  
  
  
def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    size = int(size)
    if not sizey:
        sizey = size
    else:
        sizey = int(sizey)
    x, y = scipy.mgrid[-size:size+1, -sizey:sizey+1]
    g = scipy.exp(-(x**2/float(size)+y**2/float(sizey)))
    return g / g.max()
  
def nmgy2mag(nmgy, ivar=None):
    """
    Taken from http://sdsspy.googlecode.com/hg/sdsspy/util.py
    Name:
        nmgy2mag
    Purpose:
        Convert SDSS nanomaggies to a log10 magnitude.  Also convert
        the inverse variance to mag err if sent.  The basic formulat
        is 
            mag = 22.5-2.5*log_{10}(nanomaggies)
    Calling Sequence:
        mag = nmgy2mag(nmgy)
        mag,err = nmgy2mag(nmgy, ivar=ivar)
    Inputs:
        nmgy: SDSS nanomaggies.  The return value will have the same
            shape as this array.
    Keywords:
        ivar: The inverse variance.  Must have the same shape as nmgy.
            If ivar is sent, then a tuple (mag,err) is returned.

    Outputs:
        The magnitudes.  If ivar= is sent, then a tuple (mag,err)
        is returned.

    Notes:
        The nano-maggie values are clipped to be between 
            [0.001,1.e11]
        which corresponds to a mag range of 30 to -5
    """
    nmgy = numpy.array(nmgy, ndmin=1, copy=False)

    nmgy_clip = numpy.clip(nmgy,0.001,1.e11)

    mag = nmgy_clip.copy()
    mag[:] = 22.5-2.5*scipy.log10(nmgy_clip)

    if ivar is not None:

        ivar = numpy.array(ivar, ndmin=1, copy=False)
        if ivar.shape != nmgy.shape:
            raise ValueError("ivar must be same shape as input nmgy array")

        err = mag.copy()
        err[:] = 9999.0

        w=where( ivar > 0 )

        if w[0].size > 0:
            err[w] = sqrt(1.0/ivar[w])

            a = 2.5/log(10)
            err[w] *= a/nmgy_clip[w]

        return mag, err
    else:
        return mag

  