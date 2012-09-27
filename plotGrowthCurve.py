# -*- coding: utf-8 -*-
import plot_survey as plot


def plotGrowthCurve(fluxData, CALIFA_ID):
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'k', 'best')
    currentFluxSkySubPPData = plot.GraphData(((fluxData[:,0], fluxData[:,2])), 'k', 'best')
    currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,4])), 'b', 'best')
    skySubFluxData = plot.GraphData(((fluxData[:,0], fluxData[:, 6])), 'b', 'best')
    #NpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 5] - fluxData[:, 4])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], CALIFA_ID+"cumulative_Flux", plot.PlotTitles("Sky subtracted cumulativeFlux", "distance", "Flux"))
    graph.plotScatter([currentFluxSkySubPPData], CALIFA_ID+"Flux_per_pixel", plot.PlotTitles("Sky subtracted flux per pixel", "distance", "Flux per pixel"))
    graph.plotScatter([currentFluxData], CALIFA_ID+"Current_flux", plot.PlotTitles("Flux profile", "major axis", "counts"))
    graph.plotScatter([skySubFluxData], CALIFA_ID+"Sky_sub_flux", plot.PlotTitles("Sky subtracted flux", "major axis", "counts"))

