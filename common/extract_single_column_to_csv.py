#!/usr/bin/python

# Extract single column to csv, and possibly perform some operations to it.

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import math
import numpy
import itertools
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] column_number infile1 [infile2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--dimensionality", dest = "dimensionality", type="int",
                  help = "treat output data as one or two dimensional")
parser.add_option("-s","--separator", dest = "separator", type="string",
                  help = "the separator (comma, or space)")
parser.add_option("--name", dest = "column_name", help = "name of the data")
parser.add_option("--header", action = "store_true", dest = "has_header",
                  default = False, help = "ignore a header in the input file(s)")

parser.add_option("--sum", action = "store_true", dest = "sum_column",
                  default = False, help = "in a given file, collapse the column's values as the sum and print that out")
parser.add_option("--mean", action = "store_true", dest = "mean_column",
                  default = False, help = "in a given file, collapse the column's values as the mean and print that out") 
parser.add_option("--median", action = "store_true", dest = "median_column",
                  default = False, help = "in a given file, collapse the column's values as the median and print that out") 
parser.add_option("--var", action = "store_true", dest = "var_column",
                  default = False, help = "in a given file, collapse the column's values as the var and print that out") 
parser.add_option("--std", action = "store_true", dest = "std_column",
                  default = False, help = "in a given file, collapse the column's values as the std and print that out") 
parser.add_option("--ste", action = "store_true", dest = "ste_column",
                  default = False, help = "in a given file, collapse the column's values as the ste and print that out") 
parser.add_option("-c", "--calculate_stats", action = "store_true", dest = "calc_stats",
                  default = False, help = "in a given file, calculate the stats of the column and print those out instead")


##### A NOTE ON DIMENSIONALITY
## --dimensionality 1
##  treat the output data as linearly 1-D; every stack of values from a file is added to the final 
##  values array as individual scalars. If there is more than one value in a file and you are not aggregating,
##  this is PROBABLY not what you want.
##
##  This is what you want if each file is a single line. (this is an unusual situation, but whatever).
##  eg, the output would look like:
##   file1.val1, file1.val2, file1.val3, file2.val1, file2.val2, file2.val3
##
## --dimensionality 2 (default!)
##  treat it as 2-D; every stack of values from a file is added to the values array as its own array, creating
##  a two-dimensional structure. If there is more than one target value in your file, this is probably what you want.
##  eg, the output would look like:
##   file1.val1, file1.val2, file1.val3
##   file2.val1, file2.val2, file2.val3

##### A NOTE ON SUM_COLUMN, MEAN_COLUMN, 
## --sum --mean --median --std --ste --var
##  These methods respects output_dimensionality
##
##  If --dimensionality 1, it will take each file, and print the sum of the selected column as a value in the line
##  output:
##   file1.aggrval, file2.aggrval, file3.aggrval
##
##  If --dimensionality 2, it will take each file, and print the sum of the selected column on a line on its own
##  output:
##   file1.aggrval
##   file2.aggrval
##   file3.aggrval

##### A NOTE ON CALC_STATS ON COLUMN
## -c
##  This method assumes output --dimensionality 2. Specifically, it assumes that each file is a statistical entity
##  It will calculate the mean, median, variance, std, and ste over the selected column in a file, and output that as a single line
##  If each file only contains one value, this is probably not what you want.
##  output:
##   file1.mean, file1.median, file1.variance, file1.std, file1.ste
##   file2.mean, file2.median, file2.variance, file2.std, file2.ste


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

aggregate = False
if ( options.sum_column or options.mean_column or options.median_column or options.var_column or options.std_column or options.ste_column ):
    aggregate = True
    if not ( options.calc_stats ^ options.sum_column ^ options.mean_column ^ options.median_column ^ options.var_column ^ options.std_column ^ options.ste_column ):
        parser.error("aggregating functions are mutually exclusive (--calc_stats, --sum, --mean, --median, --var, --std, or --ste)")

if not options.dimensionality:
    options.dimensionality = 2 ## two-d is the default, where there is more than one line in a given input file, and you want to collect a column from all of the lines

aggregate = False
if ( options.sum_column or options.mean_column or options.median_column or options.var_column or options.std_column or options.ste_column ):
    aggregate = True

if options.calc_stats: ## see note above.
    options.dimensionality = 2 ## output this way, since the alternative doesn't make a whole lot of sense.

if not options.separator:
    options.separator = " "

## column number
col_str = args[0]
col_id = int(col_str)

## input filename
inputfilenames = args[1:]

values = [] ## each value is a sample

for inputfilename in inputfilenames:

    file_values = []

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

        try:
            value = line[col_id - 1] 
        except: ## if there's a problem, skip the line. This should probably be made configurable at some point.
            continue ## this is a little bit of a gamble and a possible SOURCE OF BUG. :/

        if value < 0: ## skip this bit
            continue

        if options.debug_messages:
            print "  value =", value

        file_values.append( value ) ## collect the data
        line_ct += 1

    fd.close()

    values.append( file_values ) ## always treat input as 2-D; every file is a treated as its own array (even with a single member), creating a 2-d array


if options.column_name:
    print "#" + options.column_name

if aggregate:
    if options.debug_messages:
        print "AGGREGATING"

    aggr_values = []
    for file_vals in values:
        file_vals_num = [ float(i) for i in file_vals ]
        if options.sum_column:
            aggr_values.append( [ str(sum( file_vals_num ) ) ] )
        elif options.mean_column:
            aggr_values.append( [ str(numpy.mean( file_vals_num )) ] )
        elif options.median_column:
            aggr_values.append( [ str(numpy.median( file_vals_num ) ) ])
        elif options.var_column:
            aggr_values.append( [ str(numpy.var( file_vals_num )) ] )
        elif options.std_column:
            aggr_values.append( [ str(numpy.std( file_vals_num )) ] )
        elif options.ste_column:
            aggr_values.append( [ str(numpy.std( file_vals_num ) / math.sqrt( len(file_vals_num) )) ] )
        else:
            assert( "aggregate can only happen with a valid aggregation method." )

    values = aggr_values ## replace with the aggregated output

    if options.debug_messages:
        print aggr_values

if (options.calc_stats):
    if options.debug_messages:
        print "CALC STATS"
    calc_values = []

    for file_vals in values: ## calc the stats for each array
        #print len(file_vals)

        if len(file_vals) == 0: ## for whatever reason, this file was empty, maybe because there were no organisms during this sample.
            print "nan,nan,nan,nan,nan"
            continue

        file_vals_num = [ float(i) for i in file_vals ]

        mean = numpy.mean(file_vals_num)
        median = numpy.median(file_vals_num)
        variance = numpy.var(file_vals_num)
        std = numpy.std(file_vals_num)
        ste = std / math.sqrt( len(file_vals_num) )
        
        calc_values.append ( [str(mean), str(median), str(variance), str(std), str(ste)] )

    values = calc_values ## replace with the statistical output

if options.debug_messages:
    print values

if (options.dimensionality == 1): ## essentially, print all the values you have gathered on a single line
    print ",".join( list(itertools.chain(*values)) ) ## flatten the 2-d array and print it out all in one line.
else: ## default!
    for i in values: ## print all the values you have gathered, one line per file.
        print ",".join( i )

