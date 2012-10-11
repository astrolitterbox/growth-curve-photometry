# -*- coding: utf-8 -*-
import numpy as np
import math as math
import matplotlib.pylab as plt
import kcorrect as KC
from kcorrect.sdss import SDSSKCorrect, SDSSPhotoZ, SDSS
from kcorrect.utils.cosmology import ztodm
from scipy import integrate

import matplotlib.cm as cm
import matplotlib.mlab as mlab
import pyfits as pyfits
import utils


#import sami_db
import db as db
import plot_survey as plot
#from sami_new import getDataArray as fullDataArray
#from sami_new import plotScatter as OldSchoolPlot
import matplotlib.font_manager 
import csv
import readAtlas
import collections

c = 299792.458 
pi = 3.14159265
#     Cosmological parameters
H0 = 70.0 #km/s/Mpc, 1 Mpc= 3.08568025*1e19 km
Wm = 0.3
Wl = 0.7
Wh = c / H0 
Wk = 1 - Wm - Wl 
tH = (3.08568025*1e19/H0)/(3600 * 365 * 24*10e9) #Hubble time in Gyr
skyArea = 41252.9612494193 #degrees      
dH = c/H0 #in Mpc
imgDir = 'img/'
dbDir = '../db/'
dbFile = 'CALIFA.sqlite'
dataFile = 'data/Califa.csv'
morphDataFile = 'morph.dat'
observedList = 'list_observed.txt'
db_dataFile = 'db_data.txt'

#constants
H0 = 70.0 #km/s/Mpc, 1 Mpc= 3.08568025*1e19 km
Wl = 0.728
Wm = 1 - Wl
Wh = c / H0 
Wk = 1 - Wm - Wl 
tH = (3.08568025*1e19/H0)/(3600 * 365 * 24*10e9) #Hubble time in Gyr
skyArea = 41252.9612494193 #degrees      
dH = c/H0 #in Mpc


#utilities
def E_z(z): #time derivative of log(a(t)), used for integration
	return 1/(np.sqrt((Wm*(1+z)**3 + Wk*(1+z)**2 + Wl)))

def comovingDistance(z):
	Dc = dH * 1000* integrate.quad(E_z, 0, z)[0] #in kpc
	return Dc

def angular2physical(reff, z): #return physical effective diameter of the galaxy in kpc
    return (math.radians(2*reff/3600) *(comovingDistance(z)) / (1 + z)**2)

def getAbsMag(z, mag, ext):
	print z
	d = comovingDistance(z)
        dm = ztodm(z, (0.3, 0.7, 0.7))
	absmag = mag - dm #- 3.1 * ext
	print dm, 'dm', absmag, 'absmag'
	return absmag
	
def convert(data):
     tempDATA = []
     for i in data:
         tempDATA.append([float(j) for j in i])
     return np.asarray(tempDATA)

def findOverlap(a, b):
   a_multiset = collections.Counter(list(a))
   b_multiset = collections.Counter(list(b))
   return list((a_multiset & b_multiset).elements())
  
def getDataArray(data, zData):
  
  
  myArray = np.empty((939, ))
  
  redshifts = dataArray[:,20]
  maggies = dataArray[:,3:8]
  maggies_err = dataArray[:,8:13]
  extinction = dataArray[:,13:18]
  kc = SDSSKCorrect(redshifts, maggies, maggies_err, extinction, cosmo=(Wm, Wl, H0/100))
  kcorr = kc.kcorrect()
  absmag = kc.absmag()
  dataArray[:,21] = absmag[:, 2]
  dataArray[:,22] = data[:]['petroMag_g'] - data[:]['extinction_g'] - (data[:]['petroMag_r'] - data[:]['extinction_r'])
  sb = data[:]['rho'] + data[:]['petroMag_r']
  dataArray[:,23] = sb
  stMass = np.zeros((len(data), 1))
  size = np.zeros((len(data), 1))
  reff = np.zeros((len(data), 1))
  for i in range(0, len(data)):
    if data[i]['lnLDeV_r'] >= data[i]['lnLExp_r']:
      reff[i] = data[i]['deVRad_r']
    else:
      reff[i] = data[i]['expRad_r']
    size[i] = angular2physical(reff[i], redshifts[i])
    dataArray[i,24] = reff[i]
    dataArray[i,25] = size[i]
  coeffs = kc.coeffs
  tmremain = np.array([[0.601525, 0.941511, 0.607033, 0.523732, 0.763937]])
  ones = np.ones((1, len(redshifts)))
  prod = np.dot(tmremain.T, ones).T 
  modelMasses = coeffs*prod
  #print modelMasses.shape
  mass = np.sum(modelMasses, axis=1)
  for i in range (0, (len(data))):
    distmod = KC.utils.cosmology.ztodm(redshifts[i])
    exp = 10 ** (0.4 * distmod)
    stMass[i] = mass[i] * exp
    dataArray[i,26] = stMass[i]
  return dataArray

def main():
  data = np.empty((939, 16))

  califa_id = utils.convert(db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'gc'))
  
  u = utils.convert(db.dbUtils.getFromDB('u_mag', dbDir+'CALIFA.sqlite', 'gc'))
  g = utils.convert(db.dbUtils.getFromDB('g_mag', dbDir+'CALIFA.sqlite', 'gc'))
  r = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'gc'))
  i = utils.convert(db.dbUtils.getFromDB('i_mag', dbDir+'CALIFA.sqlite', 'gc'))
  z = utils.convert(db.dbUtils.getFromDB('z_mag', dbDir+'CALIFA.sqlite', 'gc'))


  ext_u = utils.convert(db.dbUtils.getFromDB('extinction_u', dbDir+'CALIFA.sqlite', 'extinction'))
  ext_g = utils.convert(db.dbUtils.getFromDB('extinction_g', dbDir+'CALIFA.sqlite', 'extinction'))
  ext_r = utils.convert(db.dbUtils.getFromDB('extinction_r', dbDir+'CALIFA.sqlite', 'extinction'))
  ext_i = utils.convert(db.dbUtils.getFromDB('extinction_i', dbDir+'CALIFA.sqlite', 'extinction'))
  ext_z = utils.convert(db.dbUtils.getFromDB('extinction_z', dbDir+'CALIFA.sqlite', 'extinction'))
  
  err_u = utils.convert(db.dbUtils.getFromDB('petroMagErr_u', dbDir+'CALIFA.sqlite', 'extinction'))
  err_g = utils.convert(db.dbUtils.getFromDB('petroMagErr_g', dbDir+'CALIFA.sqlite', 'extinction'))
  err_r = utils.convert(db.dbUtils.getFromDB('petroMagErr_r', dbDir+'CALIFA.sqlite', 'extinction'))
  err_i = utils.convert(db.dbUtils.getFromDB('petroMagErr_i', dbDir+'CALIFA.sqlite', 'extinction'))
  err_z = utils.convert(db.dbUtils.getFromDB('petroMagErr_z', dbDir+'CALIFA.sqlite', 'extinction'))  
  
  redshift = utils.convert(db.dbUtils.getFromDB('z', dbDir+'CALIFA.sqlite', 'hl_z'))  
  
  data[:, 0] = u[:, 0]
  data[:, 1] = g[:, 0]
  data[:, 2] = r[:, 0]
  data[:, 3] = i[:, 0]
  data[:, 4] = z[:, 0]
  
  data[:, 5] = ext_u[:, 0]
  data[:, 6] = ext_g[:, 0]
  data[:, 7] = ext_r[:, 0]
  data[:, 8] = ext_i[:, 0]
  data[:, 9] = ext_z[:, 0]
  
  data[:, 10] = err_u[:, 0]
  data[:, 11] = err_g[:, 0]
  data[:, 12] = err_r[:, 0]
  data[:, 13] = err_i[:, 0]
  data[:, 14] = err_z[:, 0]
  
  data[:, 15] = redshift[:, 0]
  
  maggies = data[:, 0:5]

  extinction = data[:, 5:10]

  maggies_err = data[:, 11:]  

  
  
  
  outputArray = np.empty((939, 7))
  
  kc = SDSSKCorrect(redshift, maggies, maggies_err, extinction, cosmo=(Wm, Wl, H0/100))
  kcorr = kc.kcorrect()
  #absmag = getAbsMag(redshift, maggies[:, 2], extinction[:, 2])#kc.absmag() 
  outputArray[:,0] = califa_id[:, 0]
  print outputArray[:, 1:6].shape
  
  outputArray[:, 1:6] = kc.absmag()  
  coeffs = kc.coeffs
  tmremain = np.array([[0.601525, 0.941511, 0.607033, 0.523732, 0.763937]])
  ones = np.ones((1, len(redshift)))
  prod = np.dot(tmremain.T, ones).T 
  modelMasses = coeffs*prod
  #print modelMasses.shape
  mass = np.sum(modelMasses, axis=1)
  for i in range (0, (len(data))):
    distmod = KC.utils.cosmology.ztodm(redshift[i])
    exp = 10 ** (0.4 * distmod)
    outputArray[i, 6] = mass[i] * exp

  
  np.savetxt("absmag.csv", outputArray, fmt = '%i, %10.3f, %10.3f, %10.3f, %10.3f, %10.3f, %10.3e')  
  
if __name__ == '__main__':
    main()




