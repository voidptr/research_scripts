############ Run File Data Extraction and Aggregation ###########

import glob
import os
import sys
sys.path.append("../../common/") ## to analysis/
import config as cf## some basic shit that I don't want to do myself

cf.addpath( "integrity_testing/" )
import integrity_testing as it

extract_single_column_to_csv_path = cf.getpath( "common/extract_single_column_to_csv.py" )
aggregate_file_path = cf.getpath( "common/aggregate_file.py" )

def aggregate_timeseries( directories, input_files_glob, outfile, column, grouping="", subgrouping="", verbose=False, separator=" ", header=False, test=False, expected=None ):

    cwd = cf.Config.Script.cwd

    if grouping:
        grouping = "%s_" % grouping
    if subgrouping:
        subgrouping = "%s__" % subgrouping

    headeropt = ""
    if header:
        headeropt = "--header"


    aggregate_filename = os.path.join( cwd, "%s%s%s.timeseries.csv" % (grouping, subgrouping, outfile) )
    
    if test:
        return it.test( directories, input_files_glob, expected=expected )
    else:

        if it.test( directories, input_files_glob, expected=expected ): ## test the integrity of the given directories. In particular that they have the files I am looking for.
            ## do the work

            if os.path.exists( aggregate_filename ):
                os.unlink( aggregate_filename )

            for dir in directories:
                print dir
                os.chdir(dir)

                cmd = "python2 %s --dimensionality 1 %s -s \"%s\" %s %s >> %s" % ( extract_single_column_to_csv_path, headeropt, separator, column, input_files_glob[0], aggregate_filename )
                print cmd
                os.popen( cmd )

                os.chdir(cwd)

            return True

        return False

def collapse( infile, outfile, type="mean", grouping="", subgrouping="", verbose=False, separator=",", header=False, test=False, expected=None, passoptions="" ):

    cwd = cf.Config.Script.cwd

    if grouping:
        grouping = "%s_" % grouping
    if subgrouping:
        subgrouping = "%s__" % subgrouping

    headeropt = ""
    if header:
        headeropt = "--header"

    aggregate_infile = os.path.join( cwd, "%s%s%s.timeseries.csv" % (grouping, subgrouping, infile) )
    collapsed_filename = os.path.join( cwd, "%s%s%s.%s.csv" % (grouping, subgrouping, outfile, type) )

    if test:
        return it.test(  ["./"], [aggregate_infile], expected=expected )
    else:

        if it.test( ["./"], [aggregate_infile], expected=expected ): ## test the integrity of the given directories. In particular that they have the files I am looking for.
            ## do the work
    
            if os.path.exists( collapsed_filename ):
                os.unlink( collapsed_filename )

            cmd = "python2 %s %s --direction rows %s -s \"%s\" --%s %s >> %s" % ( aggregate_file_path, passoptions, headeropt, separator, type, aggregate_infile, collapsed_filename )

            print cmd
            os.popen( cmd )

            return True

        return False
