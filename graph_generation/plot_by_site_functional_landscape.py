# Plot the functional mutation landscape histogram against the ancestor's task map.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
import matplotlib.pyplot as pl
import matplotlib.cm as cm
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile histogram.csv task_map_colors.csv

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Supplemental Graph Title")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 3:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters
histogram_file = args[1]
task_map_colors_file = args[2]

outfile = args[0]

## read the histogram file
if histogram_file[-3:] == ".gz":
    fd = gzip.open(histogram_file)
else:
    fd = open(histogram_file)

histogram = []
for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue
#    print "HAI"
#    print line

    line = line.split(',')
    line = [float(bit) for bit in line]

    histogram.extend( line )

#    print line

fd.close()

## read the task_map colors file
if task_map_colors_file[-3:] == ".gz":
    fd = gzip.open(task_map_colors_file)
else:
    fd = open(task_map_colors_file)

task_map_colors = []
for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    line = line.split('(')[1:] ## skip the one prior to the opening (

    for bit in line:
        bit = bit.split(')')[0]

        pieces = bit.split(',')
#        print pieces
        pieces = [ float(val) for val in pieces ]

        task_map_colors.append( (pieces[0],pieces[1],pieces[2],pieces[3]) )
fd.close()

#print task_map_colors

### plot the thing

fig = pl.figure()
ax = fig.add_subplot(111) ## 2 row, 1 column, first plot

width = 0.95
indices = np.arange( len(histogram) )


#print histogram
#print len(histogram)
#print indices

histo = ax.bar( indices, histogram, width )
pl.xlim( 0, len(histogram) )
#thing = ax.imshow(all_entropies_tp, cmap=cm.jet, interpolation='nearest', aspect="auto", 
#        norm = colors.Normalize(vmin = 0.0, vmax = 1.0, clip = False))

if options.title:
    pl.title("Functional Mutation Landscape\n%s" % options.title) 
else:
    pl.title("Functional Mutation Landscape") 
pl.ylabel("Mutations")
pl.xticks( [], [] )

## try this out.
divider = make_axes_locatable( ax )
ax2 = divider.append_axes("bottom", 0.3, pad=0.1)

ax2.imshow([task_map_colors],aspect="auto", interpolation='nearest')
#ax2.plot( sum_norm_plottable )
#pl.ylim(0,1)

#pl.ylabel("Mean Entropy")
pl.yticks( [], [] )
pl.xlabel("Site Functions")


#xlocs, xlabels = pl.xticks()
#xmodlabels = []
#xmodlocs = []
#for i in range(0, len(xlocs)):
#    xmodlabels.append( int(xlocs[i]) * 50 )
#    xmodlocs.append(xlocs[i] )
#pl.xticks( xmodlocs, xmodlabels )

pl.savefig(outfile)


