# Extract single column to csv

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] from to infile1 [infile2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--dimensionality", dest = "dimensionality", type="int",
                  help = "treat input data as one or two dimensional")
parser.add_option("--name", dest = "column_name", help = "name of the data")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 3:
    parser.error("incorrect number of arguments")

## patterns
from = args[0]
to = args[1]

## input filename
inputfilenames = args[2:]

#values = [] ## each value is a sample

for inputfilename in inputfilenames:

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    if from in inputfilename:
        index = inputfilename.find(from)
        length = len(from)

        print "mv " + inputfilename + " " + inputfilename[0:index] + to + inputfilename[index+length:]


