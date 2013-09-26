# -*- coding: utf-8 -*-
import numpy as np
from string import *
import csv
#import scipy
import itertools
import db

TFDir = "./"
#Settings
f = open('settings','r')
settings = eval(f.read())
dbDir = settings['dbDir']


def getDBData(califa_id):
    paOrig = db.dbUtils.getFromDB('pa_align', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+califa_id)[0]
    pa = np.radians(90 - paOrig)
    r90 = 0.396*db.dbUtils.getFromDB('r90', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id = '+califa_id)[0]    
    ba = db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'BestBA', ' where califa_id = '+califa_id)[0]
    r50 = db.dbUtils.getFromDB('hlma', dbDir+'CALIFA.sqlite', 'gc_results', ' where califa_id = '+califa_id)[0]
    cz = 300000*db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id = '+califa_id)[0]
    l_sc = db.dbUtils.getFromDB('scalelength', dbDir+'CALIFA.sqlite', 'scale_lengths', ' where califa_id = '+califa_id)[0]    
    return (pa, r90, ba, r50, cz, l_sc)


def mode(a, axis=0):
    scores = np.unique(np.ravel(a))       # get ALL unique values
    testshape = list(a.shape)
    testshape[axis] = 1
    oldmostfreq = np.zeros(testshape)
    oldcounts = np.zeros(testshape)

    for score in scores:
        template = (a == score)
        counts = np.expand_dims(np.sum(template, axis),axis)
        mostfrequent = np.where(counts > oldcounts, score, oldmostfreq)
        oldcounts = np.maximum(counts, oldcounts)
        oldmostfreq = mostfrequent
    
    return mostfrequent[0]



def getHubbleType(califa_id):
    HubType = db.dbUtils.getFromDB('hubtype', dbDir+'CALIFA.sqlite', 'morph', ' where califa_id = '+califa_id)[0]
    HubSubType = db.dbUtils.getFromDB('hubsubtype', dbDir+'CALIFA.sqlite', 'morph', ' where califa_id = '+califa_id)[0]
    return str(decodeU(HubType)[0])+str(decodeU(HubSubType)[0])



def getMorphNumbers(morphtype, resolution):
  
  numbers = np.empty((morphtype.shape), dtype=int)
  if resolution == 'hubtype':

    numbers[np.where(morphtype == 'E0')] = 0
    numbers[np.where(morphtype == 'E1')] = 1
    numbers[np.where(morphtype == 'E2')] = 2
    numbers[np.where(morphtype == 'E3')] = 3
    numbers[np.where(morphtype == 'E4')] = 4
    numbers[np.where(morphtype == 'E5')] = 5
    numbers[np.where(morphtype == 'E6')] = 6
    numbers[np.where(morphtype == 'E7')] = 7
    numbers[np.where(morphtype == 'S0')] = 8
    numbers[np.where(morphtype == 'S0a')] = 9
    numbers[np.where(morphtype == 'Sa')] = 10
    numbers[np.where(morphtype == 'Sab')] = 11
    numbers[np.where(morphtype == 'Sb')] = 12
    numbers[np.where(morphtype == 'Sbc')] = 13
    numbers[np.where(morphtype == 'Sc')] = 14
    numbers[np.where(morphtype == 'Scd')] = 15
    numbers[np.where(morphtype == 'Sd')] = 16
    numbers[np.where(morphtype == 'Sdm')] = 17
    numbers[np.where(morphtype == 'Sm')] = 18
    numbers[np.where(morphtype == 'Ir')] = 19
      
  elif resolution == 'barredness':
    numbers[np.where(morphtype == 'A')] = 0
    numbers[np.where(morphtype == 'AB')] = 1
    numbers[np.where(morphtype == 'B')] = 2

  elif resolution == 'merger':
    numbers[np.where(morphtype == 'I')] = 0
    numbers[np.where(morphtype == 'M')] = 1
  print len(np.unique(numbers)), 'nu'
  return numbers


def make_list(names):
	petro_ids = []
	for i in names:
	      petro_ids.append(str(i[0]))
	return petro_ids


def sqlify(arr):
  strings = ''
  for i in arr:
     if type(i) == type(tuple()):
        i = i[0]   
     strings = strings+","+'"'+strip(str(i))+'"'
  strings = '('+strings[1:]+')'
  return strings

def UGCXmatch(galNames):

  names = []
  for n in galNames:
    #n = 
    if find(n, 'UGC') != -1:
      n = strip(n)
      catNr = lstrip(str(n), 'UGC')
      m = 'UGC'+zfill(catNr, 5)    
      names.append(m)
  return names

def decodeU(query_output):
  output = []
  for u in query_output:
    u = str(u)
    output.append(u)
  return output


def writeOut(output, filename='log.csv'):
   print output
   f = open(filename,'aw')
   w = csv.writer(f)
   w.writerow(output)
   f.close()

def getSlope(y1, y2, x1, x2):
	#print  (abs(y2 - y1)/abs(x2 - x1)), 'slope', y1, y2, x1, x2
  	return (y2 - y1)/(x2 - x1)

def createIndexArray(inputShape):
  shape = (inputShape[0]*inputShape[1], 2)
  inputIndices = np.zeros(shape, dtype = int) 
  k = 0
  for i in range(0, inputShape[0]):
    for j in range(0, inputShape[1]):  
      inputIndices[k, 0] = j
      inputIndices[k, 1] = i
      k+=1
  #np.savetxt('inputIndices.txt', inputIndices, fmt = '%8i')    
  return np.asarray(inputIndices)


def convert(data):
     tempDATA = []
     for i in data:
         tempDATA.append([float(j) for j in i])
     return np.asarray(tempDATA)

def unique_rows(a):
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


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
    if not np.isscalar(val):
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
  with open(dataDir+'/maskFilenames.csv', 'wb') as f:
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
     fname = strip(mycsv[ID][1])
     print fname
   return fname  
   
def rFilename(ID):
  ID = ID+1
  fitsDir = Settings.getConstants().dataDir+'SDSS/'
  ra = GalaxyParameters.SDSS(int(ID) - 1).ra
  dec = GalaxyParameters.SDSS(int(ID) - 1).dec
  run = GalaxyParameters.SDSS(int(ID) - 1).run
  rerun = GalaxyParameters.SDSS(int(ID) - 1).rerun
  camcol = GalaxyParameters.SDSS(int(ID) - 1).camcol
  field = GalaxyParameters.SDSS(int(ID) - 1).field
  runstr = GalaxyParameters.SDSS(int(ID) - 1).runstr
  field_str = sdss.field2string(field)
  rFile = fitsDir+'r/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'
  return rFile

   
def createOutputFilename(sdssFilename, dataDir):
  sdssFilename = sdssFilename.lstrip(dataDir+'/SDSS/')
  outputFilename = sdssFilename[:-3]+'s'
  return outputFilename
  
  
'''  
def gauss_kern(size, sizey=None):
    """ Returns a normalized 2D gauss kernel array for convolutions """
    #size = int(size)
    #if not sizey:
    #    sizey = size
    #else:
    #    sizey = int(sizey)
    #x, y = scipy.mgrid[-size:size+1, -sizey:sizey+1]
    #g = scipy.exp(-(x**2/float(size)+y**2/float(sizey)))
    #return g / g.max()
    g = np.genfromtxt('gauss.csv')
    
    return g
'''
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
    nmgy = np.array(nmgy, ndmin=1, copy=False)

    nmgy_clip = np.clip(nmgy,0.001,1.e11)

    mag = nmgy_clip.copy()
    mag[:] = 22.5-2.5*scipy.log10(nmgy_clip)

    if ivar is not None:

        ivar = np.array(ivar, ndmin=1, copy=False)
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


  
#np.savetxt('gauss.csv', gauss_kern(2, sizey=None))
