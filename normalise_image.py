# -*- coding: utf-8 -*-
import numpy as np
import pyfits

maskFile = pyfits.open('fits/mask_no_lanes.fits')
maskFile.info()
mask = maskFile[0].data
print np.mean(mask) #just checking
masked = np.where(mask != 0)
mask[masked] = mask[masked]/mask[masked]
print np.mean(mask) #just checking
hdu = pyfits.PrimaryHDU(mask)
hdu.writeto('fits/mask4.fits')
 
