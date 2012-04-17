# -*- coding: utf-8 -*-
import pyfits
import numpy as np
import utils
#print head


#print atlasData.field('IAUNAME')

def find_mag(ra, dec):
    r_band = 4
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


