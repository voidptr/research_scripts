# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
#import pylab as pl
import matplotlib.pyplot as pl
import matplotlib.cm as cm
import matplotlib.colors as colors
from mpl_toolkits.axes_grid1 import make_axes_locatable

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile by_site_entropy.csv

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-t", "--title", dest="title", type="string",
                  help="Supplemental Graph Title")
parser.add_option("-x", "--xlabel", dest="xlabel", type="string", 
                  help="X-axis Label")
parser.add_option("--ylabel1", dest="ylabel1", type="string", 
                  help="Y-axis Label - top")
parser.add_option("--ylabel2", dest="ylabel2", type="string", 
                  help="Y-axis Label - bottom")                  
parser.add_option("--xsize", dest="xsize", type="int", 
                  help="size in X dimension in px")
parser.add_option("--ysize", dest="ysize", type="int", 
                  help="size in Y dimension in px")                  
parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

### Fetch Parameters
inputfilename = args[1]

outfile = args[0]

## regular defaults
if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)


## read the file
mean_fitnesses = []
max_fitnesses = []
all_entropies = []

line_ct = 0
for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    line = line.split(',')

    line = [float(bit) for bit in line]


    if line_ct == 1:
        mean_fitnesses = line
    elif line_ct == 2:
        max_fitnesses = line
    else:
        all_entropies.append( line )
        #print all_entropies[-1]

    line_ct += 1


### plot the thing
sum_normalized_entropy = [ sum(entropies)/float(len(entropies)) for entropies in all_entropies ]
sum_norm_plottable = np.array( sum_normalized_entropy )

##transpose
all_entropies_tp = zip(*all_entropies)

ent_plottable = np.array( all_entropies )
ent_plottable = np.transpose( ent_plottable )


if (options.xsize and options.ysize):
    my_dpi = 300
    fig = pl.figure(figsize=(options.xsize/my_dpi, options.ysize/my_dpi), dpi=my_dpi)
else:
    fig = pl.figure()
    
ax = fig.add_subplot(111) ## 2 row, 1 column, first plot
#ax.set_adjustable('box')
#ax.set_aspect('auto')
#ax.imshow(ent_plottable, cmap=cm.jet, interpolation='nearest')
thing = ax.imshow(all_entropies_tp, cmap=cm.jet, interpolation='nearest', aspect="auto",
        norm = colors.Normalize(vmin = 0.0, vmax = 1.0, clip = False))
#fig.colorbar(thing)

if options.title:
    pl.title(options.title)
if options.ylabel1:
    pl.ylabel( options.ylabel1 )
pl.xticks( [], [] )

#pl.ylabel("Site")


#pl.xlabel("Update")

## try this out.
divider = make_axes_locatable( ax )
ax_cb = divider.append_axes("right", 0.1, pad=0.1)

ax2 = divider.append_axes("bottom", 0.6, pad=0.2)

fig.colorbar(thing, cax=ax_cb)


#ax2 = fig.add_subplot(212)
ax2.plot( sum_norm_plottable )
pl.ylim(0,1)

if options.ylabel2:
    pl.ylabel( options.ylabel2 )
if options.xlabel:
    pl.xlabel( options.xlabel )

ylocs, ylabels = pl.yticks()
ymodlabels = [0.0, " ", 0.5, " ", 1.0]
ymodlocs = [0, 0.25, 0.5, 0.75, 1]

#for i in range(0, len(ylocs)):
#    
#    ymodlocs.append( ylocs[i] )
#    if i%2 == 0:
#        ymodlabels.append(ylocs[i])
#    else:
#        ymodlabels.append(" ")
#    #xmodlabels.append(int(xlocs[i]) * 50 )
pl.yticks( ymodlocs, ymodlabels )




#ax2 = fig.add_subplot(212) ## 2 row, 1 column, second plot
#fits_plottable = np.array( [ mean_fitnesses, max_fitnesses ] )
#ax2.plot( fits_plottable )

xlocs, xlabels = pl.xticks()
xmodlabels = []
xmodlocs = []
for i in range(0, len(xlocs)):
    xmodlocs.append( xlocs[i] )
    if i == 0:
        xmodlabels.append(int(xlocs[i]))
    else:
        xmodlabels.append(str(int(xlocs[i]*50)/1000) + "k")
pl.xticks( xmodlocs, xmodlabels )

if options.show:
    pl.show()

#pl.savefig(outfile)
pl.savefig(outfile, bbox_inches='tight', dpi=(my_dpi))


