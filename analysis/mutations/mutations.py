############ Mutation Data Extraction and Aggregation ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to analysis/
import config as cf## some basic shit that I don't want to do myself

cf.addpath( "run_file_aggregation/" )
import run_file_aggregation as rf

## aggregate the contents of the tasks.dat file
def aggregate_coding_mutations_timeseries( directories, grouping="", subgrouping="", verbose=False, test=False, expected=None ):

    input_files_glob = ["mutation_metrics.csv*"] ## this is actually a globbing pattern
    column = 1
    outfile = "coding_mutations"

    return rf.aggregate_timeseries( directories, input_files_glob, outfile, column, grouping=grouping, subgrouping=subgrouping, verbose=verbose, separator=",", header=True, test=test, expected=expected )

def aggregate_degenerate_mutations_timeseries( directories, grouping="", subgrouping="", verbose=False, test=False, expected=None ):

    input_files_glob = ["mutation_metrics.csv*"] ## this is actually a globbing pattern
    column = 3
    outfile = "degenerate_mutations"

    return rf.aggregate_timeseries( directories, input_files_glob, outfile, column, grouping=grouping, subgrouping=subgrouping, verbose=verbose, separator=",", header=True, test=test, expected=expected )

def aggregate_noncoding_mutations_timeseries( directories, grouping="", subgrouping="", verbose=False, test=False, expected=None ):

    input_files_glob = ["mutation_metrics.csv*"] ## this is actually a globbing pattern
    column = 2
    outfile = "noncoding_mutations"

    return rf.aggregate_timeseries( directories, input_files_glob, outfile, column, grouping=grouping, subgrouping=subgrouping, verbose=verbose, separator=",", header=True, test=test, expected=expected )

def coding_mutations_collapse( grouping="", subgrouping="", verbose=False, type="mean", header=True, test=False, expected=None ): 

    outfile = "coding_mutations"
    return rf.collapse( outfile, outfile, grouping=grouping, subgrouping=subgrouping, verbose=verbose, type=type, header=header, test=test, expected=expected )  ## the double outfile is correct. :P

def degenerate_mutations_collapse( grouping="", subgrouping="", verbose=False, type="mean", header=True, test=False, expected=None ): 

    outfile = "degenerate_mutations"
    return rf.collapse( outfile, outfile, grouping=grouping, subgrouping=subgrouping, verbose=verbose, type=type, header=header, test=test, expected=expected )

def noncoding_mutations_collapse( grouping="", subgrouping="", verbose=False, type="mean", header=True, test=False, expected=None ): 

    outfile = "noncoding_mutations"
    return rf.collapse( outfile, outfile, grouping=grouping, subgrouping=subgrouping, verbose=verbose, type=type, header=header, test=test, expected=expected )
