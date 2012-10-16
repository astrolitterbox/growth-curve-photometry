import numpy as np
import os

ids = np.genfromtxt("high_re_ids.csv", dtype = int)
zipfile = "high_re"
for x, id in enumerate(ids):
	#os.system("zip -j "+zipfile+ " growth_curves/r/gc_profile"+str(id)+".csv")
	os.system("zip -j "+zipfile+ " img/plots/"+str(id)+"cumulative_Flux.png")
