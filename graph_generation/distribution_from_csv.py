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
usage = """usage: %prog [options] column outfile infile

Permitted types for outfile are png, pdf, ps, eps, and svg
Multiple columns may be listed as comma separated enclosed in quotes.
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
if len(args) < 3:
    parser.error("incorrect number of arguments")

## column to use
column = int(args[0])

## output file name
outfilename = args[1]

## input filenames
inputfilename = args[2]

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

    if line_ct == 0 and options.has_header: ## the first line is a header line. skip it.
        line_ct += 1
        continue

    line = line.split(options.separator)    
    file_data.append( float( line[ int(column) - 1] ) )
       
    line_ct += 1   
fd.close()

if options.debug_messages:
    print "RAW INPUT"
    print file_data

## generate the histogram 

mean = np.mean( file_data )
std = np.std( file_data )

print file_data
print mean
print std

artists = []
fig = pl.figure()
ax1 = fig.add_subplot(111)

n, bins, patches =  pl.hist( file_data, normed=1, histtype="stepfilled" )

print n
print bins

y = pl.normpdf( bins, mean, std )
l = pl.plot( bins, y, 'k--', linewidth=1.5)

ax1.set_xlabel( options.x_label )
ax1.set_ylabel( options.y_label )

if options.title:
    pl.title( options.title )

pl.savefig(outfilename)
