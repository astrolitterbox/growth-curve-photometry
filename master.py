# -*- coding: utf-8 -*-
#import Interpol
#import getImages
import pyfits
import os
import string
import gzip
import csv
import utils


class GalaxyParameters:
  @staticmethod
  def SDSS(listFile, ID):
    ret = GalaxyParameters()
    CALIFAID_col = 0
    ra_col = 1
    dec_col = 2
    run_col = 7
    rerun_col = 8
    camcol_col = 9
    field_col = 10
    with open(listFile, 'rb') as f:
	mycsv = csv.reader(f)
	mycsv = list(mycsv)	
	ret.CALIFAID = string.strip(mycsv[ID][CALIFAID_col])
	ret.ra = string.strip(mycsv[ID][ra_col])
	ret.dec = string.strip(mycsv[ID][dec_col])
	ret.run = string.strip(mycsv[ID][run_col])
	ret.rerun = string.strip(mycsv[ID][rerun_col])
	ret.camcol = string.strip(mycsv[ID][camcol_col])
	ret.field = string.strip(mycsv[ID][field_col])
	ret.runstr = utils.run2string(ret.run)
	ret.field_str = utils.field2string(ret.field)	
    return ret

  
  @staticmethod
  def getTsFieldFiles(listFile, noOfGalaxies):
      for i in range(0, noOfGalaxies):
	run = GalaxyParameters.SDSS(listFile, i).run
	rerun = GalaxyParameters.SDSS(listFile, i).rerun
	camcol = GalaxyParameters.SDSS(listFile, i).camcol
	field = GalaxyParameters.SDSS(listFile, i).field
	runstr = GalaxyParameters.SDSS(listFile, i).runstr
	field_str = GalaxyParameters.SDSS(listFile, i).field_str
	#http://das.sdss.org/imaging/5115/40/calibChunks/2/tsField-005115-2-40-0023.fit
	
	print 'wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
	
	'''
	print 'wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz'
	os.system('wget http://das.sdss.org/imaging/'+run+'/'+rerun+'/corr/'+camcol+'/fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
	print 'uncompressing..'
	gz = gzip.open('fpC-'+runstr+'-r'+camcol+'-'+field_str+'.fit.gz')
	imgFile = pyfits.open(gz, mode='readonly')
	print 'getting header info...'  '''

def main():

  listFile = '../data/SDSS_photo_match.csv'
  fitsDir = '../data/SDSS/'
  dataDir = '../data'
  outputFile = '../data/growthCurvePhotometry.csv'
  imgDir = 'img/'
  noOfGalaxies = 939
  
  print GalaxyParameters.getTsFieldFiles(listFile, noOfGalaxies)

  
if __name__ == "__main__":
  main()
