# -*- coding: utf-8 -*-

import plot_survey as plot
import db 
import utils

dbDir = '../db/'


def main():
  
    gc_mag = utils.convert(db.dbUtils.getFromDB('el_mag', dbDir+'CALIFA.sqlite', 'gc'))  #parsing tuples    
    nadines_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'nadine'))[77:161]  #parsing tuples
    sdss_mag = utils.convert(db.dbUtils.getFromDB('petroMag_r', dbDir+'CALIFA.sqlite', 'mothersample'))[77:161]  #parsing tuples    
    
    #plot relations between various magnitude results
    graph = plot.Plots()
    gc_magData = plot.GraphData(((gc_mag, nadines_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "gc_mag_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's photometry values", "gc r magnitude, mag", "Nadine's gc magnitude, mag"))

    gc_magData = plot.GraphData(((gc_mag, sdss_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "gc_mag_vs_sdss", plot.PlotTitles("Comparison between my and sdss photometry values", "gc r magnitude, mag", "Nadine's gc magnitude, mag"))


    #plot various HLR values
    gc_hlr = utils.convert(db.dbUtils.getFromDB('circ_hlr', dbDir+'CALIFA.sqlite', 'gc'))
    nadine_hlr = utils.convert(db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'nadine'))[77:161]
    sdss_hlr = utils.convert(db.dbUtils.getFromDB('petroR50_r', dbDir+'CALIFA.sqlite', 'mothersample'))[77:161]  #parsing tuples    
    lucie_hlr = utils.convert(db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'lucie'))[77:161]  #parsing tuples    
    el_hlr = utils.convert(db.dbUtils.getFromDB('el_hlr', dbDir+'CALIFA.sqlite', 'gc'))

    graph = plot.Plots()
    plotData = plot.GraphData(((gc_hlr, lucie_hlr)), 'k', 'best')
    graph.plotScatter([plotData], "hlr_vs_lucie", plot.PlotTitles("Comparison between my and Lucie's HLR values", "gc r magnitude, mag", "Nadine's gc magnitude, mag"))
    
    graph = plot.Plots()
    plotData = plot.GraphData(((el_hlr, nadine_hlr)), 'k', 'best')
    graph.plotScatter([plotData], "el_hlr_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's HLR values", "gc r magnitude, mag", "Nadine's gc magnitude, mag"))


if __name__ == "__main__":
  main()













