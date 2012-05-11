# Extract the "in-phase" values from the csv file


# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] infile

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-p", action="store_true", default=False, dest="phase")
parser.add_option("-s", action="store_true", default=False, dest="strip_header")
parser.add_option("-i", type="int", dest="data_start")



## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

## input filename
inputfilename = args[0]

## define a helper function
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

##### do the actual work #######

values = [] ## each value is a sample
if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

ct = 0
for line in fd:
    ct = ct+1


    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    if ct == 1 and options.strip_header:
        continue

    line = line.split(',') ## break the line up on commas

#    print(len(line))

    if len(line) == 0:
        continue

    values.append(line) ## tack the values into there.

fd.close()

phased_lines = []
for line in values:
    line_phase_values = []

    phase = 0 ## first phase (hurt)
    if options.phase:
        phase = 1 ## second phase (ok)

    start = 0

    if options.data_start:
        start = options.data_start
        line_phase_values.extend( line[0:options.data_start] )

#    if not is_number(line[0]): ## if we have something else at the start of the line.
#        start = 1
#        line_phase_values.append(line[0])

    ## with increments of 500, and a zero start, the first snapshot of the result of the first phase of the first cycle should fall at update 50,500, which is index 101
    ## equivalently, the result of the last phase of the last cycle should fall on update 100,000, which is index 200
    ## there are 100 phase result snapshots. Now, we only want the result first phase of the cycle, which is where the magic happens (no reward, or punishment).

    #print len(line)

    for i in range(start + phase + 101, start + phase + 201, 2):
#        print i
        line_phase_values.append( line[i] )      
        
    phased_lines.append( line_phase_values )

#if options.store_header:
#    print header

for line in phased_lines:
#    print len(line)
    print ','.join( line )











