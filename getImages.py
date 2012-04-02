# -*- coding: utf-8 -*-
import os
import pyfits
import csv
import numpy
import string
import gzip


#awk < CALIFA.csv 'BEGIN { FS="," }; { print $1,",",$2,",",$3,",",$8,",",$9,",",$10,",",$11}' > list.txt

dataFile = 'list.txt'

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


PA = []
csvReader = csv.reader(open(dataFile, "rU"), delimiter=',')
f = csv.writer(open('Position_angles.txt', 'w'), delimiter=',')
for row in csvReader:
      print '********************************', row[0]      
      CALIFAID = string.strip(row[0])
      ra = string.strip(row[1])
      dec = string.strip(row[2])
      run = string.strip(row[3])
      rerun = string.strip(row[4])
      camcol = string.strip(row[5])
      field = string.strip(row[6])
      runstr = run2string(run)
      field_str = field2string(field)
      print 'wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'
      os.system('wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
      print 'uncompressing..'
      gz = gzip.open('fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
      imgFile = pyfits.open(gz, mode='readonly')
      print 'getting header info...'
      head = imgFile[0].header
      angle = head['SPA']
      info = (int(CALIFAID), angle)
      #PA.append(info)
      #print PA    
      f.writerow(info)
#numpy.savetxt('', PA)

