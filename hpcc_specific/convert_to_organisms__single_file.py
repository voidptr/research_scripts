# Take a file, and multiply the output based on a column in it.

# Written in Python 2.7
# RCK
# 3-24-11

import os
import gzip
import math
import numpy
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] column file_to_multiply

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-s","--separator", dest = "separator", type="string",
                  help = "the separator (comma, or space)")

## fetch the args
(options, args) = parser.parse_args()


## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

if options.separator == None:
    options.separator = " "

## column number
col_str = args[0]
col_id = int(col_str)

## input filename
file_to_multiply = args[1]

fd = open(file_to_multiply)

if options.verbose:
    print "Processing: '" + file_to_multiply + "'"

## build an array of values from the file.
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    value = int(line.split( options.separator )[col_id - 1]) ## break the line up on spaces

    for i in range(0, value): ## do it however many times it needs to be done.
        print line
fd.close()


