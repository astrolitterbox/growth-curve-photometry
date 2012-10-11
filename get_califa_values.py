# -*- coding: utf-8 -*-
import numpy as np
import db
import utils
dbDir = '../db/'

data = np.empty((939, 3), dtype = object)


#califa_id = utils.convert(db.dbUtils.getFromDB('CALIFA_ID', dbDir+'CALIFA.sqlite', 'gc_r'))
ra = utils.convert(db.dbUtils.getFromDB('ra', dbDir+'CALIFA.sqlite', 'mothersample'))
dec = utils.convert(db.dbUtils.getFromDB('dec', dbDir+'CALIFA.sqlite', 'mothersample'))

print ra.shape
for i in range(0, 939):


  data[i, 0] = str(ra[i, 0])+'d'
  data[i, 1] = str(dec[i, 0])+'d'
  data[i, 2] = 0.05
  print i, data[i]
  utils.writeOut(data[i, 0:3], "ned_query_coords.csv", ";")

#np.savetxt("ned_query_coords.csv", data, delimiter = ';')

