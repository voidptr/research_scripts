#!/usr/bin/python

# Draw the placements of where the tasks are

# Written in Python 2.7
# RCK
# 03-21-12

import os
import glob
import gzip
from optparse import OptionParser

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Set up options
usage = """usage: %prog [options] outfile.png lineage_map_file.csv

"""
parser = OptionParser(usage)
parser.add_option("-t", "--trim", action = "store_true", dest = "trim_whitespace",
                  default = False, help = "trim the whitespace")

parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose mode")
parser.add_option("-d", "--debug", action = "store_true", dest = "debug_messages",
                  default = False, help = "debug mode")

parser.add_option("--title", dest = "title", type="string",
                  help = "Supplemental Title")

parser.add_option("--legend", dest="legend", action="store_true", default = False, help = "Show the legend.")

parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")

parser.add_option("--horizontal", action = "store_true", dest = "horizontal",
                  default = False, help = "horizontal view mode")
parser.add_option("--xsize", dest="xsize", type="int", 
                  help="size in X dimension in px")
parser.add_option("--ysize", dest="ysize", type="int", 
                  help="size in Y dimension in px")   
parser.add_option("--xlabel", dest = "xlabel", type="string",
                  help = "xlabel")   
parser.add_option("--ylabel", dest = "ylabel", type="string",
                  help = "ylabel")                   

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

outfile = args[0]
lineage_map_file = args[1]

class Colors:
    Black = (0.0, 0.0, 0.0, 1.0)
    Purple = (0.55, 0.0, 0.55, 1.0)
    Blue = (0, 0, 0.95, 1.0)
    Green = (0.0, 0.7, 0.0, 1.0)
    Yellow = (0.9, 0.9, 0.0, 1.0)
    Orange = (0.93, 0.67, 0.13, 1.0)
    Red = (0.95, 0, 0.0, 1.0)
    DarkPink = (0.86, 0.62, 0.65, 1.0)
    DarkGray = (0.65, 0.65, 0.65, 1.0)
    Gray = (0.75, 0.75, 0.75, 1.0)
    LightGray = (0.85, 0.85, 0.85, 1.0)
    White = (1.0, 1.0, 1.0, 1.0)
    LightPurple = (0.57, 0.43, 0.85, 1.0) ## degenerate site
    LightBlue = (0.39, 0.58, 0.92, 1.0) ## degenerate site
    LightPink = (0.91, 0.59, 0.47, 1.0) ## degenerate site
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


######### load in the lineage file
maps = []
if lineage_map_file[-3:] == ".gz":
    fp = gzip.open(lineage_map_file)
else:
    fp = open(lineage_map_file)

for line in fp:
    line = line.strip()
    if len(line) == 0 or line[0] == '#': ## skip it if it's not format
        continue

    line = line.split(',')
    line = [ int(val) for val in line ]
    maps.append( line )

fp.close()

## apply the colors
colored_maps = []
for input_map in maps:
    colored_map = []
    for site in input_map:
        colored_map.append( ColorsMapping[ site ] )
    colored_maps.append( colored_map )


# [0 [0(A), 1(B), 2(C)],
#  1 [0(A), 1(B), 2(C)],
#  2 [0(A), 1(B), 2(C)]
#  3 [0(A), 1(B), 2(C)]]
#
#[ [A, A, A, A]]
#

horizontal_maps = []    
if options.horizontal:
    for x in range(len(colored_maps[0])):
        horizontal_maps.append([])
        for y in range(len(colored_maps)):
            horizontal_maps[x].append(colored_maps[y][x])
            
    #horizontal_maps.reverse()        
    
    colored_maps = horizontal_maps            

######### NOW GENERATE THE PLOT(S) ###############
def proxy_artist( color ):
    p = plt.Rectangle((0,0), 1,1, fc=color)
    return p

## generate the plot
if (options.xsize and options.ysize):
    my_dpi = 300.0
    fig = plt.figure(figsize=(options.xsize/my_dpi, options.ysize/my_dpi), dpi=my_dpi)
else:
    fig = plt.figure()

if options.trim_whitespace:
    ax = fig.add_axes((0,0,1,1))
    ax.set_axis_off()
    ax.imshow(colored_maps, interpolation='nearest')

    plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
    plt.savefig(outfile, pad_inches=0)

    ## trim the fat
    os.system('convert '+outfile+' -bordercolor white -border 1x1 -trim +repage -alpha off +dither -colors 32 PNG8:'+filename)

else:
    ax = fig.add_subplot(111) ## 1 row, 1 column, first plot
    #ax.set_aspect("auto")
    ax.imshow(colored_maps, interpolation='nearest', aspect="auto")#, aspect=1) ## now it should spread wide.


    if options.ylabel:
        ax.set_ylabel(options.ylabel)
    if options.xlabel:
        ax.set_xlabel(options.xlabel)
    if options.title:
        plt.title( options.title ) ## set it above the current center. Maybe it will shift properly. :/

    ## apply the divider
    divider = make_axes_locatable( ax )
    

    ax_leg = divider.append_axes("right", 2, pad=0.1 )
    
    ## turn off the frame
    ax_leg.set_frame_on(False)
    ax_leg.axes.get_yaxis().set_visible(False)
    ax_leg.axes.get_xaxis().set_visible(False)

    #plt.gca().invert_xaxis()
    
    ## prepare the proxy artists for the legends
    sites = [ proxy_artist(Colors.Red),
              proxy_artist(Colors.Blue),
              proxy_artist(Colors.Purple),
              proxy_artist(Colors.LightPink),
              proxy_artist(Colors.LightBlue),
              proxy_artist(Colors.LightPurple),
              proxy_artist(Colors.Black)]
    phases = [proxy_artist(Colors.Gray),
              proxy_artist(Colors.DarkGray)]

    mutations = [proxy_artist(Colors.Yellow),
                 proxy_artist(Colors.Green),
                 proxy_artist(Colors.Orange)]

    sites_labels = [ 'XOR', 'EQU', 'XOR & EQU',
                     'Vestig. XOR', 'Vestig. EQU', 'Vestig. Both', 'Lethal' ]
    phases_labels = ['Reward Phase', 'No Reward Phase' ]
    mutations_labels = ['Point Mutation', 'Insertion', 'Deletion' ]

    if options.legend:
        ## apply the legends
        l1 = ax_leg.legend(sites, sites_labels, title="Sites", bbox_to_anchor=(-0.01, 1), loc=2, borderaxespad=0.0)
        leg = plt.gca().get_legend()
        ltext = leg.get_texts()
        plt.setp( ltext, fontsize='small')

    #    l2 = ax_leg.legend(phases, phases_labels, title="Phases", bbox_to_anchor=(0, .53), loc=2, borderaxespad=0.)
    #    leg = plt.gca().get_legend()
    #    ltext = leg.get_texts()
    #    plt.setp( ltext, fontsize='small')

        #l3 = ax_leg.legend(mutations, mutations_labels, title="Mutations", bbox_to_anchor=(0, .34), loc=2, borderaxespad=0.)
   #     l3 = ax_leg.legend(mutations, mutations_labels, title="Mutations", bbox_to_anchor=(0, .53), loc=2, borderaxespad=0.)
   #     leg = plt.gca().get_legend()
   #     ltext = leg.get_texts()
   #     plt.setp( ltext, fontsize='small')

        plt.gca().add_artist(l1)
#    plt.gca().add_artist(l2)

    if options.show:
        plt.show()

    #plt.tight_layout()
    ## save
    #plt.savefig(outfile, dpi=(300)) #figsize=(options.xsize/my_dpi, options.ysize/my_dpi), dpi=my_dpi
    #plt.savefig(outfile, bbox_inches='tight')#, dpi=(300)
    #pl.savefig(outfile)
    plt.savefig(outfile, bbox_inches='tight', dpi=(my_dpi))


