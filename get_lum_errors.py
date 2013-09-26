import db
import numpy as np
from cosmolopy import fidcosmo, magnitudes

#Settings
TFDir = "./"
settingsFile = open('settings','r')
settings = eval(settingsFile.read())
dbDir = settings['dbDir']

vel_ids = db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'lss_velocities')
err = np.zeros((939, 4))

r = db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'gc2_r')[0]

photo_err = db.dbUtils.getFromDB('elmag_r_err', dbDir+'CALIFA.sqlite', 'gc2_errors')
print np.mean(photo_err)

'''
z = db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'ned_z')
dist_mod = magnitudes.distance_modulus(z, **fidcosmo)
R_sdss = db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'kcorrect_sdss')[0]
R = r - dist_mod
err[:, 1] = R
LSS = np.where(califa_id == vel_ids)
z_err = db.dbUtils.getFromDB('vel', dbDir+'CALIFA.sqlite', 'lss_velocities')[0]/(2*300000) #we split errorbar in two
upper_dist_mod = magnitudes.distance_modulus(z+z_err, **fidcosmo)
lower_dist_mod = magnitudes.distance_modulus(z-z_err, **fidcosmo)
R_low = r - lower_dist_mod
R_up = r - upper_dist_mod
err[:, 2] = abs(np.sqrt(((R_low-R)/R)**2 + (photo_err/abs(2*r))**2))

  err[:, 3] = abs(np.sqrt(((R_up-R)/R)**2 + (photo_err/abs(2*r))**2))
  else:
    err[califa_id-1, 2] = abs(R_sdss - R)/(2*R)
    err[califa_id-1, 3] = abs(R_sdss - R)/(2*R)
   

  
  np.savetxt("luminosity_errors_wsdss.csv", err, fmt="%i, %f, %f, %f")
    
    
'''