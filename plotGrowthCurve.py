# -*- coding: utf-8 -*-
import plot_survey as plot


def plotGrowthCurve(fluxData):
    graph = plot.Plots()
    cumulativeFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,1])), 'r', 'best')
    currentFluxSkySubPPData = plot.GraphData(((fluxData[:,0], fluxData[:,2])), 'b', 'best')
    #currentFluxData = plot.GraphData(((fluxData[:,0], fluxData[:,3])), 'b', 'best')
    #TheoreticalNpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 4])), 'b', 'best')
    #NpixData = plot.GraphData(((fluxData[:,0], fluxData[:, 5] - fluxData[:, 4])), 'b', 'best')
    graph.plotScatter([cumulativeFluxData], "Sky subtracted cumulative Flux", plot.PlotTitles("Sky subtracted cumulativeFlux", "distance", "Flux"))
    graph.plotScatter([currentFluxSkySubPPData], "Sky subtracted cumulative flux per pixel", plot.PlotTitles("cumulative_flux_skysub_per_pixel", "distance", "Flux per pixel"))
    #graph.plotScatter([TheoreticalNpixData], "Mathematical ellipse length", plot.PlotTitles("ellipse length", "distance", "circumference"))
    #graph.plotScatter([NpixData], "Pixel ellipse length", plot.PlotTitles("ellipse length", "distance", "circumference"))

