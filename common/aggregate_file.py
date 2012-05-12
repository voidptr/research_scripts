#!/usr/bin/python

# Take a file, aggregate the entire content, and then output it as a line.

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import math
import numpy
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] infile
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-s","--separator", dest = "separator", type="string",
                  help = "the separator (comma, or space)")
parser.add_option("--header", action = "store_true", dest = "has_header",
                  default = False, help = "ignore a header in the input file(s)")
parser.add_option("--direction", dest = "direction", type="string",
                  help = "Aggregate the \"columns\" vertically (default), or the \"rows\".")
parser.add_option("--start_at", dest="start_at", type="int",
                  help="Only start doing the aggregation from datapoint <start_at>")

parser.add_option("--sum", action = "store_true", dest = "sum",
                  default = False, help = "in a given file, collapse each column's values as the sum and print that out")
parser.add_option("--mean", action = "store_true", dest = "mean",
                  default = False, help = "in a given file, collapse each column's values as the mean and print that out") 
parser.add_option("--median", action = "store_true", dest = "median",
                  default = False, help = "in a given file, collapse each column's values as the median and print that out") 
parser.add_option("--var", action = "store_true", dest = "var",
                  default = False, help = "in a given file, collapse each column's values as the var and print that out") 
parser.add_option("--std", action = "store_true", dest = "std",
                  default = False, help = "in a given file, collapse each column's values as the std and print that out") 
parser.add_option("--ste", action = "store_true", dest = "ste",
                  default = False, help = "in a given file, collapse each column's values as the ste and print that out") 
parser.add_option("--max", action = "store_true", dest = "max",
                  default = False, help = "in a given file, collapse each column's values as the max and print that out") 
## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

if not ( options.sum ^ options.mean ^ options.median ^ options.var ^ options.std ^ options.ste ^ options.max ):
    parser.error("aggregating functions are mutually exclusive (--sum, --mean, --median, --var, --std, or --ste, or --max)")

if not options.separator:
    options.separator = " "

if not options.direction:
    options.direction = "columns"

## input filename
inputfilename = args[0]

lines = [] ## each value is a sample

if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

if options.verbose or options.debug_messages:
    print "Processing: '" + inputfilename + "'"

## build an array of values from the file.
line_ct = 0
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    if line_ct == 0 and options.has_header:
        line_ct += 1
        continue
    
    line = line.split( options.separator ) ## break the line up on spaces

    if options.debug_messages:
        print "  value =", value

    lines.append( line ) ## collect the data
    line_ct += 1

fd.close()

## now, transpose the lists 

data = lines

if options.direction == "columns": ## transpose!
    data = zip(*lines) ## THEY SHOULD BE THE SAME SIZE

aggr_values = []
for unit in data:
    file_vals_num = [ float(i) for i in unit ]

    if options.start_at:
        file_vals_num = file_vals_num[options.start_at:] ## cut down what we need to aggregate.

    if options.sum:
        aggr_values.append( str(sum( file_vals_num ) ) )
    elif options.mean:
        aggr_values.append( str(numpy.mean( file_vals_num )) )
    elif options.median:
        aggr_values.append( str(numpy.median( file_vals_num ) ) )
    elif options.var:
        aggr_values.append( str(numpy.var( file_vals_num )) )
    elif options.std:
        aggr_values.append( str(numpy.std( file_vals_num )) )
    elif options.ste:
        aggr_values.append( str(numpy.std( file_vals_num ) / math.sqrt( len(file_vals_num) )) )
    elif options.max:
        aggr_values.append( str(max( file_vals_num )) )
    else:
        assert( "aggregate can only happen with a valid aggregation method." )

if options.debug_messages:
    print aggr_values

if options.direction == "columns":
    print ",".join( aggr_values )
else:
    for val in aggr_values:
        print val

