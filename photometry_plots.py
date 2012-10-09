# -*- coding: utf-8 -*-

import plot_survey as plot
import db 
import utils
import readAtlas
import numpy as np
import matplotlib.pyplot as plt
dbDir = '../db/'


def main():

  
    gc_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'gc'))[:937, :]  #parsing tuples
    circ_mag = utils.convert(db.dbUtils.getFromDB('circ_r_mag', dbDir+'CALIFA.sqlite', 'gc'))[:937, :]  #parsing tuples    
    nadines_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'nadine'))[:937, :]  #parsing tuples
    sdss_mag = utils.convert(db.dbUtils.getFromDB('petroMag_r', dbDir+'CALIFA.sqlite', 'mothersample'))[:937, :]  #parsing tuples    
    atlas_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'atlas'))[:937, :]  

    gc_hlr = utils.convert(db.dbUtils.getFromDB('circ_hlr', dbDir+'CALIFA.sqlite', 'gc'))[:937, :]
    nadine_hlr = utils.convert(db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'nadine'))[:937, :]
    sdss_hlr = utils.convert(db.dbUtils.getFromDB('petroR50_r', dbDir+'CALIFA.sqlite', 'mothersample'))[:937, :]  #parsing tuples    
    lucie_hlr = utils.convert(db.dbUtils.getFromDB('hlr', dbDir+'CALIFA.sqlite', 'lucie'))[:937, :]  #parsing tuples    
    el_hlr = utils.convert(db.dbUtils.getFromDB('el_hlma', dbDir+'CALIFA.sqlite', 'gc'))[:937, :]

    #lucie_sky = utils.convert(db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'lucie'))[:937, :]  - 1000  #parsing tuples        
    gc_sky = utils.convert(db.dbUtils.getFromDB('gc_sky', dbDir+'CALIFA.sqlite', 'gc'))[:937, :]
    sdss_sky = utils.convert(db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sdss_sky'))[:937, :]
    #plot relations between various magnitude results
    graph = plot.Plots()
    gc_magData = plot.GraphData(((nadines_mag, gc_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "gc_mag_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's photometry values", "gc r magnitude, mag", "Nadine's gc magnitude, mag"), (11, 16, 11, 16))

    gc_magData = plot.GraphData(((sdss_mag, gc_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "gc_mag_vs_sdss", plot.PlotTitles("Comparison between my and SDSS photometry values", "gc r magnitude, mag", "SDSS Petrosian r magnitude, mag"),(11, 16, 11, 16))

    gc_magData = plot.GraphData(((atlas_mag, gc_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "gc_mag_vs_nsatlas", plot.PlotTitles("Comparison between my and NASA Sloan Atlas photometry values", "gc r magnitude, mag", "NSAtlas magnitude, mag"),(11, 16, 11, 16))

    gc_magData = plot.GraphData(((atlas_mag, sdss_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "sdss_mag_vs_nsatlas", plot.PlotTitles("Comparison between SDSS and NASA Sloan Atlas photometry values", "SDSS Petrosian r magnitude, mag", "NSAtlas magnitude, mag"),(11, 16, 11, 16))

    gc_magData = plot.GraphData(((circ_mag, gc_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "el_mag_vs_circ_apert", plot.PlotTitles("Comparison between elliptical and circular annuli", "r magnitude, mag", "r magnitude, mag"),(11, 16, 11, 16))



    #plot various HLR values

    graph = plot.Plots()
    plotData = plot.GraphData(((lucie_hlr, gc_hlr)), 'k', 'best')
    graph.plotScatter([plotData], "hlr_vs_lucie_noscale", plot.PlotTitles("Comparison between my and Lucie's HLR values", "Lucie's $r_e$, arcsec (?)", "gc hlr, arcsec"), (0, 50, 0, 50))   
    
    plotData = plot.GraphData(((nadine_hlr, el_hlr)), 'k', 'best')    
    graph.plotScatter([plotData], "el_hlr_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's HLR values", "Nadine's $r_e$, arcsec", "gc hlr, arcsec"), (0, 70, 0, 50))
    
    plotData = plot.GraphData(((sdss_hlr, gc_hlr)), 'k', 'best')    
    graph.plotScatter([plotData], "circ_hlr_vs_sdss", plot.PlotTitles("Comparison between my and SDSS HLR values", "SDSS Petrosian $r_50$, arcsec", "gc hlr, arcsec"), (0, 50, 0, 50))
    
    
    #compare sky values
   
    graph = plot.Plots()
    
    #plotData = plot.GraphData(((np.arange(1, 938), gc_sky - lucie_sky)), 'k', 'best')    
    graph.plotScatter([plotData], "sky_comparison", plot.PlotTitles("Comparison between my and Lucie's sky values", "counts", "counts"), (70, 170, -2, 1))
    
    plotData = plot.GraphData(((np.arange(1, 938), gc_sky - sdss_sky)), 'k', 'best')    
    graph.plotScatter([plotData], "sdss_sky_comparison", plot.PlotTitles("Comparison between my and SDSS sky values", "counts", "counts"), (70, 170, -1, 1))






    
    



    #sky comparison
if __name__ == "__main__":
  main()













