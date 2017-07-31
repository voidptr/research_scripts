# Plot from CSV(s)

# Written in Python 2.7
# RCK
# 1-10-12

# Rewritten to suck less
# RCK
# 5-30-12

import matplotlib
matplotlib.use('Agg')

import gzip
import numpy as np
import pylab as pl
from scipy import stats
import scipy  
import scikits.bootstrap as bootstrap
import math
from optparse import OptionParser
import os
import sys
from cycler import cycler

# Set up options
usage = """
 %prog [options] outfile infile1 [infile2]

Permitted types for outfile are png, pdf, ps, eps, and svg
Input files must be grouped by treatment group, and sorted
by desired display order"""
parser = OptionParser(usage)
## version
parser.add_option("--version", action = "store_true", dest = "display_version",
                  default = False, help = "Output the version message and exit")
## output
parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")

## data input
parser.add_option("-d", "--delimiter", dest="delimiter", type="string",
                  help="Datafile delimiter")
parser.add_option("--data_members", dest="member_count", type="int",
                  help="Number of Components from a given data source (treatment)")
parser.add_option("--start_at", dest="start_at", type="int",
                  help="Only start plotting from datapoint <start_at>")
parser.add_option("--end_at", dest="end_at", type="int",
                  help="Stop plotting from datapoint <end_at>")
parser.add_option("--has_header", dest="has_header", action="store_true", default = False, help = "Contains header line, so ignore it")

## basic display
parser.add_option("-o", "--mean", action="store_true", dest = "mean",
                  default = True, help = "calculate and display mean")
parser.add_option("-a", "--all", action="store_true", dest = "all",
                  default = False, help = "display all lines of a source")
parser.add_option("--error", dest="calculate_error", action="store_true", default = False,
                  help="include error bars - error values will be calculated from data using bootstrap")
parser.add_option("--samples", dest="samples", type="int",
                  help="how many samples to draw for bootstrap?")


## legends and labels
parser.add_option("-l", "--legend", dest="legend", type="string", 
                  help = "include a legend, (values)")
parser.add_option("-x", "--xlabel", dest="xlabel", type="string", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="ylabel", type="string", 
                  help="Y-axis Label")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Graph Title")
parser.add_option("--include_chevrons", dest="include_chevrons", 
                  action="store_true", default = False, 
                  help="Include line marker glyphs in addition to color")
parser.add_option("--chevrons_by_members", dest="member_chevrons", 
                  action="store_true", default = False, 
                  help="Make the chevrons track by members, along with line style")
## visual mods
parser.add_option("--xtick_multiplier", dest="xtick_multiplier", type="int", 
                  help="X-axis Tick Multipliers")
parser.add_option("--alt_axis", dest="alt_axis", type="int",
                  help="Use an alternative axis for the Nth data source")
parser.add_option("-w", "--ylabel_alt_axis", dest="y_label_alt_axis", type="string", 
                  help="Alternative Y-axis Label")
parser.add_option("--ylim_max", dest="ylim_max", type="float",
                  help="Set the ylim max")
parser.add_option("--ylim_min", dest="ylim_min", type="float",
                  help="Set the ylim min")
parser.add_option("--xlim_max", dest="xlim_max", type="float",
                  help="Set the xlim max")
parser.add_option("--xlim_mix", dest="xlim_min", type="float",
                  help="Set the xlim min")
parser.add_option("--ylog", action="store_true", dest="ylog",
                  default=False, help="Display the Y-axis on a logarithmic scale")
## fetch the args
(options, args) = parser.parse_args()

## handle version
if options.display_version:
    print sys.argv[0]
    print "Version: ", os.popen("git describe --tags").read()
    exit(0)

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

if options.member_count:
    input_file_count = len(args[1:])
    if input_file_count % options.member_count > 0:
        parser.error("The number of input files provided must be a multiple of member count") 

## parameter defaults -- do this here because optparse seems to fuck this up
if not options.member_count:
    options.member_count = 1

if not options.delimiter:
    options.delimiter = ','

## output file name
outfilename = args[0]

## input filenames
inputfilenames = args[1:]


## read the input data
data = []
for inputfilename in inputfilenames:

    data_2d_array = [] ## each row is run, each column is a datapoint in that run
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        if options.has_header: ## the first line is a header line. skip it.
            options.has_header = False ## clear it
            continue

        line = line.split(',') ## break the line up on commas
        line = [val if val is not "nan" else "0" for val in line] # replace "nan" with 0

        ## handle data limiting
        if options.end_at:
            line = line[:options.end_at+1] ## chop off whatever.

        if options.start_at:
            line = line[options.start_at:] ## chop off whatever.

        data_2d_array.append( line )
        
    fd.close()

    data.append( data_2d_array )



## start plotting
fig = pl.figure()
axes = [ fig.add_subplot(111) ]
axes.append( axes[0].twinx() )

axis_indexes = []

for i in range(0, len(data)):
    if options.alt_axis == (i % options.member_count):
        axis_indexes.append( 1 )
    else:
        axis_indexes.append( 0 )


## calculate the mean (and error) for each file
mean_data_array = []
   
for data_2d_array in data:
    ## transpose so that each array is now all the values for a given sample
    transposed = zip(*data_2d_array)
    cleaned = []
    for sample_array in transposed:
        cleaned.append( [ float( val ) for val in sample_array if val != "nan" ] ) ## filter out nan's and convert to floating point 

    means = []
    for sample in cleaned:
        means.append( np.mean( sample ) )
    mean_data_array.append( means )

## now, plot the things
for i in range(0, len(mean_data_array)):
    plottable = np.add( mean_data_array[i], 0 )
    plottable = np.transpose( plottable )

    
    axes[ axis_indexes[i] ].plot(plottable) 


pl.savefig(outfilename)
