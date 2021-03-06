# Extract single column to csv

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] column_number expression prefix infile1 [infile2 ...]

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
if len(args) < 2:
    parser.error("incorrect number of arguments")

## column number
col_str = args[0]
col_id = int(col_str)

## test expression
expr = args[1]

## output prefix
prefix = args[2]

## input filename
inputfilenames = args[3:]

#values = [] ## each value is a sample

for inputfilename in inputfilenames:

    file_values = []

    outputfilename = inputfilename

    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
        outputfilename = inputfilename[0:-3] ## amend it to not use the gz, since this file won't be compressed.
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        whole_line = line

        line = line.split() ## break the line up on spaces

        value = line[col_id - 1]

        evaluate_string = str(value) + expr

        if options.debug_messages:
            print evaluate_string

        if eval( evaluate_string ) == False:
            if options.debug_messages:
                print "  FALSE - skipping"
            continue

        file_values.append( whole_line ) ## collect the data

    fd.close()

    outfile = open( prefix + outputfilename, 'w' )

    if options.debug_messages:
        print outfile

    for line in file_values:
        outfile.write( line + "\n" ) 

    outfile.close()


