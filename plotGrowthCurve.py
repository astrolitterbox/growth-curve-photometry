# -*- coding: utf-8 -*-
import plot_survey as plot
import sys
import numpy as np


def plotGrowthCurve(fluxData, band, CALIFA_ID):
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((0.396*fluxData[:,0], fluxData[:,1])), 'k', 'best')
    currentFluxSkySubPPData = plot.GraphData(((0.396*fluxData[:,0], fluxData[:,2])), 'k', 'best')
    currentFluxData = plot.GraphData(((0.396*fluxData[:,0], fluxData[:,3])), 'b', 'best')
    skySubFluxData = plot.GraphData(((0.396*fluxData[:,0], fluxData[:, 2])), 'b', 'best')
    #NpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 5] - fluxData[:, 4])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], band+'/'+CALIFA_ID+"cumulative_Flux", plot.PlotTitles("CumulativeFlux", "distance", "Flux"))
    graph.plotScatter([currentFluxSkySubPPData], band+'/'+CALIFA_ID+"Flux_per_pixel", plot.PlotTitles("Sky subtracted flux per pixel", "distance", "Flux per pixel"))
    graph.plotScatter([currentFluxData], band+'/'+CALIFA_ID+"Current_flux", plot.PlotTitles("Flux profile", "major axis", "counts"))
    graph.plotScatter([skySubFluxData], band+'/'+CALIFA_ID+"Sky_sub_flux", plot.PlotTitles("Sky subtracted flux", "major axis", "counts"))

