#!/usr/bin/python

# Calculate the relative fitness increase ratio from a csv file.

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import math
import numpy
import itertools
from optparse import OptionParser

# Set up options
usage = """usage: %prog infile.csv
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
parser.add_option("--starting", dest = "starting", type="string",
                  help = "Supply your own starting value")


############## A NOTE ON THE DIMENSIONALITY ###################################
## The script expects each line to represent a time-series. The ratio is based
## on the starting value (the first value of the line).

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

## defaults
if not options.separator:
    options.separator = ","

## input filename
inputfilename = args[0]

if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

if options.verbose or options.debug_messages:
    print "Processing: '" + inputfilename + "'"

## build an array of values from the file.
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    if options.has_header:
        options.has_header = False
        continue
    
    line = line.split( options.separator ) ## break the line up on spaces

    line = [ float(val) for val in line ] ## convert to floats

    if options.starting:
        start_value = float(options.starting)
    else:
        start_value = line[0]

    ratios = [ str(val/start_value) for val in line ]

    print options.separator.join( ratios )

fd.close()




