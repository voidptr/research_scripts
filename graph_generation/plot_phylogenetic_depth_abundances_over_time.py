# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import math
import numpy as np
#import pylab as pl
import matplotlib.pyplot as pl
import matplotlib.cm as cm
import matplotlib.colors as colors

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile phylo_depth_abundances_over_time.csv

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true",
                  dest = "debug_messages", default = False,
                  help = "print debug messages to stdout")

parser.add_option("--most_recent_coalescence",
                  dest="most_recent_coalescence_file_and_col", type="string",
                  help="Plot the most recent coalescensce based on stats.dat",
                  metavar="\"file, column\"")

parser.add_option("-t", "--title", dest="title", type="string",
                  help="Supplemental Graph Title")

parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

### Fetch Parameters
inputfilename = args[1]

outfile = args[0]

coalescence_data = []
if options.most_recent_coalescence_file_and_col:

    (coalescence_file, coalescence_col) = \
        options.most_recent_coalescence_file_and_col.split(",")
    coalescence_col = int(coalescence_col) - 1

    if coalescence_file[-3:] == ".gz":
        fd_coal = gzip.open( coalescence_file )
    else:
        fd_coal = open( coalescence_file )

    for line in fd_coal:
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            continue

        line = line.split()

        coalescence_data.append( int(line[ coalescence_col ]) )

    fd_coal.close()

## read the file
if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

count_arrays = []

for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    line = line.split(',')
    line = [int(bit) for bit in line]
    count_arrays.append( line )


### plot the thing

## convert to log
log_count_arrays = [ [ math.log(count) if count > 0 else 0 for count in sample ]
                     for sample in count_arrays ]

## apply coalescene information, if optioned.
if options.most_recent_coalescence_file_and_col:
    ## grab the max value in the log_count_arrays
    max_log_count = max( [ max(sample) for sample in log_count_arrays ] )

    ## this is the value that we will set.
    for (depth, sample) in zip(coalescence_data, log_count_arrays):
        sample[ depth ] = max_log_count ## set it.

## import and transpose
counts_plottable = np.array( log_count_arrays )
counts_plottable = np.transpose( counts_plottable )


fig = pl.figure()
ax = fig.add_subplot(111) ## 2 row, 1 column, first plot
thing = ax.imshow(counts_plottable, cmap=cm.hot, aspect="auto", origin='lower',
                  interpolation='bicubic' )#,
#        norm = colors.Normalize(vmin = 0.0, vmax = 1.0, clip = False))
#fig.colorbar(thing)

if options.title:
    pl.title("Phylogenetic Depth Over Time - %s" % options.title)
else:
    pl.title("Phylogenetic Depth Over Time")
pl.ylabel("Phylogenetic Depth")
pl.xlabel("Update")

#ax2 = fig.add_subplot(212)
#ax2.plot( sum_norm_plottable )
#pl.ylim(0,1)

#pl.ylabel("Mean Entropy")
#pl.xlabel("Update")

pl.xlim(0, len(count_arrays)-1)

xlocs, xlabels = pl.xticks()
xmodlabels = []
xmodlocs = []
for i in range(0, len(xlocs)):
    xmodlabels.append(int(xlocs[i]) * 50 )
    xmodlocs.append( xlocs[i] )
pl.xticks( xmodlocs, xmodlabels )

if options.show:
    pl.show()

pl.savefig(outfile)

