import numpy as np
import csv
import sys
import utils
import string

band = sys.argv[1]
data = np.genfromtxt(band+'ellipse.csv', delimiter = ',')
newData = np.genfromtxt(band+'_ellipse_log69.csv', delimiter = ',')
for i in range(0, newData.shape[0]):
	lineNr = int(newData[i, 0]) - 1
	print lineNr
	data[lineNr, :] = newData[i, :]
np.savetxt("new_"+band+"ellipse.csv", data, fmt = '%i, %10.5f, %10.5f, %10.5f, %10.5f')


