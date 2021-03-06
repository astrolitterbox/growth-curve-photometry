# -*- coding: utf-8 -*-

import plot_survey as plot
import db 
import utils
import readAtlas
import numpy as np
import matplotlib.pyplot as plt
dbDir = '../db/'


def main():
    #selecting by ids when some of them are missing
    fit_sky_ids = utils.convert(db.dbUtils.getFromDB('califa_id', dbDir+'CALIFA.sqlite', 'u_tot'))[:, 0]    
    ids = ''
    id_length = 0
    for i in fit_sky_ids:
      ids = ids+","+str(int(i))
      id_length+=1
    ids = ids[1:]  
    
    tot_mag = utils.convert(db.dbUtils.getFromDB('u_mag', dbDir+'CALIFA.sqlite', 'u_tot', ' where califa_id in('+ids+')'))  #parsing tuples  
    gc_mag = utils.convert(db.dbUtils.getFromDB('u_mag', dbDir+'CALIFA.sqlite', 'gc', ' where califa_id in('+ids+')'))  #parsing tuples
    #circ_mag = utils.convert(db.dbUtils.getFromDB('circ_r_mag', dbDir+'CALIFA.sqlite', 'gc'))  #parsing tuples    
    nadines_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'nadine', ' where califa_id in('+ids+')'))  #parsing tuples
    sdss_mag = utils.convert(db.dbUtils.getFromDB('petroMag_u', dbDir+'CALIFA.sqlite', 'mothersample', ' where califa_id in('+ids+')'))  #parsing tuples    
    atlas_mag = utils.convert(db.dbUtils.getFromDB('r_mag', dbDir+'CALIFA.sqlite', 'atlas', ' where califa_id in('+ids+')'))

    #gc_hlr = utils.convert(db.dbUtils.getFromDB('circ_hlr', dbDir+'CALIFA.sqlite', 'gc'))
    #nadine_hlr = utils.convert(db.dbUtils.getFromDB('re', dbDir+'CALIFA.sqlite', 'nadine'))
    #sdss_hlr = utils.convert(db.dbUtils.getFromDB('petroR50_r', dbDir+'CALIFA.sqlite', 'mothersample'))  #parsing tuples    
    #lucie_hlr = utils.convert(db.dbUtils.getFromDB('hlr', dbDir+'CALIFA.sqlite', 'lucie'))  #parsing tuples    
    #el_hlr = utils.convert(db.dbUtils.getFromDB('el_hlma', dbDir+'CALIFA.sqlite', 'gc'))

    #lucie_sky = utils.convert(db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'lucie', ' where califa_id in('+ids+')'))  - 1000  #parsing tuples        
    tot_sky = utils.convert(db.dbUtils.getFromDB('gc_sky', dbDir+'CALIFA.sqlite', 'u_tot', ' where califa_id in('+ids+')'))  #parsing tuples 
    gc_sky = utils.convert(db.dbUtils.getFromDB('gc_sky', dbDir+'CALIFA.sqlite', 'gc', ' where califa_id in('+ids+')'))
    sdss_sky = utils.convert(db.dbUtils.getFromDB('sky', dbDir+'CALIFA.sqlite', 'sdss_sky', ' where califa_id in('+ids+')'))
    
    
    
    #plot relations between various magnitude results
    graph = plot.Plots()
    #gc_magData = plot.GraphData(((nadines_mag, tot_mag)), 'k', 'best')
    #graph.plotScatter([gc_magData], "/analysis/new_gc_mag_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's photometry values", "Nadine's gc magnitude, mag", "Updated gc r magnitude, mag"), (11, 16, 11, 16))

    gc_magData = plot.GraphData(((sdss_mag, tot_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/new_gc_mag_vs_sdss_u", plot.PlotTitles("Comparison between my and SDSS photometry values", "SDSS Petrosian u magnitude, mag", "Updated gc r magnitude, mag"),(12, 18, 12, 18))

    #gc_magData = plot.GraphData(((atlas_mag, tot_mag)), 'k', 'best')
    #graph.plotScatter([gc_magData], "/analysis/new_gc_mag_vs_nsatlas", plot.PlotTitles("Comparison between my and NASA Sloan Atlas photometry values", "Updated gc r magnitude, mag", "NSAtlas magnitude, mag"),(11, 16, 11, 16))

    gc_magData = plot.GraphData(((gc_mag, tot_mag)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/gc_vs_gc_new_u", plot.PlotTitles("Comparison between GC and sky-fit GC photometry values", "GC r magnitude, mag", "Updated GC magnitude, mag"),(12, 17, 12, 17))

    #gc_magData = plot.GraphData(((circ_mag, gc_mag)), 'k', 'best')
    #graph.plotScatter([gc_magData], "/analysis/el_mag_vs_circ_apert", plot.PlotTitles("Comparison between elliptical and circular annuli", "r magnitude, mag", "r magnitude, mag"),(11, 16, 11, 16))

    
    #compare sky values
   
    graph = plot.Plots()
    
    #plotData = plot.GraphData(((np.arange(1, 938), gc_sky - lucie_sky)), 'k', 'best')    
    #graph.plotScatter([plotData], "/analysis/sky_comparison", plot.PlotTitles("Comparison between my and Lucie's sky values", "counts", "counts"), (70, 170, -2, 1))
    
    
    
    #print sdss_sky
    
    #print np.reshape((tot_sky - sdss_sky), (id_length, 1)).shape, np.reshape(np.arange(1, id_length+1), (id_length, 1)).shape
    

    plotData = plot.GraphData(((np.arange(1, id_length+1), tot_sky - sdss_sky)), 'k', 'best')    
    graph.plotScatter([plotData], "/analysis/sdss_sky_comparison_u", plot.PlotTitles("Comparison between my and SDSS sky values", "No.", "counts"), (0, id_length, -2, 0.5))

    plotData = plot.GraphData(((np.arange(1, id_length+1), gc_sky - tot_sky)), 'k', 'best')    
    graph.plotScatter([plotData], "/analysis/gc_sky_comparison_u", plot.PlotTitles("GC sky - updated GC sky", "No.", "counts"))


    exit()
    #plot various HLR values

    graph = plot.Plots()
    plotData = plot.GraphData(((lucie_hlr, gc_hlr)), 'k', 'best')
    graph.plotScatter([plotData], "/analysis/hlr_vs_lucie_noscale", plot.PlotTitles("Comparison between my and Lucie's HLR values", "Lucie's $r_e$, arcsec (?)", "gc hlr, arcsec"), (0, 50, 0, 50))   
    
    plotData = plot.GraphData(((nadine_hlr, el_hlr)), 'k', 'best')    
    graph.plotScatter([plotData], "/analysis/el_hlr_vs_nadine", plot.PlotTitles("Comparison between my and Nadine's HLR values", "Nadine's $r_e$, arcsec", "gc hlr, arcsec"), (0, 70, 0, 50))
    
    plotData = plot.GraphData(((sdss_hlr, gc_hlr)), 'k', 'best')    
    graph.plotScatter([plotData], "/analysis/circ_hlr_vs_sdss", plot.PlotTitles("Comparison between my and SDSS HLR values", "SDSS Petrosian $r_50$, arcsec", "gc hlr, arcsec"), (0, 50, 0, 50))
    

    
    #stellar mass, absmag comparison with Jakob's values:
    '''
    absmag_kc = utils.convert(db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'jakobs'))[:937, :]
    absmag_j = utils.convert(db.dbUtils.getFromDB('r', dbDir+'CALIFA.sqlite', 'kcorrect_ned'))[:937, :]

    graph = plot.Plots()
    gc_magData = plot.GraphData(((absmag_kc, absmag_j)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/absolute_magnitudes", plot.PlotTitles("Comparison between my and Jakob's absolute magnitudes", "gc M_r, mag", "JW M_r, mag"))
	

    stmass_kc = utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_ned'))[:937, :]
    stmass_kc_sdss = utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_sdss_phot'))[:937, :]    
    stmass_kc_no_z = utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_no_uz'))[:937, :]        
    stmass_j = utils.convert(db.dbUtils.getFromDB('mstar', dbDir+'CALIFA.sqlite', 'jakobs'))[:937, :]
    stmass_kc = np.log10(stmass_kc)
    stmass_kc_no_z = np.log10(stmass_kc_no_z)
    stmass_kc_sdss = np.log10(stmass_kc_sdss)    
    stmass_j = np.log10(stmass_j)
    
    graph = plot.Plots()
    gc_magData = plot.GraphData(((stmass_kc_sdss, stmass_j)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/stellar masses", plot.PlotTitles("Comparison between kcorrect's and Jakob's stellar masses", "M_{kc}", "M_{JW}"), (7.5, 13, 7.5, 13))

    gc_magData = plot.GraphData(((stmass_kc_sdss, stmass_j)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/stellar_sdss_kc_masses", plot.PlotTitles("Comparison between kcorrect's and Jakob's stellar masses", "M_{kc}", "M_{JW}"), (7.5, 13, 7.5, 13))

    gc_magData = plot.GraphData(((stmass_kc_no_z, stmass_j)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/stMass_jw_gc_no_uz_bands", plot.PlotTitles("Comparison between kcorrect's gri and Jakob's stellar masses", "M_{kc}", "M_{JW}"), (7.5, 13, 7.5, 13))
	
    '''

    '''
	
    #comparison with Starlight:
    starlight_ids = "1,3,4,7,8,10,14,39,42,43,45,53,73,88,100,119,127,133,146,147,151,152,155,156,208,213,273,274,277,306,307,309,319,326,364,387,388,475, 479,486,489,500,515,518,528,548,577,607,609,610,657,663,676,758,764,769,783,797,798,802,806,820,821,823,826,828,829,832,845,847,848,850,851,852,853,854,856,857,858,859,860,863,864,866,867,869,872,873,874,877,878,879,880,881,883,886,887,888,890,896,900,901,902,904,935,938"
    #SELECT k.st_mass, s.starlight_mass FROM kcorrect_ned as k, rosa as s where k.califa_id in(starlight_ids) and s.califa_id in(starlight_ids)
    starlight_masses = utils.convert(db.dbUtils.getFromDB('starlight_mass', dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')'))
    kc_masses = np.log10(utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_ned', ' where califa_id in('+starlight_ids+')')))
    califa_ids = db.dbUtils.getFromDB("califa_id", dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')')
    out = np.hstack((califa_ids, (starlight_masses -  kc_masses)))
    #np.savetxt("mass_outliers.csv", out)
    graph = plot.Plots()
    gc_magData = plot.GraphData(((starlight_masses, kc_masses)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/starlight_masses", plot.PlotTitles("Comparison between kcorrect's and Starlight stellar masses", "M_{\star}", "M_{kc}"), (7.5, 13, 7.5, 13))

    #Starlight comparison with kc_sdss:
    starlight_masses = utils.convert(db.dbUtils.getFromDB('starlight_mass', dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')'))
    kc_masses = np.log10(utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_sdss', ' where califa_id in('+starlight_ids+')')))
    
    
    
    graph = plot.Plots()
    gc_magData = plot.GraphData(((starlight_masses, kc_masses)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/starlight_masses_kc_sdss", plot.PlotTitles("Comparison between kcorrect's and Starlight stellar masses", "M_{\star}", "M_{kc}"), (7.5, 13, 7.5, 13))	
    exit()
    #Starlight comparison with kc_sdss_photometry:
    starlight_ids = "1,3,4,7,8,10,14,39,42,43,45,53,73,88,100,119,127,133,146,147,151,152,155,156,208,213,273,274,277,306,307,309,319,326,364,387,388,475, 479,486,489,500,515,518,528,548,577,607,609,610,657,663,676,758,764,769,783,797,798,802,806,820,821,823,826,828,829,832,845,847,848,850,851,852,853,854,856,857,858,859,860,863,864,866,867,869,872,873,874,877,878,879,880,881,883,886,887,888,890,896,900,901,902,904,935,938"
    #SELECT k.st_mass, s.starlight_mass FROM kcorrect_ned as k, rosa as s where k.califa_id in(starlight_ids) and s.califa_id in(starlight_ids)
    starlight_masses = utils.convert(db.dbUtils.getFromDB('starlight_mass', dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')'))
    kc_masses = np.log10(utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_sdss_phot', ' where califa_id in('+starlight_ids+')')))
    
    graph = plot.Plots()
    gc_magData = plot.GraphData(((starlight_masses, kc_masses)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/starlight_masses_kc_sdss_phot", plot.PlotTitles("Comparison between kcorrect's and Starlight stellar masses", "M_{\star}", "M_{kc}"), (7.5, 13, 7.5, 13))	
    
    #Starlight comparison with kc_sdss_z_replaced:
    starlight_ids = "1,3,4,7,8,10,14,39,42,43,45,53,73,88,100,119,127,133,146,147,151,152,155,156,208,213,273,274,277,306,307,309,319,326,364,387,388,475, 479,486,489,500,515,518,528,548,577,607,609,610,657,663,676,758,764,769,783,797,798,802,806,820,821,823,826,828,829,832,845,847,848,850,851,852,853,854,856,857,858,859,860,863,864,866,867,869,872,873,874,877,878,879,880,881,883,886,887,888,890,896,900,901,902,904,935,938"
    #SELECT k.st_mass, s.starlight_mass FROM kcorrect_ned as k, rosa as s where k.califa_id in(starlight_ids) and s.califa_id in(starlight_ids)
    starlight_masses = utils.convert(db.dbUtils.getFromDB('starlight_mass', dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')'))
    kc_masses = np.log10(utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_z_replaced', ' where califa_id in('+starlight_ids+')')))
    
    graph = plot.Plots()
    gc_magData = plot.GraphData(((starlight_masses, kc_masses)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/starlight_masses_kcorrect_z_replaced", plot.PlotTitles("Comparison between kcorrect's and Starlight stellar masses", "M_{\star}", "M_{kc}"), (7.5, 13, 7.5, 13))	

    #Starlight comparison with kc_sdss_z_replaced:
    starlight_ids = "1,3,4,7,8,10,14,39,42,43,45,53,73,88,100,119,127,133,146,147,151,152,155,156,208,213,273,274,277,306,307,309,319,326,364,387,388,475, 479,486,489,500,515,518,528,548,577,607,609,610,657,663,676,758,764,769,783,797,798,802,806,820,821,823,826,828,829,832,845,847,848,850,851,852,853,854,856,857,858,859,860,863,864,866,867,869,872,873,874,877,878,879,880,881,883,886,887,888,890,896,900,901,902,904,935,938"
    #SELECT k.st_mass, s.starlight_mass FROM kcorrect_ned as k, rosa as s where k.califa_id in(starlight_ids) and s.califa_id in(starlight_ids)
    starlight_masses = utils.convert(db.dbUtils.getFromDB('starlight_mass', dbDir+'CALIFA.sqlite', 'rosa', ' where califa_id in('+starlight_ids+')'))
    kc_masses = np.log10(utils.convert(db.dbUtils.getFromDB('st_mass', dbDir+'CALIFA.sqlite', 'kcorrect_no_uz', ' where califa_id in('+starlight_ids+')')))
    
    graph = plot.Plots()
    gc_magData = plot.GraphData(((starlight_masses, kc_masses)), 'k', 'best')
    graph.plotScatter([gc_magData], "/analysis/starlight_masses_kcorrect_no_z", plot.PlotTitles("Comparison between kcorrect's and Starlight stellar masses from gri", "M_{\star}", "M_{kc}"), (7.5, 13, 7.5, 13))	
    '''

    
    



    #sky comparison
if __name__ == "__main__":
  main()













