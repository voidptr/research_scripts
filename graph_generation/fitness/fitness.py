############ Fitness Data Plotting ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to common/
import config as cf## some basic shit that I don't want to do myself


cf.addpath( "commongraph/" )
import commongraph as cg


## plot a fitness timeseries
def plot_timeseries( grouping="", subgrouping="" ):

    input_files_glob = "*fitness.timeseries.csv" ## this is actually a globbing pattern
    outfile = "fitness"
    legend = True
    datasources = 1 ## this is weird, but an artifact of plot_from_csv. bar_chart_from_csv is more sane.
    title = "Fitness by Treatment"
    xlabel = "Updates"
    ylabel = "Fitness"
    ploterror = True
    xtickinterval = 50 ## maybe make this saner or configurable at some point, but all my stuff is this right now
    type = "median_only"

    return cg.plot_timeseries( input_files_glob, outfile, 
        grouping=grouping,
        subgrouping=subgrouping,
        legend=legend,
        datasources=datasources,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        ploterror=ploterror,
        xtickinterval=xtickinterval,
        type=type )

def plot_barchart( grouping="", subgrouping="", type="max" ):

    input_files_glob = "*fitness.%s.csv" % type ## this is actually a globbing pattern
    outfile = "fitness"
#    groups = 3 
    title = "Max Fitness by Treatment"
    xlabel = "Treatment"
    ylabel = "Fitness"
    type = type

    return cg.plot_barchart( input_files_glob, outfile, 
        grouping=grouping,
        subgrouping=subgrouping,
#        groups=groups,
        title=title,
        xlabel=xlabel,
        ylabel=ylabel,
        type=type )


