# -*- coding: utf-8 -*-
import numpy as np
#import set
import utils
data = np.zeros((939, 6), dtype = int)
data[:, 0] = np.arange(1, 940, dtype = int)


#flag: 1 denotes visually wrong PA:

indices = [10, 43, 104, 146, 156, 176, 194, 251, 265, 272, 302, 342, 418, 429, 431, 448, 525, 533, 566, 577, 638, 659, 721, 787, 878, 902, 938, 939]
for i, x in enumerate(indices):
	indices[i] = x - 1
data[indices, 1] = 1

#flag: 2 denotes off-center galaxies:
center = [246, 428, 679]
data[center, 2] = 2
print data[center].shape, data.shape

#flag: 4 marks galaxies that are closer to the edge of the frame than 2 HLSMA (in r band):
#select g.califa_id, (0.396*c.closest_edge)/g.elhlr from gc2_r as g, closest_edge as c where (c.closest_edge)/g.elhlr < 2 and g.califa_id = c.califa_id
indices = [126, 244, 258, 260, 273, 304, 417, 434, 545, 696, 741, 763, 809, 841, 880] 
for i, x in enumerate(indices):
	indices[i] = x - 1
data[indices, 3] = 4

#flag: 8 denotes galaxies that have suspicious/unreliable measurements (heavily masked)

indices = [10, 22, 46, 53, 63, 86, 135, 154, 156, 161, 162, 175, 185, 223, 233, 245, 248, 255, 266, 267, 271, 355, 390, 426, 444, 457, 460, 491, 541, 577, 592, 617, 670, 680, 684, 699, 710, 714, 781, 784, 785, 801, 806, 819, 824, 827, 852, 858, 870, 874, 880, 881, 882, 883, 888, 893, 897, 908, 911, 924, 928, 932, 938, 939]
for i, x in enumerate(indices):
	indices[i] = x - 1
data[indices, 4] = 8


for i in range(0, 939):
	data[i, 5]  = np.sum(data[i, 1:5])
	out = data[i, :]
	print 'did you delete the file?'
	utils.writeOut(out, 'gc2_flags.txt')		
