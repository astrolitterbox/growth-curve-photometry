import matplotlib 
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

edgeDist = np.genfromtxt('closest_edge.csv', delimiter=",")[:, 1]
r50 = np.genfromtxt('magsr.csv', delimiter=",")[:, 3] 
print r50.shape, edgeDist.shape, r50, np.min(r50), np.max(r50)

fig = plt.figure()
ax = fig.add_subplot(121)
ax.hist(edgeDist/r50, bins=50)
plt.title("D/r50")
ax = fig.add_subplot(122)
ax.hist(edgeDist*0.396, bins=50)
plt.title("D, arcsec")


fig = plt.figure()
ax = fig.add_subplot(121)
ax.hist(edgeDist/r50, bins=50)
plt.title("D/r50")
ax = fig.add_subplot(122)
ax.hist(edgeDist*0.396, bins=50)
plt.title("D, arcsec"
plt.savefig('img/rtest')


plt.savefig('img/edgeDistances')






