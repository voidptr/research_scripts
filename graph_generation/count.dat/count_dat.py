############ Count.dat Data Plotting ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to common/
import config as cf## some basic shit that I don't want to do myself


cf.addpath( "commongraph/" )
import commongraph as cg


## plot a fitness timeseries
def plot_genotype_count_timeseries( grouping="", subgrouping="" ):

    input_files_glob = "*genotype_count.timeseries.csv" ## this is actually a globbing pattern
    outfile = "genotype_count"
    legend = True
    datasources = 1 ## this is weird, but an artifact of plot_from_csv. bar_chart_from_csv is more sane.
    title = "Genotype Count by Treatment"
    xlabel = "Updates"
    ylabel = "Genotype Count"
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


