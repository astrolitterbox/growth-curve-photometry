import pyfits
import numpy as np
band = 'r'


def read_pa_ba_values(fileName, galaxy):
  hdulist = pyfits.open(fileName)
  tbdata = hdulist[1].data 
  print galaxy, fileName, tbdata.field('Name').shape
  if galaxy in tbdata.field('Name'):
    ind = np.where(tbdata.field('Name') == galaxy)
    ba = tbdata.field('disc_ba')[ind]
    pa = tbdata.field('disc_PA')[ind]	  
    return ba[0], pa[0]
  else:
   raise Exception('NotInFile')
  	

barFile = 'GALFIT_discbarbulge.'+band+'.fits'
bulgeFile = 'GALFIT_discbulge.'+band+'.fits'
discFile = 'GALFIT_disc.'+band+'.fits'

val = []

galaxyList = np.genfromtxt('list.csv', dtype='object')


for galaxy in galaxyList:
  try:
    ba, pa = read_pa_ba_values(barFile, galaxy)
  except Exception:
    print 'no bar'
    try:
      ba, pa = read_pa_ba_values(bulgeFile, galaxy)
    except Exception:
      print 'no bulge'	
      ba, pa = read_pa_ba_values(discFile, galaxy)
  print ba, pa  
  val.append([galaxy, ba, pa])
val = np.asarray(val, dtype='object')
np.savetxt('ba_pa_values.csv', val, delimiter=',', fmt='%s, %f, %f')	  


