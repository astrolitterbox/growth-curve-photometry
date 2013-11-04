#setting up CALIFA colourmap:
import matplotlib.pyplot as plt
from matplotlib import colors
import numpy as np

def make_colourmap(ind, red, green, blue, name):
	newInd = range(0, 256)
	r = np.interp(newInd, ind, red, left=None, right=None)
	g = np.interp(newInd, ind, green, left=None, right=None)
	b = np.interp(newInd, ind, blue, left=None, right=None)
	colours = np.transpose(np.asarray((r, g, b)))
	fctab= colours/255.0
	cmap = colors.ListedColormap(fctab, name=name,N=None) 
	return cmap

def get_califa_velocity_cmap():
	ind = [0.,  1., 35., 90.,125.,160.,220.,255.]
	red = [  0.,148.,  0.,  0., 55.,221.,255.,255.]
	green = [  0.,  0.,  0.,191., 55.,160.,  0.,165.]
	blue = [  0.,211.,128.,255., 55.,221.,  0.,  0.]
	return make_colourmap(ind, red, green, blue, 'califa_vel')
	
def get_califa_intensity_cmap():
	ind = [  0.,  1., 50.,100.,150.,200.,255.]
	red = [  0.,  0.,  0.,255.,255., 55.,221.]
	green =	[  0.,  0.,191.,  0.,165., 55.,160.]
	blue = [  0.,128.,255.,  0.,  0., 55.,221.]
	return make_colourmap(ind, red, green, blue, 'califa_int')		
	
califa_vel = get_califa_velocity_cmap()	
califa_int = get_califa_intensity_cmap()	
