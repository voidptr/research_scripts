# Extract single column to csv, and possibly perform some operations to it.

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import math
import numpy
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
                  help = "treat input data as one or two dimensional")
parser.add_option("-s","--separator", dest = "separator", type="string",
                  help = "the separator (comma, or space)")
parser.add_option("--name", dest = "column_name", help = "name of the data")
parser.add_option("-c", "--calculate_stats", action = "store_true", dest = "calc_stats",
                  default = False, help = "in a given file, calculate the stats of the column and print those out instead")


##### A NOTE ON DIMENSIONALITY
## --dimensionality 1
##  treat the data as linearly 1-D; every stack of values from a file is added to the final 
##  values array as individual scalars. If there is more than one value in a file, this is PROBABLY not what you want.
##  This is what you want if each file is a single line. (this is an unusual situation, but whatever).
##  eg, the output would look like:
##   file1.val1, file1.val2, file1.val3, file2.val1, file2.val2, file2.val3
##
## --dimensionality 2
##  treat it as 2-D; every stack of values from a file is added to the values array as its own array, creating
##  a two-dimensional structure. If there is more than one target value in your file, this is probably what you want.
##  eg, the output would look like:
##   file1.val1, file1.val2, file1.val3
##   file2.val1, file2.val2, file2.val3

##### A NOTE ON CALC_STATS ON COLUMN
## -c
##  This method assumes --dimensionality 2. Specifically, it assumes that each file is a statistical entity
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

if options.calc_stats: ## see note above.
    options.dimensionality = 2

if options.separator == None:
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

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    ## build an array of values from the file.
    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        line = line.split( options.separator ) ## break the line up on spaces

        value = line[col_id - 1] 

        if value < 0: ## skip this bit
            continue

        if options.debug_messages:
            print "  value =", value

        file_values.append( value ) ## collect the data

    fd.close()

    if (options.dimensionality == 1):
        values.extend( file_values ) 
    else:
        values.append( file_values ) ## treat it as 2-D; every value is a treated as its own array (with a single member?), creating a 2-d array


if options.column_name:
    print "#" + options.column_name

if (options.calc_stats):
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
        
        print ",".join( [str(mean), str(median), str(variance), str(std), str(ste)] )

elif (options.dimensionality == 1): ## essentially, print all the values you have gathered on a single line
    print ",".join( values )

else:
    for i in values: ## print all the values you have gathered, one line per file.
        print ",".join( i )

