import numpy as np
import csv
import sys
import utils
import string

band = sys.argv[1]
data = np.genfromtxt('iellipse.csv', delimiter = ',')
newData = np.genfromtxt('i_ellipse_r.csv', delimiter = ',')
for i in range(0, newData.shape[0]):
	lineNr = int(newData[i, 0]) - 1
	print lineNr
	data[lineNr, :] = newData[i, :]
np.savetxt("iellipseNew.csv", data, fmt = '%i, %10.5f, %10.5f, %10.5f, %10.5f')


