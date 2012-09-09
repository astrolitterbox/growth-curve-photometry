# -*- coding: utf-8 -*-
import pyfits
import numpy as np
import utils
#print head
import collections
import db

dbDir = '../db/'

#print atlasData.field('IAUNAME')





def find_mag(ra, dec):
    r_band = 4
    #atlasFile = '/media/46F4A27FF4A2713B_/work/nsa_v0_1_2.fits'
    atlasFile = '../data/NSAtlas/nsa_v0_1_2.fits'
    atlas = pyfits.open(atlasFile)
    atlasData = atlas[1].data
#    print atlas[1].columns.names

    head = atlas[1].header
    #print atlasData.field('RA')[15], atlasData.field('DEC')[15]
    for i in range(0, atlasData.shape[0]):
      if (round(atlasData.field('RA')[i], 3) == round(ra, 3)) and (round(atlasData.field('DEC')[i], 3) == round(dec, 3)):
	print 'i', i, round(atlasData.field('RA')[i], 3), round(atlasData.field('DEC')[i], 3)
	return utils.nmgy2mag(atlasData.field('NMGY')[i][r_band])
      #else:
	#print 'object not found!'

def find_in_atlas(arg, ra, dec, roundParam, spiralID):
    r_band = 4
    atlasFile = '../data/NSAtlas/nsa_v0_1_2.fits'
    atlas = pyfits.open(atlasFile)
    atlasData = atlas[1].data
#    print atlas[1].columns.names  
    head = atlas[1].header
    #print atlasData.field('RA')[15], atlasData.field('DEC')[15]
    '''for i in range(0, atlasData.shape[0]):
      if (round(atlasData.field('RA')[i], 3) == round(ra, 3)) and (round(atlasData.field('DEC')[i], 3) == round(dec, 3)):
	print 'i', i, round(atlasData.field('RA')[i], 3), round(atlasData.field('DEC')[i], 3)
	return atlasData.field(arg)[i]
      #else:
	#print '''
    ret = np.empty((len(ra), 5))
    for i in range(0, len(ra)):
      
      decs = np.where(np.round(atlasData.field('DEC'), roundParam) == round(dec[i], roundParam))
      ras = np.where(np.round(atlasData.field('RA'), roundParam) == round(ra[i], roundParam))
      #print round(ras, 3), round(decs, 3)
      print 'ra: ', ras[0], 'dec', decs[0]
    
      a_multiset = collections.Counter(list(ras[0]))
      b_multiset = collections.Counter(list(decs[0]))
      overlap = list((a_multiset & b_multiset).elements())
      print 'o', overlap, spiralID[i]

      if overlap != []:	
	ret[i][1] =  atlasData.field('ra')[overlap]
	ret[i][2] = atlasData.field('dec')[overlap]      
	ret[i][3] =  atlasData.field(arg)[overlap][0][r_band]
	ret[i][4] = atlasData.field('SERSIC_TH50')[overlap]
	
      else:
	ret[i][1] =  ra[i]
	ret[i][2] = dec[i]
	ret[i][3] = 0
	ret[i][4] = 0
      ret[i][0] = spiralID[i]
      print 'id', ret[i]
    
    atlas.close()	
    return ret
    #print np.where((np.round(atlasData.field('RA'), 3) == round(ra, 3)))# and np.round(atlasData.field('DEC'), 3) == round(dec, 3)))
    #print np.where(np.round(atlasData.field('RA'), 3) == round(ra, 3))]#.field(arg)



'''

    #getting Sloan Atlas data:
ra = utils.convert(db.dbUtils.getFromDB('ra', dbDir+'CALIFA.sqlite', 'mothersample'))
print ra, 'ra', len(ra), len(np.arange(1, 940, 1))

dec = utils.convert(db.dbUtils.getFromDB('dec', dbDir+'CALIFA.sqlite', 'mothersample'))
Atlas_mag = find_in_atlas('NMGY', ra, dec, 3, np.arange(1, 940, 1))
Atlas_mag[:, 3] = utils.nmgy2mag(Atlas_mag[:, 3])
np.savetxt('atlas_magnitudes.txt', Atlas_mag, fmt=('%i', '%f8', '%f8', '%f4', '%f4'))

'''