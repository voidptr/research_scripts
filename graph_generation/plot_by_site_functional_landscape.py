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

    line = line.split(',')
    line = [float(bit) for bit in line]

    histogram.extend( line )


fd.close()

## read the task_map colors file
if task_map_colors_file[-3:] == ".gz":
    fd = gzip.open(task_map_colors_file)
else:
    fd = open(task_map_colors_file)

task_map = []
for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    line = line.split(',') 

    task_map.append( line )
fd.close()

############# plot the thing

## define the colors and the mapping for the map task
class Colors:
    Black = (0.0, 0.0, 0.0, 1.0)
    Purple = (0.55, 0.0, 0.55, 1.0)
    Blue = (0.20, 0.49, 0.95, 1.0)
    Green = (0.0, 0.7, 0.0, 1.0)
    Yellow = (0.9, 0.9, 0.0, 1.0)
    Orange = (0.93, 0.67, 0.13, 1.0)
    Red = (0.95, 0, 0.0, 1.0)
    DarkPink = (0.86, 0.62, 0.65, 1.0)
    DarkGray = (0.65, 0.65, 0.65, 1.0)
    Gray = (0.75, 0.75, 0.75, 1.0)
    LightGray = (0.85, 0.85, 0.85, 1.0)
    White = (1.0, 1.0, 1.0, 1.0)
    LightPurple = (0.8, 0.7, 0.8, 1.0) ## degenerate site
    LightBlue = (0.7, 0.7, 0.8, 1.0) ## degenerate site
    LightPink = (0.8, 0.7, 0.7, 1.0) ## degenerate site
    TransparentGray = (0.75, 0.75, 0.75, 0.5)
    Default = (0.7, 0.53, 0.5, 1.0) ## pukey brown

#### <-- See extract_task_mappings.py for the actual meanings.
ColorsMapping = [    
    Colors.Default, ## this is unused -- an error code
    Colors.Gray, ## KO.GainBB_GainFL -- neutral
    Colors.Gray, ## KO.GainBB_NeutFL -- neutral
    Colors.Blue, #Colors.Green, ## fluctuating site, but you also gain BB, so a little different
    Colors.Gray, ## KO.NeutBB_GainFL -- neutral
    Colors.Gray, ## KO.NeutBB_NeutFL -- neutral
    Colors.Blue, ## fluctuating only site 
    Colors.Red,  #Colors.Orange, ## backbone site, but you gain FL, so interesting 
    Colors.Red,  ## backbone only site 
    Colors.Purple, ## both site 
    Colors.Black,  ## knocking out this site kills you -- KnockOuts.Dead
    Colors.LightGray, ## empty -- KnockOuts.Empty -- WEIRD -- 11
    Colors.LightBlue, ## degenerate fluctuating site -- KODegen.FLNeut
    Colors.LightPink, ## degenerate backbone site -- KODegen.BBNeut
    Colors.LightPurple, ## degenerate both site -- KODegen.BBFLNeut
    Colors.Yellow, ## Point Mutation -- 15
    Colors.Green, ## Insertion -- 16
    Colors.Orange, ## Deletion -- 17
    Colors.DarkPink, #Colors.TransparentGray,## No Mutation -- 18
    Colors.White, ## Phases.Reward -- 19
    Colors.Red, ## Phases.NoReward
    Colors.Black] ## Phases.Border -- 21

colored_maps = []
for input_map in task_map:
    colored_map = []
    for site in input_map:
        colored_map.append( ColorsMapping[ site ] )
    colored_maps.append( colored_map )


## plot it
fig = pl.figure()
ax = fig.add_subplot(111) ## 2 row, 1 column, first plot

width = 0.95
indices = np.arange( len(histogram) )


histo = ax.bar( indices, histogram, width )
pl.xlim( 0, len(histogram) )

if options.title:
    pl.title("Functional Mutation Landscape\n%s" % options.title) 
else:
    pl.title("Functional Mutation Landscape") 
pl.ylabel("Mutations")
pl.xticks( [], [] )

## try this out.
divider = make_axes_locatable( ax )
ax2 = divider.append_axes("bottom", 0.3, pad=0.1)

ax2.imshow(colored_maps,aspect="auto", interpolation='nearest')
pl.yticks( [], [] )
pl.xlabel("Site Functions")



pl.savefig(outfile)


