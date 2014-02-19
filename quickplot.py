#!/usr/bin/python

###################
# Analyze
###################

# system includes
import glob
import os
from optparse import OptionParser
import sys

sys.path.append( os.path.abspath( os.path.join( sys.path[0], "common/" ) ) ) ## to common/
import config as cf

# note the paths to the utilities
analyzepath = os.path.abspath( os.path.join( sys.path[0], "analysis/analyze.py" ) )
plotpath = os.path.abspath( os.path.join( sys.path[0], "graph_generation/plot_from_csv.py" ) )


# Set up options
usage = """usage: %prog [options] outfile [input_file1 column1 \"directory_glob1\" name1 .. input_fileN columnN \"directory_globN\" nameN] 
          
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--plotonly", action = "store_true", dest = "plotonly",
                  default = False, help = "Skip the aggregation step, and plot only, using existing data files.")
parser.add_option("-t", "--title", dest = "title",
                  help = "set a different title than outfile (default)")
parser.add_option("-x", "--xlabel", dest="xlabel", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="ylabel", 
                  help="Y-axis Label")
parser.add_option("--data_members", dest="member_count",
                  help="Number of Components from a given data source (treatment)")
parser.add_option("--xtick_multiplier", dest="xtick_multiplier", 
                  help="X-axis Tick Multipliers")
parser.add_option("--ylog", action="store_true", dest="ylog",
                  help="Y-axis logarithmic scale")
parser.add_option("--error", dest="calculate_error", action="store_true", default = False,
                  help="include error bars - error values will be calculated from data using bootstrap")
parser.add_option("--end_at", dest="end_at",
                  help="Stop plotting at datapoint <end_at>")
## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 5: #outfile, plus a singular input set
    parser.error("incorrect number of arguments")

if (len(args[1:]) % 4) != 0:
    parser.error("incorrectly formatted input sets. (infile, column, directory glob, and name)")

outfile = args[0]

input_set_count = len(args[1:]) / 4

#input_set_count = 1
#if options.input_set_count:
#    input_set_count = int(options.input_set_count)

title = outfile
if options.title:
    title = options.title

error_opt = ""
if options.calculate_error:
    error_opt = " --error"

xlabel_opt = ""
if options.xlabel:
    xlabel_opt = " --xlabel \"" + options.xlabel + "\"" 

ylabel_opt = ""
if options.ylabel:
    ylabel_opt = " --ylabel \"" + options.ylabel + "\"" 

datamembers_opt = ""
if options.member_count:
    datamembers_opt = " --data_members " + options.member_count  

xtickmult_opt = ""
if options.xtick_multiplier:
    xtickmult_opt = " --xtick_multiplier " + options.xtick_multiplier

endat_opt = ""
if options.end_at:
    endat_opt = " --end_at " + options.end_at 

ylog_opt = ""
if options.ylog:
    ylog_opt = " --ylog"

## extract the list of input files and columns
input_files = []
columns = []
globs = []
names = []

for i in range(1, (input_set_count*4) + 1, 4):
    input_files.append( args[i] )
    columns.append( args[i + 1] )
    globs.append( args[i + 2] )
    names.append( args[i + 3] )

#print input_files
#print columns
#print globs
#print names

if input_set_count != len(input_files) != len(columns) != len(globs) != len(names):
    parser.error("input_set_count must equal the number of input files, columns, and directory globs")

expanded_globs = []
for thing in globs:

    output = glob.glob(thing)
    if len(output) > 0:
        expanded_globs.append( output )

if len(expanded_globs) < 1 :
    parser.error("directory glob does not interpret into anything.")

aggregated_names = []
for i in range(0, input_set_count):
    ####### FIRST, DO THE AGGREGATIONS
    
    ag_name = outfile + "." + names[i]
    aggregated_names.append( ag_name )

    command = "python " + analyzepath + " -i \"" + input_files[i] + "*\" -c " + columns[i] + " -o " + ag_name + " timeseries " + " ".join(expanded_globs[i])

    print
    print "Aggregating " + names[i] + ":"
    print command
    if options.plotonly:
        print "~~SKIPPING, PLOTTING ONLY~~"
    else:
        print os.popen( command ).read()

####### THEN, PLOT IT.

agnames_csv = [ name + ".timeseries.csv" for name in aggregated_names ]

command = "python " + plotpath + " -o --title \"" + title + "\"" + error_opt + ylog_opt + endat_opt + xlabel_opt + ylabel_opt + datamembers_opt + xtickmult_opt + " --legend \"" + ",".join(names) + "\" " + outfile + ".png " + " ".join(agnames_csv)

print
print "Plotting " + outfile + ":"
print command
print os.popen( command ).read()
