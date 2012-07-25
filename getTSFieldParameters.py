import ellipse_photometry as e
import pyfits


def getParams(listFile, ID):
      filterNumber = 2 #(0, 1, 2, 3, 4 - ugriz SDSS filters)     
      run = e.GalaxyParameters.SDSS(listFile, ID).run
      rerun = e.GalaxyParameters.SDSS(listFile, ID).rerun
      camcol = e.GalaxyParameters.SDSS(listFile, ID).camcol
      field = e.GalaxyParameters.SDSS(listFile, ID).field
      runstr = e.GalaxyParameters.SDSS(listFile, ID).runstr
      field_str = e.GalaxyParameters.SDSS(listFile, ID).field_str
	#http://das.sdss.org/imaging/5115/40/calibChunks/2/tsField-005115-2-40-0023.fit
      print 'http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit'
      tsFile = pyfits.open('http://das.sdss.org/imaging/'+run+'/'+rerun+'/calibChunks/'+camcol+'/tsField-'+runstr+'-'+camcol+'-'+rerun+'-'+field_str+'.fit', mode='readonly')
      print 'opened'
      img = tsFile[1].data
      #indexing -- field numbering in documentation starts with 0, hence #27 instead of #28 field, etc
      zpt_r = list(img.field(27))[0][filterNumber]
      ext_coeff = list(img.field(33))[0][filterNumber]
      airmass = list(img.field(22))[0][filterNumber]
      params = [zpt_r, ext_coeff, airmass]
      return params
