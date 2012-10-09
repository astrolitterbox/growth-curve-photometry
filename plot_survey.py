# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:18:52 2012

@author: astrolitterbox
"""
import numpy as np
#import db
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 19:18:52 2012

@author: astrolitterbox
"""
import numpy as np
#import db

import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager
import numpy as np



x1,x2,n,m,b = 0.,300.,1000,1.,0.
x = np.r_[x1:x2:n*1j]  


class PlotTitles:
    def __init__(self, title, xlabel, ylabel):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel


class GraphData:
    def __init__(self, data, colour, legend):
        self.data = data
        self.colour = colour
        self.legend = legend

class Plots:
    imgDir = './img/analysis'        
    def plotLogHist(self, graphDataList, filename, plotTitles, bins, *args):
      bins=10**np.arange(*bins)     
      s = plt.figure()
      ax = s.add_subplot(111)      
      try:
        args[0]
      except IndexError:
          print 'blah'
      else:  
          v = list(args[0])
          ax.axis(v)
      prop = matplotlib.font_manager.FontProperties(size=8)     
      for gd in graphDataList:
          p1 = plt.hist((gd.data), color=gd.colour, bins = bins, histtype='barstacked', alpha=0.75)    
          print gd.legend            
          #plt.legend([p1], list(gd.legend), loc=0, markerscale=10, fancybox=True, labelspacing = 0.2, prop=prop, shadow=True)
      plt.title(plotTitles.title)
      plt.xlabel = plotTitles.xlabel
      plt.xscale('log')
      plt.ylabel = plotTitles.ylabel
      plt.savefig(self.imgDir+filename)

    def plotHist(self, graphDataList, filename, plotTitles, bins, *args):
      s = plt.figure()
      ax = s.add_subplot(111)
      try:
        args[0]
      except IndexError:
          print 'blah'
      else:  
          v = list(args[0])
          ax.axis(v)
      prop = matplotlib.font_manager.FontProperties(size=8)     
      for gd in graphDataList:
          p1 = plt.hist((gd.data), color=gd.colour, bins = bins, histtype='barstacked', alpha=0.75)    
          print gd.legend            
          #plt.legend([p1], list(gd.legend), loc=0, markerscale=10, fancybox=True, labelspacing = 0.2, prop=prop, shadow=True)
      plt.title(plotTitles.title)
      plt.xlabel = plotTitles.xlabel
      plt.ylabel = plotTitles.ylabel
      plt.savefig(self.imgDir+filename)
    
    def plotScatter(self, graphDataList, filename, plotTitles, *args):

      s = plt.figure()
      ax = s.add_subplot(111)
      try:
        args[0]
      except IndexError:
          print 'no axis settings!'
      else:  
          v = list(args[0])
          ax.axis(v)

      prop = matplotlib.font_manager.FontProperties(size=8)     
      for gd in graphDataList:
          p1 = ax.plot(gd.data[0], gd.data[1], '.', markersize=2, color=gd.colour, mec=gd.colour, alpha = 0.9) 
          #plt.legend([p1[0]], gd.legend,  loc=0, markerscale=1, fancybox=True, labelspacing = 0.2, prop=prop, shadow=True)
      #plt.plot(x, m*x + b, color='r', alpha = 0.6)
      plt.title(plotTitles.title)
      plt.xlabel(plotTitles.xlabel)
      plt.ylabel(plotTitles.ylabel)
      
      plt.savefig(self.imgDir+'/'+filename)
