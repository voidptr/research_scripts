#!/usr/bin/python

# histogram from a CSV 

# Written in Python 2.7
# RCK
# 1-10-12


import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile infile

Permitted types for outfile are png, pdf, ps, eps, and svg

Assumes that the input file contains the pre-counted and binned histogram values.
For raw data counting and plotting, use distribution_from_csv.py
"""
parser = OptionParser(usage)
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print verbose messages to stdout")
parser.add_option("-l", "--legend", action="store_true", dest = "legend",
                  default = False, help = "include a legend")
parser.add_option("-x", "--xlabel", dest="x_label", type="string", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="y_label", type="string", 
                  help="Y-axis Label")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Graph Title")
parser.add_option("--ylim_max", dest="ylim_max", type="float",
                  help="Set the max ylim")
parser.add_option("--has_header", dest="has_header", action="store_true", default = False, help = "Contains header line, so ignore it")
parser.add_option("-s", "--separator", dest="separator", type="string", help="Separator")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## output file name
outfilename = args[0]

## input filenames
inputfilename = args[1]

if not options.separator:
    options.separator="," ## default

    
if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

line_ct = 0
file_data = []
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.split(options.separator)    
    #file_data.append( float( line[ int(column) - 1] ) )
    file_data = [float(v) for v in line] 
       
    line_ct += 1   
fd.close()

if options.debug_messages:
    print "RAW INPUT"
    print file_data

## generate the histogram 


print file_data

artists = []
fig = pl.figure()
ax1 = fig.add_subplot(111)

bins = np.arange(0, 256)
vals = np.zeros(256)



for i in range(len(file_data)):
    vals[i] = file_data[i]

pl.bar(bins, vals)

print vals
print bins

ax1.set_xlabel( options.x_label )
ax1.set_ylabel( options.y_label )

if options.title:
    pl.title( options.title )

pl.savefig(outfilename)
