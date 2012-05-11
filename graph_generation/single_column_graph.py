# Single Column Graph

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile column_name column_number x-axis infile1 [infile2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-g", "--graph", action = "store_true", dest = "showgraph",
                  default = False, help = "show the graph")
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-m", "--median", action="store_true", dest = "median",
                default = False, help = "calculate and display median")
parser.add_option("-o", "--medianonly", action="store_true", dest = "median_only",
                  default = False, help = "calculate and display median ONLY")
parser.add_option("-l", "--logscale", action="store_true", dest = "log_scale",
                  default = False, help = "display y-axis as log scale")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 3:
    parser.error("incorrect number of arguments")
if options.median_only and options.median:
    parser.error("-m and -o are mutually exclusive")

## output file name
outfilename = args[0]

## column name (y-axis)
column_name = args[1]

## column number
col_str = args[2]
col_id = int(col_str)

## x-axis
x_axis = args[3]

## input filename
inputfilenames = args[4:]

fitness_2d_array = [] ## each row is a sample, each column is a file

for inputfilename in inputfilenames:
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    line_num = 0
    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue
        line = line.split() ## break the line up on spaces

        fitness = float(line[col_id - 1]) ## dunno if this is right

        if fitness < 0: ## skip this bit
            continue

        if options.debug_messages:
            #print "  update = ", update
            print "  value =", fitness
            print " "
        
        if len(fitness_2d_array) <= line_num:
          fitness_2d_array.append( [] )

        fitness_2d_array[line_num].append( fitness )

#        if (options.debug_messages):
#            print fitness

        line_num += 1 

    fd.close()

pl.xlabel(x_axis)
pl.ylabel(column_name)

if options.log_scale:
    # set to log scale
    pl.yscale('log')

if options.median_only:
    median_fitness_array = []
    for datapoint in fitness_2d_array:
        median_fitness_array.append( np.mean( datapoint ) )
    plottable = np.add( median_fitness_array, 0 )
    pl.plot( plottable )
elif options.median:
    plottable = np.add( fitness_2d_array, 0 )
    pl.plot( plottable, '#CCCCCC' )
 
    median_fitness_array = []
    for datapoint in fitness_2d_array:
        median_fitness_array.append( np.mean( datapoint ) )
    plottable = np.add( median_fitness_array, 0 )

#    for datapoint in fitness_2d_array:
#        datapoint.append( np.mean( datapoint ) )
    pl.plot( plottable, 'k' )
else:
    plottable = np.add( fitness_2d_array, 0 )
    pl.plot( plottable )

pl.savefig(outfilename)
