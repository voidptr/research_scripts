############ Fitness Data Extraction and Aggregation ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to common/
import config as cf## some basic shit that I don't want to do myself


cf.addpath( "run_file_aggregation/" )
import run_file_aggregation as rf


## aggregate the contents of the tasks.dat file
def aggregate_timeseries( directories, input_files_glob="", column="", outfile="", grouping="", subgrouping="", verbose=False, test=False, expected=None ):

    input_files_glob_list = [input_files_glob] ## this is actually a globbing pattern
    #column = 4
    #outfile = "fitness"

    print "CRAP"
    print input_files_glob_list
    print column
    print outfile
    print "DONE"

    return rf.aggregate_timeseries( directories, input_files_glob_list, outfile, int(column), grouping=grouping, subgrouping=subgrouping, verbose=verbose, test=test, expected=expected )

#def collapse( outfile="", grouping="", subgrouping="", verbose=False, type="mean", test=False, expected=None, passoptions="" ): 
#
#    #outfile = "fitness"
#    return rf.collapse( outfile, outfile, grouping=grouping, subgrouping=subgrouping, verbose=verbose, type=type, test=test, expected=expected, passoptions=passoptions )  ## the double outfile is correct. :P

