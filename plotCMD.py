import db
import numpy as np
import matplotlib.pyplot as plt

band = 'u'
secondBand = 'r'
new_ids = db.dbUtils.getFromDB('califa_id', '../db/CALIFA.sqlite', 'gc_new_'+band).astype('i')
print new_ids
new_ids = new_ids - 1

mag = db.dbUtils.getFromDB(band+'_mag', '../db/CALIFA.sqlite', 'gc_new_'+band).astype('f')

mag_old = db.dbUtils.getFromDB(band+'_mag', '../db/CALIFA.sqlite', 'gc')[new_ids]


mag_sdss = db.dbUtils.getFromDB('petromag_'+band, '../db/CALIFA.sqlite', 'mothersample')[new_ids]
secondMag = db.dbUtils.getFromDB(secondBand+'_mag', '../db/CALIFA.sqlite', 'gc_new_'+secondBand).astype('f')


fig = plt.figure()
ax = fig.add_subplot(211, aspect='equal')
ax.scatter(mag, mag_old)
plt.xlabel("GC magnitude")
plt.ylabel("GC magnitude, previous measurements")

ax = fig.add_subplot(212, aspect='equal')
ax.scatter(mag, mag_sdss)
plt.xlabel("GC magnitude")
plt.ylabel("SDSS magnitude")

plt.savefig('test/'+band+'_mags')
#plotting CMD
fig = plt.figure()
ax = fig.add_subplot(211, aspect='equal')
ax.scatter(mag-secondMag, mag)
plt.xlabel(band+'-'+secondBand+' color')
plt.ylabel("GC magnitude")

ax = fig.add_subplot(212, aspect='equal')
ax.scatter(mag, mag_sdss)
plt.xlabel("GC magnitude")
plt.ylabel("SDSS magnitude")

plt.savefig('test/'+band+'-'+secondBand+'_color')


