# -*- coding: utf-8 -*-
import numpy as np
import db
import utils
dbDir = '../db/'

data = np.empty((939, 14), dtype = float)


califa_id = utils.convert(db.dbUtils.getFromDB('CALIFA_ID', dbDir+'CALIFA.sqlite', 'gc_r'))
el_u = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc_u')) - 0.04 #AB correction
el_g = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc_g'))
el_r = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc_r'))
el_i = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc_i'))
el_z = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc_z'))

el_hlr = 0.396*utils.convert(db.dbUtils.getFromDB('el_hlma', dbDir+'CALIFA.sqlite', 'gc_r')) #SDSS pixel scale
print el_hlr

circ_mag = utils.convert(db.dbUtils.getFromDB('circ_mag', dbDir+'CALIFA.sqlite', 'gc_r'))
circ_hlr = 0.396*utils.convert(db.dbUtils.getFromDB('circ_hlr', dbDir+'CALIFA.sqlite', 'gc_r'))
r_sky = utils.convert(db.dbUtils.getFromDB('gc_sky', dbDir+'CALIFA.sqlite', 'gc_r'))

pa = utils.convert(db.dbUtils.getFromDB('PA', dbDir+'CALIFA.sqlite', 'angles'))
pa_align = utils.convert(db.dbUtils.getFromDB('PA_align', dbDir+'CALIFA.sqlite', 'angles'))
ba = utils.convert(db.dbUtils.getFromDB('ba', dbDir+'CALIFA.sqlite', 'nadine'))

flags = utils.convert(db.dbUtils.getFromDB('sum', dbDir+'CALIFA.sqlite', 'gc_flags'))

print data[:, 0].shape, califa_id.shape


data[:, 0] = califa_id[:, 0]
data[:, 1] = el_u[:, 0]
data[:, 2] = el_g[:, 0]
data[:, 3] = el_r[:, 0]
data[:, 4] = el_i[:, 0]
data[:, 5] = el_z[:, 0]
data[:, 6] = el_hlr[:, 0]
data[:, 7] = circ_mag[:, 0]
data[:, 8] = circ_hlr[:, 0]
data[:, 9] = r_sky[:, 0]
data[:, 10] = pa[:, 0]
data[:, 11] = pa_align[:, 0]
data[:, 12] = ba[:, 0]
data[:, 13] = flags[:, 0]
np.savetxt("growth_curve_analysis.csv", data, fmt = '%i, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %10.5f, %i', delimiter = ',')

