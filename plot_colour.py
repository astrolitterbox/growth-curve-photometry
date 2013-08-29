import numpy as np
from utils import *
import matplotlib as mpl
mpl.use('Agg')
import db
import math
import matplotlib.pyplot as plt




#Settings
f = open('settings','r')
settings = eval(f.read())
dbDir = settings['dbDir']

bands = ['u', 'g', 'r', 'i']

mags = np.empty((937, 5))
oldMags = np.empty((937, 5))
petroMags = np.empty((937, 5))
phot_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_r')
ids = sqlify(phot_ids)

for i, band in enumerate(bands):
  mags[:, i] = db.dbUtils.getFromDB(band+'_mag', dbDir+'CALIFA_new_photometry.sqlite', 'gc_new_'+band, ' where califa_id in '+ids)
  petroMags[:, i] = db.dbUtils.getFromDB('petroMag_'+band, dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id in '+ids)
  oldMags[:, i] = db.dbUtils.getFromDB(band, dbDir+'CALIFA.sqlite', 'gc_results', ' where califa_id in '+ids)

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

#morphtypes

Hubtype = np.asarray(decodeU(db.dbUtils.getFromDB('Hubtype', dbDir+'CALIFA.sqlite', 'morph', ' where califa_id in '+ids)))
HubSubType = np.asarray(decodeU(db.dbUtils.getFromDB('HubSubtype', dbDir+'CALIFA.sqlite', 'morph', ' where califa_id in '+ids)))
n = db.dbUtils.getFromDB('n', dbDir+'CALIFA.sqlite', 'galfit', ' where califa_id in '+ids)

morphtypes = np.empty((Hubtype.shape[0], 1), dtype = 'object')
for i, galaxy in enumerate(Hubtype):
  morphtypes[i] = galaxy+HubSubType[i]
#print morphtypes

resolution = 'hubtype'

morph = getMorphNumbers(morphtypes, resolution)

types = ['EO', 'E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'S0', 'S0a', 'Sa', 'Sab', 'Sb', 'Sbc', 'Sc', 'Scd', 'Sd', 'Sdm', 'Sm', 'Ir']

#clipped_col = np.clip(col, np.mean(col)-3*np.std(col), np.mean(col)+3*np.std(col))

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111)
mean = np.mean(mags[:, 1] - mags[:, 3])
sigma = np.std(mags[:, 1] - mags[:, 3])
print sigma, mean, mags[:, 1] - mags[:, 3]
p = plt.scatter(morph, n, c=np.clip(mags[:, 1] - mags[:, 3], mean-sigma, mean+sigma), alpha=0.9, s=30)
plt.ylabel(r"S$\'{e}$rsic n")
plt.xlabel("Hubble type")
plt.xlim(-0.2, 20)
plt.ylim(-0, 8)
Minor_formatter = mpl.ticker.FixedFormatter(types)
majorLocator = mpl.ticker.MultipleLocator(1)
#cbar = plt.colorbar(p)
ax.xaxis.set_major_locator(majorLocator)
ax.xaxis.set_major_formatter(Minor_formatter)

#cbar.ax.set_ylabel("g-r color")
plt.savefig("test/morphtypes_vs_color")


