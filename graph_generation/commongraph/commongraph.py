############ Run File Data Extraction and Aggregation ###########

import glob
import os
import sys

sys.path.append("../../common/") ## to analysis/
import config as cf## some basic shit that I don't want to do myself

#cf.addpath( "integrity_testing/" )
#import integrity_testing as it


plot_from_csv_path = cf.getpath("graph_generation/plot_from_csv.py")
bar_chart_from_csv_path = cf.getpath("graph_generation/bar_chart_from_csv.py")

def plot_timeseries( infiles_glob, outfile, 
    grouping="", 
    subgrouping="", 
    legend=False,
    datasources=None,
    title="",
    xlabel="",
    ylabel="",
    ploterror=False,
    xtickinterval=None,
    type="median_only" ):

    ## manage the inputs
    
    if grouping:
        if title: ## this is gross
            title = "%s - %s" % (title, grouping)
        grouping = "%s_" % grouping
        
    if subgrouping:
        if title: ## this is gross
            title = "%s - %s" % (title, subgrouping)
        subgrouping = "%s__" % subgrouping

    if legend:
        legend = "--legend "
    if datasources:
        datasources = "--data_sources %s " % datasources
    if title:
        title = "--title \"%s\" " % title
    if xlabel:
        xlabel = "-x \"%s\" " % xlabel
    if ylabel:
        ylabel = "-y \"%s\" " % ylabel
    errorname = ""
    if ploterror:
        ploterror = "--calculate_error "
        errorname = ".error"
    if xtickinterval:
        xtickinterval = "--x_tick_intervals %s " % xtickinterval
    if type == "median_only":
        type = "-o "

    cwd = cf.Config.Script.cwd

    print infiles_glob
    infiles = glob.glob( infiles_glob )

    if len(infiles) == 0:
        print "Required input files are missing: %s" % infiles_glob
        return False

    outfile = os.path.join( cwd, "%s%s%s.timeseries.plot%s.png" % ( grouping, subgrouping, outfile, errorname ) )
    infile = " ".join(infiles)

    cmd = "python " + plot_from_csv_path + " " + type + datasources + legend + ploterror + title + ylabel + xlabel + xtickinterval + outfile + " " + infile 
    print cmd
    os.popen( cmd )

    return True

def plot_barchart( infiles_glob, outfile, 
    grouping="", 
    subgrouping="", 
    groups=None,
    title="",
    xlabel="",
    ylabel="",
    type="max" ):

    ## manage the inputs
    title_opt = ""
    if title:
        title_text = title
        if grouping:
            title_text += " - %s" % grouping
        if subgrouping:
            title_text += " - %s" % subgrouping

        title_opt = "--title \"%s\" " % title_text

    grouping_opt = ""
    if grouping:
        grouping_opt = "%s_" % grouping
       
    subgrouping_opt = ""
    if subgrouping:
        subgrouping_opt = "%s__" % subgrouping

    groups_opt = ""
    if groups:
        groups_opt = "--groups %s " % groups

    xlabel_opt = ""
    if xlabel:
        xlabel_opt = "-x \"%s\" " % xlabel
    ylabel_opt = ""
    if ylabel:
        ylabel_opt = "-y \"%s\" " % ylabel

    cwd = cf.Config.Script.cwd

    infiles = glob.glob( infiles_glob )

    if len(infiles) == 0:
        print "Required input files are missing: %s" % infiles_glob
        return False

    outfile = os.path.join( cwd, "%s%s%s.%s.barchart.png" % ( grouping_opt, subgrouping_opt, outfile, type ) )
    infile = " ".join(infiles)

    cmd = "python " + bar_chart_from_csv_path + " " + groups_opt + title_opt + ylabel_opt + xlabel_opt + outfile + " " + infile 
    print cmd
    os.popen( cmd )

    return True


