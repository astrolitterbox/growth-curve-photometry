import numpy as np
from utils import *
import matplotlib as mpl
mpl.use('Agg')
import db
import math
import matplotlib.pyplot as plt



def makeDiagonalLine(data):
  x1,x2,n,m,b = np.min(data),np.max(data),1000,1.,0. 
  x = np.r_[x1:x2:n*1j] #http://docs.scipy.org/doc/numpy/reference/generated/numpy.r_.html
  return x, m, b


#Settings
f = open('settings','r')
settings = eval(f.read())
dbDir = settings['dbDir']

bands = ['u', 'g', 'r', 'i', 'z']

mags = np.empty((937, 5))
oldMags = np.empty((937, 5))
oldSky = np.empty((937, 5))
sky = np.empty((937, 5))
isoA = np.empty((937, 1))
oldIsoA = np.empty((937, 5))
petroMags = np.empty((937, 5))
phot_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_r')
ids = sqlify(phot_ids)

for i, band in enumerate(bands):
  mags[:, i] = db.dbUtils.getFromDB(band+'_mag', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_'+band, ' where califa_id in '+ids)
  petroMags[:, i] = db.dbUtils.getFromDB('petroMag_'+band, dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id in '+ids)
  oldMags[:, i] = db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', band+'_tot', ' where califa_id in '+ids)
  oldSky[:, i] = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id in '+ids)
  if band == 'r':
    sky[:, i] = db.dbUtils.getFromDB('sky', dbDir+'CALIFA_new_photometry.sqlite', 'sky_new', ' where califa_id in '+ids)
  else:
    sky[:, i] = db.dbUtils.getFromDB(band+'_sky', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_'+band, ' where califa_id in '+ids)
  
  oldSky[:, i] = db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id in '+ids)
  oldSky[:, i][np.where(oldSky[:, i] > 1000)] = oldSky[:, i][np.where(oldSky[:, i] > 1000)] - 1000
  sky[:, i][np.where(sky[:, i] > 1000)] = sky[:, i][np.where(sky[:, i] > 1000)] - 1000
  oldIsoA[:, i] = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA.sqlite', 'sky_fits_'+band, ' where califa_id in '+ids)

#because it's the same for all bands:
isoA[:, 0] = db.dbUtils.getFromDB('isoA', dbDir+'CALIFA_new_photometry.sqlite','sky_new', ' where califa_id in '+ids)

# r mag

fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(petroMags[:, 2], mags[:, 2], c='k', s=5)
c = ax.scatter(petroMags[:, 2], oldMags[:, 2], c=np.abs(mags[:, 2] - oldMags[:, 2]), s=5, edgecolor="None")
plt.colorbar(c)
ax.axis([10, 16.5, 10, 16.5])
#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("SDSS r magnitude, mag")
plt.ylabel("GC r magnitude, mag")
plt.savefig('test/r_SDSS_vs_GC')

fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(oldMags[:, 2], mags[:, 2], c='k', s=5)
#plt.colorbar(c)
ax.axis([10, 16.5, 10, 16.5])
#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("Old GC r magnitude, mag")
plt.ylabel("New GC r magnitude, mag")
plt.savefig('test/r_GC_vs_GC')


# u mag

fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(petroMags[:, 0], mags[:, 0], c='k', s=5)
c = ax.scatter(petroMags[:, 0], oldMags[:, 0], c=np.abs(mags[:, 0] - oldMags[:, 0]), s=5, edgecolor="None")
plt.colorbar(c)
ax.axis([12, 20, 12, 20])
#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("SDSS u magnitude, mag")
plt.ylabel("GC u magnitude, mag")
plt.savefig('test/u_SDSS_vs_GC')

fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(111)
ax.scatter(oldMags[:, 0], mags[:, 0], c='k', s=5)
#c = ax.scatter(petroMags[:, 0], oldMags[:, 0], c=np.abs(mags[:, 0] - oldMags[:, 0]), s=5, edgecolor="None")
#plt.colorbar(c)
ax.axis([12, 20, 12, 20])
#ax.line([[10, 10], [16.5, 16.5]])
plt.xlabel("Old GC u magnitude, mag")
plt.ylabel("New GC u magnitude, mag")
plt.savefig('test/u_GC_vs_GC')




#colours
fig = plt.figure(figsize=(8, 8))  
ax = plt.subplot(211)
ax.scatter(petroMags[:, 0] - petroMags[:, 2], mags[:, 0] - mags[:, 2], c='k', s=5)
plt.xlabel("u-r colour, SDSS")
plt.ylabel("u-r colour, GC")
ax.axis([0, 5, 0, 5])

ax = plt.subplot(212)
ax.scatter(petroMags[:, 0] - petroMags[:, 2], oldMags[:, 0] - oldMags[:, 2], c='k', s=5)
plt.xlabel("u-r colour, SDSS")
plt.ylabel("u-r colour, old GC")
ax.axis([0, 5, 0, 5])

plt.savefig('test/u_r_colour')

#g - i
fig = plt.figure(figsize=(8, 12))  
ax = plt.subplot(411)
ax.scatter(petroMags[:, 1] - petroMags[:, 3], mags[:, 1] - mags[:, 3], c='k', s=5)
plt.xlabel("g-i colour, SDSS")
plt.ylabel("g-i colour, GC")
ax.axis([-0.5, 2.5, -0.5, 2.5])


ax = plt.subplot(412)
ax.scatter(petroMags[:, 1] - petroMags[:, 3], oldMags[:, 1] - oldMags[:, 3], c='k', s=5)
plt.xlabel("g-i colour, SDSS")
plt.ylabel("g-i colour, old GC")
#ax.axis([0, 5, 0, 5])

ax = plt.subplot(413)
ax.scatter(oldMags[:, 1], mags[:, 1], c='k', s=5)
plt.xlabel("g mag, old GC")
plt.ylabel("g mag, GC")

ax = plt.subplot(414)
ax.scatter(oldMags[:, 3], mags[:, 3], c='k', s=5)
plt.xlabel("i mag, old  GC")
plt.ylabel("i mag, GC")

plt.savefig('test/g_i_colour')


#all magnitudes



fig = plt.figure(figsize=(14, 14))  
ax = plt.subplot(511)
x, m, b = makeDiagonalLine(petroMags[:, 0])
ax.scatter(petroMags[:, 0], oldMags[:, 0], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("u mag, SDSS")
plt.ylabel("u mag, old GC")
#ax.axis([-0.5, 2.5, -0.5, 2.5])


ax = plt.subplot(512)
x, m, b = makeDiagonalLine(petroMags[:, 1])
ax.scatter(petroMags[:, 1], oldMags[:, 1], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("g mag, SDSS")
plt.ylabel("g mag, old GC")
#ax.axis([0, 5, 0, 5])

ax = plt.subplot(513)
x, m, b = makeDiagonalLine(petroMags[:, 2])
ax.scatter(petroMags[:, 2], oldMags[:, 2], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("r mag, SDSS")
plt.ylabel("r mag, old GC")

ax = plt.subplot(514)
x, m, b = makeDiagonalLine(petroMags[:, 3])
ax.scatter(petroMags[:, 3], oldMags[:, 3], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("i mag, SDSS")
plt.ylabel("i mag, old GC")

ax = plt.subplot(515)
x, m, b = makeDiagonalLine(petroMags[:, 4])
ax.scatter(petroMags[:, 4], oldMags[:, 4], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("z mag, SDSS")
plt.ylabel("z mag, old GC")
plt.savefig("test/all_mags_comparison")

#all mags, new GC

fig = plt.figure(figsize=(14, 14))  
ax = plt.subplot(511)
x, m, b = makeDiagonalLine(petroMags[:, 0])
ax.scatter(petroMags[:, 0], mags[:, 0], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("u mag, SDSS")
plt.ylabel("u mag, GC")
#ax.axis([-0.5, 2.5, -0.5, 2.5])


ax = plt.subplot(512)
x, m, b = makeDiagonalLine(petroMags[:, 1])
ax.scatter(petroMags[:, 1], mags[:, 1], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("g mag, SDSS")
plt.ylabel("g mag, GC")
#ax.axis([0, 5, 0, 5])

ax = plt.subplot(513)
x, m, b = makeDiagonalLine(petroMags[:, 2])
ax.scatter(petroMags[:, 2], mags[:, 2], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("r mag, SDSS")
plt.ylabel("r mag, GC")

ax = plt.subplot(514)
x, m, b = makeDiagonalLine(petroMags[:, 3])
ax.scatter(petroMags[:, 3], mags[:, 3], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("i mag, SDSS")
plt.ylabel("i mag, GC")

ax = plt.subplot(515)
x, m, b = makeDiagonalLine(petroMags[:, 4])
ax.scatter(petroMags[:, 4], mags[:, 4], c='k', s=5)
plt.plot(x,m*x + b, c='g')
plt.xlabel("z mag, SDSS")
plt.ylabel("z mag, GC")
plt.savefig("test/all_mags_comparison_new_GC")



#sky values comparison

fig = plt.figure(figsize=(14, 14))  
ax = plt.subplot(511)
ax.scatter(oldSky[:, 0], oldSky[:, 0] - sky[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("u band sky, old GC")
plt.ylabel("old GC sky - GC sky")


ax = plt.subplot(512)
ax.scatter(oldSky[:, 1], oldSky[:, 1] - sky[:, 1], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("g band sky, old GC")
plt.ylabel("old GC sky - GC sky")


ax = plt.subplot(513)
ax.scatter(oldSky[:, 2], oldSky[:, 2] - sky[:, 2], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("r band sky, old GC")
plt.ylabel("old GC sky - GC sky")

ax = plt.subplot(514)
ax.scatter(oldSky[:, 3], oldSky[:, 3] - sky[:, 3], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("i band sky, old GC")
plt.ylabel("old GC sky - GC sky")

ax = plt.subplot(515)
ax.scatter(oldSky[:, 4], oldSky[:, 4] - sky[:, 4], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("z band sky, old GC")
plt.ylabel("old GC sky - GC sky")

plt.savefig("test/sky_comparison_new_GC")


#isoA values comparison


fig = plt.figure(figsize=(14, 14))  
ax = plt.subplot(511)
ax.scatter(oldIsoA[:, 0], oldIsoA[:, 0] - isoA[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("u band radius, old GC")
plt.ylabel("old radius - new GC radius")


ax = plt.subplot(512)
ax.scatter(oldIsoA[:, 1], oldIsoA[:, 1] - isoA[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("g band radius, old GC")
plt.ylabel("old radius - new GC radius")


ax = plt.subplot(513)
ax.scatter(oldIsoA[:, 2], oldIsoA[:, 2] - isoA[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("r band radius, old GC")
plt.ylabel("old radius - new GC radius")

ax = plt.subplot(514)
ax.scatter(oldIsoA[:, 3], oldIsoA[:, 3] - isoA[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("i band radius, old GC")
plt.ylabel("old radius - new GC radius")

ax = plt.subplot(515)
ax.scatter(oldIsoA[:, 4], oldIsoA[:, 4] - isoA[:, 0], c='k', s=5)
plt.axhline(c='g')
plt.xlabel("z band radius, old GC")
plt.ylabel("old radius - new GC radius")

plt.savefig("test/isoA_comparison_new_GC")



