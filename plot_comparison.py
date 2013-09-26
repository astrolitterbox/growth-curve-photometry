import numpy as np
from utils import *
import matplotlib as mpl
mpl.use('Agg')
import db
import math
import matplotlib.pyplot as plt
from califa_cmap import califa_vel

from matplotlib.ticker import MultipleLocator, FormatStrFormatter
majorLocator = MultipleLocator(1)

minorLocator = MultipleLocator(1)


from matplotlib import rcParams
rcParams['axes.labelsize'] = 11
rcParams['xtick.labelsize'] = 11
rcParams['ytick.labelsize'] = 11
rcParams['legend.fontsize'] = 11
rcParams['font.family'] = 'serif'
rcParams['font.serif'] = ['Computer Modern Roman']
rcParams['text.usetex'] = True
rcParams['patch.edgecolor'] = 'none'
rcParams['xtick.direction'] = 'in'     # direction: in or out
rcParams['ytick.direction'] = 'in'

rcParams['axes.linewidth']=2.0

def makeDiagonalLine(data):
  x1,x2,n,m,b = np.min(data),np.max(data),1000,1.,0. 
  x = np.r_[x1:x2:n*1j] #http://docs.scipy.org/doc/numpy/reference/generated/numpy.r_.html
  return x, m, b


#Settings
f = open('settings','r')
settings = eval(f.read())
dbDir = settings['dbDir']

bands = ['u', 'g', 'r', 'i']

mags = np.empty((939, 5))
mag_err = np.empty((939, 5))
petroMags = np.empty((939, 5))
phot_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'gc2_r')
ids = sqlify(phot_ids)

for i, band in enumerate(bands):
  mags[:, i] = db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc2_'+band, ' where califa_id in '+ids)
  mag_err[:, i] = db.dbUtils.getFromDB(band+'_err', dbDir+'CALIFA.sqlite', 'gc2_errors', ' where califa_id in '+ids)
  petroMags[:, i] = db.dbUtils.getFromDB('petroMag_'+band, dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id in '+ids)
  #sky[:, i] = db.dbUtils.getFromDB(band+'_sky', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_'+band, ' where califa_id in '+ids)
  
  #oldSky[:, i] = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id in '+ids)
  #oldSky[:, i][np.where(oldSky[:, i] > 1000)] = oldSky[:, i][np.where(oldSky[:, i] > 1000)] - 1000
  #sky[:, i][np.where(sky[:, i] > 1000)] = sky[:, i][np.where(sky[:, i] > 1000)] - 1000
  #oldIsoA[:, i] = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id in '+ids)

#because it's the same for all bands:
#isoA[:, 0] = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA_new_photometry.sqlite','sky_new', ' where califa_id in '+ids)

# r mag
'''
x, m, b = makeDiagonalLine([10, 16.5])
fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(petroMags, mags, c=petroMags-mags, cmap=califa_vel, s=8, edgecolor='k')
#c = ax.scatter(petroMags[:, 2], oldMags[:, 2], c='r', s=5, edgecolor="None")
ax.axis([10, 16.5, 10, 16.5])
plt.plot(x,m*x + b, c='k')

#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("SDSS r magnitude, mag")
plt.ylabel("GC r magnitude, mag")
plt.savefig('test/r_SDSS_vs_GC')

# g mag

x, m, b = makeDiagonalLine([10, 16.5])
fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(petroMags, mags, c=petroMags-mags, cmap=califa_vel, s=8, edgecolor='k')
#c = ax.scatter(petroMags[:, 2], oldMags[:, 2], c='r', s=5, edgecolor="None")
ax.axis([10, 16.5, 10, 16.5])
plt.plot(x,m*x + b, c='k')

#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("SDSS g magnitude, mag")
plt.ylabel("GC g magnitude, mag")
plt.savefig('test/g_SDSS_vs_GC')

# u mag

x, m, b = makeDiagonalLine([12, 20])
fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
c = ax.scatter(petroMags, mags, c=petroMags-mags, cmap=califa_vel, s=8, edgecolor='k')
#c = ax.scatter(petroMags[:, 2], oldMags[:, 2], c='r', s=5, edgecolor="None")
ax.axis([12, 20, 12, 20])
plt.plot(x,m*x + b, c='k')
plt.colorbar(c)
#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("SDSS u magnitude, mag")
plt.ylabel("GC u magnitude, mag")
plt.savefig('test/u_SDSS_vs_GC')
'''



limits = [[12, 18.5], [11.4, 16.5], [10, 16], [9.5, 16]]

for i, band in enumerate(bands):
  lim_lo = limits[i][0]
  lim_hi = limits[i][1]
  x, m, b = makeDiagonalLine([lim_lo, lim_hi])
  
  fig = plt.figure(figsize=(8, 8))  
  ax = plt.subplot(111)
  c = ax.scatter(petroMags[:, i], mags[:, i], c='k', s=8, edgecolor='k') 
  ax.axis([lim_lo, lim_hi, lim_lo, lim_hi])
  ax.errorbar(petroMags[:, i], mags[:, i], yerr=mag_err[:, i], mew=0, linestyle = "none", color="black")
  plt.plot(x,m*x + b, c='k')
  ax.xaxis.set_major_locator(majorLocator)
  ax.xaxis.set_minor_locator(minorLocator)
  ax.yaxis.set_major_locator(majorLocator)
  ax.yaxis.set_minor_locator(minorLocator)
  ax.minorticks_on()
  ax.tick_params('both', length=15, width=1, which='major')
  ax.tick_params('both', length=5, width=1, which='minor')
  plt.xlabel("SDSS "+band+" magnitude, mag")
  plt.ylabel("GC "+band+" magnitude, mag")
  plt.savefig('test/'+band+'_SDSS_vs_GC')
  #print band, "mean magnitude difference: ", np.mean(petroMags[:, i]) - np.mean(mags[:, i])


fig = plt.figure(figsize=(14, 14))  
for i, band in enumerate(bands):
  lim_lo = limits[i][0]
  lim_hi = limits[i][1]
  x, m, b = makeDiagonalLine([lim_lo, lim_hi])
  print i, lim_lo, lim_hi
  ax = plt.subplot(5, 1, i+1)
  c = ax.scatter(petroMags[:, i], mags[:, i], c='k', s=8, edgecolor='k') 
  ax.axis([lim_lo, lim_hi, lim_lo, lim_hi])
  ax.errorbar(petroMags[:, i], mags[:, i], yerr=mag_err[:, i], mew=0, linestyle = "none", color="black")
  plt.plot(x,m*x + b, c='k')
  ax.xaxis.set_major_locator(majorLocator)
  ax.xaxis.set_minor_locator(minorLocator)
  ax.yaxis.set_major_locator(majorLocator)
  ax.yaxis.set_minor_locator(minorLocator)
  ax.minorticks_on()
  ax.tick_params('both', length=15, width=1, which='major')
  ax.tick_params('both', length=5, width=1, which='minor')
  plt.xlabel("SDSS "+band+" magnitude, mag")
  plt.ylabel("GC "+band+" magnitude, mag")
plt.savefig('test/all_SDSS_vs_GC', bbox_inches='tight')  

exit()

#colours
fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(311)
ax.scatter(petroMags[:, 0] - petroMags[:, 2], mags[:, 0] - mags[:, 2], c='k', s=5)
plt.xlabel("u-r colour, SDSS")
plt.ylabel("u-r colour, GC")
ax.axis([0, 5, 0, 5])

ax = plt.subplot(312)
ax.scatter(petroMags[:, 2] - petroMags[:, 3], mags[:, 2] - mags[:, 3], c='k', s=5)
plt.xlabel("r-i colour, SDSS")
plt.ylabel("r-i colour, GC")
ax.axis([-0.6, 1, -0.6, 1])

print np.where((petroMags[:, 2] - petroMags[:, 3]) == np.min(petroMags[:, 2] - petroMags[:, 3]))
print petroMags[153, 2], petroMags[153, 3], mags[153, 2], mags[153, 3]

ax = plt.subplot(313)
ax.scatter(petroMags[:, 1] - petroMags[:, 3], mags[:, 1] - mags[:, 3], c='k', s=5)
plt.xlabel("g-i colour, SDSS")
plt.ylabel("g-i colour, GC")

ax.axis([0, 2, 0, 2])


plt.savefig('test/colours_vs_SDSS')