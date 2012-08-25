# -*- coding: utf-8 -*-
import plot_survey as plot


def plotGrowthCurve(fluxData, CALIFA_ID):
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'k', 'best')
    currentFluxSkySubPPData = plot.GraphData(((fluxData[:,0], fluxData[:,2])), 'k', 'best')
    #currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,3])), 'b', 'best')
    #TheoreticalNpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 4])), 'b', 'best')
    #NpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 5] - fluxData[:, 4])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], CALIFA_ID+"cumulative_Flux", plot.PlotTitles("Sky subtracted cumulativeFlux", "distance", "Flux"))
    graph.plotScatter([currentFluxSkySubPPData], CALIFA_ID+"Flux_per_pixel", plot.PlotTitles("Sky subtracted flux per pixel", "distance", "Flux per pixel"))
    #graph.plotScatter([TheoreticalNpixData], "Mathematical ellipse length", plot.PlotTitles("ellipse length", "distance", "circumference"))
    #graph.plotScatter([NpixData], "Pixel ellipse length", plot.PlotTitles("ellipse length", "distance", "circumference"))

