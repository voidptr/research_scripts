############ Coalescence Data Extraction and Aggregation ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to analysis/
import config as cf ## some basic shit that I don't want to do myself

cf.addpath( "run_file_aggregation/" )
import run_file_aggregation as rf

## aggregate the contents of the tasks.dat file
def aggregate_timeseries( directories, grouping="", subgrouping="", verbose=False, test=False, expected=None ):

    input_files_glob = ["stats.dat*"] ## this is actually a globbing pattern
    column = 10
    outfile = "coalescent_generations"

    return rf.aggregate_timeseries( directories, input_files_glob, outfile, column, grouping=grouping, subgrouping=subgrouping, verbose=verbose, type=type, test=test, expected=expected )

