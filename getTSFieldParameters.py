# -*- coding: utf-8 -*-
import galaxyParameters as e
import pyfits


def getParams(ID, filterNumber):
      filterNumber = filterNumber #(0, 1, 2, 3, 4 - ugriz SDSS filters)     
      run = e.GalaxyParameters.SDSS(ID).run
      rerun = e.GalaxyParameters.SDSS(ID).rerun
      camcol = e.GalaxyParameters.SDSS(ID).camcol
      field = e.GalaxyParameters.SDSS(ID).field
      runstr = e.GalaxyParameters.SDSS(ID).runstr
      field_str = e.GalaxyParameters.SDSS(ID).field_str
	#http://das.sdss.org/imaging/5115/40/calibChunks/2/tsField-005115-2-40-0023.fit
      print 'STR -- http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
      
      try:
	tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')
	print 'opened'
	img = tsFile[1].data
	#indexing -- field numbering in documentation starts with 0, hence #27 instead of #28 field, etc
	zpt_r = list(img.field(27))[0][filterNumber]
	ext_coeff = list(img.field(33))[0][filterNumber]
	airmass = list(img.field(22))[0][filterNumber]
	
	print zpt_r, ext_coeff, airmass, '-------------------'
	params = [zpt_r, ext_coeff, airmass]
      except IOError as err:
	params = [-24, 0.1, 1.2]
	print 'default params', err
      return params
