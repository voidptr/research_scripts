#!/usr/bin/python

# histogram from a CSV 
# pre-binned, already counted distribution

# Written in Python 2.7
# RCK
# Nov 2014


import matplotlib
matplotlib.use('Agg')

import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile infile1 [infile2 infile3...] 

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
parser.add_option("--xlim_max", dest="xlim_max", type="float",
                  help="Set the max xlim")
parser.add_option("--xlim_min", dest="xlim_min", type="float",
                  help="Set the min xlim")
                  
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
inputfilenames = args[1:]

if not options.separator:
    options.separator="," ## default

files = []
for inputfilename in inputfilenames:
    
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
    files.append( file_data )

if options.debug_messages:
    print "RAW INPUT"
    print files

class Colors:
    Black = (0.0, 0.0, 0.0, 1.0)
    DarkGray = (0.65, 0.65, 0.65, 1.0)
    Gray = (0.75, 0.75, 0.75, 1.0)
    LightGray = (0.85, 0.85, 0.85, 1.0)
    VeryLightGray = (0.9, 0.9, 0.9, 1.0)
    White = (1.0, 1.0, 1.0, 1.0)
    Transparent = (0, 0, 0, 0)

    Purple = (0.55, 0.0, 0.55, 1.0)
    LightPurple = (0.8, 0.7, 0.8, 1.0) 

    Blue = (0.20, 0.49, 0.95, 1.0)
    LightBlue = (0.6, 0.7, 0.95, 1.0)
    DarkBlue = (0.1, 0.3, 0.7, 1.0)

    BlueGreen = (0.0, 1.0, 1.0, 1.0)
    LightBlueGreen = (0.8, 1.0, 0.8, 1.0)

    Green = (0.0, 0.7, 0.0, 1.0)
    LightGreen = (0.8, 1.0, 0.8, 1.0)

    Yellow = (0.9, 0.9, 0.0, 1.0)   

    Orange = (0.93, 0.67, 0.13, 1.0)

    OrangeRed = (1.0, 0.7, 0.0, 1.0)
    LightOrangeRed = (0.9, 0.7, 0.6, 1.0)
    DarkOrangeRed = (0.5, 0.3, 0.2, 1.0)

    Red = (0.95, 0, 0.0, 1.0)
    LightPink = (0.8, 0.7, 0.7, 1.0)
    DarkPink = (0.86, 0.62, 0.65, 1.0)

    TransparentGray = (0.75, 0.75, 0.75, 0.5)
    Default = (0.0, 0.0, 0.0, 1.0)

color_sets = [ Colors.Purple, 
    Colors.Orange, 
    Colors.BlueGreen, 
    Colors.Yellow, 
    Colors.DarkPink, 
    Colors.LightGreen, 
    Colors.DarkOrangeRed,
    Colors.LightPurple,
    Colors.DarkGray,
    Colors.Blue,
    Colors.Red,
    Colors.LightOrangeRed,
    Colors.LightBlue,
    Colors.VeryLightGray] #max seven items per group 


## generate the histogram 


print files

artists = []
fig = pl.figure()
ax1 = fig.add_subplot(111)

bins = np.arange(0, 256)

bar_width = 1.0 / len(files) ## how many bars in each pair

for idx in range(len(files)):
    file_data = files[idx]
    vals = np.zeros(256)

    for i in range(len(file_data)):
        vals[i] = file_data[i]

    #pl.bar(bins, vals)

    artists.append( ax1.bar( bins+(bar_width*idx), vals, bar_width, color=color_sets[ idx ], linewidth=0, edgecolor=color_sets[ idx ] ) )


#print vals
#print bins

ax1.set_xlabel( options.x_label )
ax1.set_ylabel( options.y_label )

if options.title:
    pl.title( options.title )

xlim_min = 0
if options.xlim_min:
    xlim_min = options.xlim_min

if (options.xlim_max):
    pl.xlim([xlim_min,options.xlim_max])

pl.savefig(outfilename)
