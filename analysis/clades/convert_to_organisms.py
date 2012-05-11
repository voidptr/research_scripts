# Extract single column to csv, and possibly perform some operations to it.

# Written in Python 2.7
# RCK
# 3-24-11

import os
import gzip
import math
import numpy
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] column_number thing_to_multiply guide 

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
if len(args) < 3:
    parser.error("incorrect number of arguments")

if options.separator == None:
    options.separator = " "

## column number
col_str = args[0]
col_id = int(col_str)

## input filename
thing_to_multiply = args[1]
guide = args[2]

number_of_organisms = [] ## each value is a sample


if guide[-3:] == ".gz":
#    fd = gzip.open(guide)
    os.popen("gunzip %s" % guide)

    if os.path.exists( guide[:-3] ):
        guide = guide[:-3]
    
#else:
fd = open(guide)

if options.verbose:
    print "Processing: '" + guide + "'"

## build an array of values from the file.
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.split( options.separator ) ## break the line up on spaces

    value = int(line[col_id - 1])

    if options.debug_messages:
        print "  value =%s" % value

    number_of_organisms.append( value ) ## collect the data

fd.close()

## print out the multiplied content.

if thing_to_multiply[-3:] == ".gz":
#    fd = gzip.open(guide)
    os.popen("gunzip %s" % thing_to_multiply)

    if os.path.exists( thing_to_multiply[:-3] ): ## did it gunzip?
        thing_to_multiply = thing_to_multiply[:-3]
    else:
        os.popen("mv %s %s" % (thing_to_multiply, thing_to_multiply[:-3])) 
        thing_to_multiply = thing_to_multiply[:-3]


fd = open(thing_to_multiply)

if options.verbose:
    print "Processing: '" + thing_to_multiply + "'"


genome_index = 0
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        print line
        continue

    for i in range(0, number_of_organisms[genome_index]): ## do it however many times it needs to be done.
        print line

    genome_index += 1
fd.close()


