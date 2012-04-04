# -*- coding: utf-8 -*-
import numpy
import string
import csv


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
  