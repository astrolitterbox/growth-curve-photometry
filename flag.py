# -*- coding: utf-8 -*-
import numpy as np
#import set
import utils
data = np.empty((939, 7), dtype = int)
data[:, 0] = np.arange(1, 940, dtype = int)

u_sens = np.genfromtxt("u_wrong_skies.csv", delimiter = ",", dtype = int)[:, 0]
g_sens = np.genfromtxt("g_wrong_skies.csv", delimiter = ",", dtype = int)[:, 0]
r_sens = np.genfromtxt("r_wrong_skies.csv", delimiter = ",", dtype = int)[:, 0]
i_sens = np.genfromtxt("i_wrong_skies.csv", delimiter = ",", dtype = int)[:, 0]
z_sens = np.genfromtxt("z_wrong_skies.csv", delimiter = ",", dtype = int)[:, 0]


susp_z = np.genfromtxt("susp_z.csv", dtype = int, delimiter = "\n")
susp_u = np.genfromtxt("susp_u.csv", dtype = int, delimiter = "\n")

for x, i in enumerate(susp_z):
	susp_z[x] = i + 1

for x, i in enumerate(susp_u):
        susp_u[x] = i + 1



#flag: 8 means more sensitive limiting slope value C = 0.00005*\sigma_{sky} (counts/pixel) was applieda

indices = set(list(u_sens) + list(g_sens) + list(r_sens)+ list(i_sens)+list(z_sens)+list(susp_u)+list(susp_z))
indices =  list(indices)

indices.sort()
print indices

#flag: 1 denotes visually wrong PA:

pa = np.genfromtxt("wrong_pas.txt", dtype = int)
print pa
pa = pa - 1
print pa
data[pa, 1] = 1

#flag: 2 denotes off-center galaxies:
#centers
#subtracted indices already!
center = [246, 428, 679]

data[center, 2] = 2

#flag: 4 denotes lower sensitivity limit galaxies with C = 0.00005:
for x, i in enumerate(indices):
	indices[x] = i - 1

print indices, 'indices'

data[indices, 3] = 4
print data[indices, 3]


#flag: 8 denotes less sensitive galaxies with C = 0.0005:


data[880, 4] = 8


#flag: 16
#visually suspicious galaxies with subtracted indices:
vis = [136, 416, 544,937, 801, 914]
data[vis, 5] = 16

for i in range(0, 939):
	data[i, 6]  = np.sum(data[i, 1:])
	out = data[i, :]
	print 'did you delete the file?'
	utils.writeOut(out, 'flags.txt')		
