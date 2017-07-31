# Plot from CSV(s)

# Written in Python 2.7
# RCK
# 1-10-12

# Rewritten to suck less
# RCK
# 5-30-12

import matplotlib
matplotlib.use('Agg')

import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser
import os
import sys

# Set up options
usage = """
 %prog [options] outfile infile1 [infile2]

Permitted types for outfile are png, pdf, ps, eps, and svg
Input files must be grouped by treatment group, and sorted
by desired display order"""
parser = OptionParser(usage)
## version
parser.add_option("--version", action = "store_true", dest = "display_version",
                  default = False, help = "Output the version message and exit")
## output
parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")

## data input
parser.add_option("-d", "--delimiter", dest="delimiter", type="string",
                  help="Datafile delimiter")
parser.add_option("--data_members", dest="member_count", type="int",
                  help="Number of Components from a given data source (treatment)")
parser.add_option("--start_at", dest="start_at", type="int",
                  help="Only start plotting from datapoint <start_at>")
parser.add_option("--end_at", dest="end_at", type="int",
                  help="Stop plotting from datapoint <end_at>")
parser.add_option("--has_header", dest="has_header", action="store_true", default = False, help = "Contains header line, so ignore it")

## basic display
parser.add_option("-o", "--mean", action="store_true", dest = "mean",
                  default = True, help = "calculate and display mean")
parser.add_option("-a", "--all", action="store_true", dest = "all",
                  default = False, help = "display all lines of a source")
parser.add_option("--error", dest="calculate_error", action="store_true", default = False,
                  help="include error bars - error values will be calculated from data using bootstrap")

## legends and labels
parser.add_option("-l", "--legend", dest="legend", type="string", 
                  help = "include a legend, (values)")
parser.add_option("-x", "--xlabel", dest="xlabel", type="string", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="ylabel", type="string", 
                  help="Y-axis Label")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Graph Title")
parser.add_option("--include_chevrons", dest="include_chevrons", type="string", 
                  help="Include line marker glyphs in addition to color")

## visual mods
parser.add_option("--xtick_multiplier", dest="xtick_multiplier", type="int", 
                  help="X-axis Tick Multipliers")
parser.add_option("--alt_axis", dest="alt_axis", type="int",
                  help="Use an alternative axis for the Nth data source")
parser.add_option("-w", "--ylabel_alt_axis", dest="y_label_alt_axis", type="string", 
                  help="Alternative Y-axis Label")
parser.add_option("--ylim_max", dest="ylim_max", type="float",
                  help="Set the ylim max")
parser.add_option("--ylim_min", dest="ylim_min", type="float",
                  help="Set the ylim min")
parser.add_option("--xlim_max", dest="xlim_max", type="float",
                  help="Set the xlim max")
parser.add_option("--xlim_mix", dest="xlim_min", type="float",
                  help="Set the xlim min")
parser.add_option("--ylog", action="store_true", dest="ylog",
                  default=False, help="Display the Y-axis on a logarithmic scale")
## fetch the args
(options, args) = parser.parse_args()

## handle version
if options.display_version:
    print sys.argv[0]
    print "Version: ", os.popen("git describe --tags").read()
    exit(0)

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

if options.member_count:
    input_file_count = len(args[1:])
    if input_file_count % options.member_count > 0:
        parser.error("The number of input files provided must be a multiple of member count") 

## parameter defaults -- do this here because optparse seems to fuck this up
if not options.member_count:
    options.member_count = 1

if not options.delimiter:
    options.delimiter = ','

## output file name
outfilename = args[0]

## input filenames
inputfilenames = args[1:]


## BOOT STRAP HELPER - mean error
def Quantile(data, q, precision=1.0):
    """
    Returns the q'th percentile of the distribution given in the argument
    'data'. Uses the 'precision' parameter to control the noise level.
    """
    N, bins = np.histogram(data, bins=precision*np.sqrt(len(data)))
    norm_cumul = 1.0*N.cumsum() / len(data)

    return bins[norm_cumul > q][0]

def bootstrap_error( data ):
    x = np.array((data))
    X = [] ## estimates
    mean = np.mean(x)
    for xx in xrange(1000): ## do this 1000 times
        X.append( np.mean( x[np.random.randint(len(x),size=len(x))] ) )

    conf = 0.95
    plower = (1-conf)/2.0
    pupper = 1-plower

    lower_ci, upper_ci = (Quantile(X, plower), Quantile(X, pupper))
    diff_upper = upper_ci - mean
    diff_lower = mean - lower_ci

    return max( diff_upper, diff_lower )
## END BOOT STRAP HELPERS


## read the input data
data = []
for inputfilename in inputfilenames:

    data_2d_array = [] ## each row is run, each column is a datapoint in that run
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        if options.has_header: ## the first line is a header line. skip it.
            options.has_header = False ## clear it
            continue

        line = line.split(',') ## break the line up on commas
        line = [val if val is not "nan" else "0" for val in line] # replace "nan" with 0

        ## handle data limiting
        if options.end_at:
            line = line[:options.end_at+1] ## chop off whatever.

        if options.start_at:
            line = line[options.start_at:] ## chop off whatever.

        data_2d_array.append( line )
        
    fd.close()

    data.append( data_2d_array )

class Colors:
    Black = (0, 0, 0)
    DarkSeafoam = (0, 0.285, 0.285)
    LightPink = (1, 0.71, 0.465)

    Purple = (0.285, 0, 0.57)
    Blue = (0, 0.426, 0.855)
    Violet = (0.71, 0.426, 1)
    SkyBlue = (0.426, 0.71, 1)
    LightBlue = (0.71, 0.855, 1)

    Rust = (0.57, 0, 0)
    Brown = (0.57, 0.285, 0)
    Orange = (0.855, 0.816, 0)
    NeonGreen = (0.14, 1, 0.14)
    Yellow = (1, 1, 0.426)

    def Transparent(color, level):
        return (color[0], color[1], color[2], level) 
 
median_colors = [Colors.Black, Colors.Purple, Colors.Blue, Colors.Violet, Colors.Rust, Colors.Orange, Colors.DarkSeafoam, Colors.LightPink]
data_colors = [Colors.Transparent(val, 0.5) for val in median_colors]
edge_colors = data_colors 

line_styles = ['-','--', ':', '-.'] ## a max of four different lines, sigh.
line_markers = [None]
if options.include_chevrons:
    line_markers = ['*','p','d','o','v','x','.']
artists = []

## start plotting
fig = pl.figure()
axes = [ fig.add_subplot(111) ]

if options.alt_axis:
    axes.append( axes[0].twinx() )

## figure out the proper color, marker, and axis order per file
color_indexes = []
style_indexes = []
marker_indexes = []
axis_indexes = []
for i in range(0, len(data)):
    color_indexes.append( (i / options.member_count) % len(data_colors) )
    marker_indexes.append( (i / options.member_count) % len(line_markers) )
    style_indexes.append( (i % options.member_count) % len(line_styles) )

    if options.alt_axis == (i / options.member_count)+1:
        axis_indexes.append( 1 )
    else:
        axis_indexes.append( 0 )

## plot all lines 
if options.all: ## plot all the lines -- all the same damned color and marker in a file
    for (data_2d_array, file_index) in zip(data, range(0, len(data))): ## one file at a time
        for line in data_2d_array: ## plot each line separately so we can set color and markers
            plottable = np.add( [ float(val) for val in line ], 0 )
            plottable = np.transpose(plottable)
            pl.plot( plottable, marker=line_markers[ marker_indexes[file_index] ], 
                                color=data_colors[ color_indexes[file_index] ],
                                linestyle=line_styles[ style_indexes[ file_index ]])

## plot the mean (with or without error)
if options.mean:

    ## calculate the mean (and error) for each file
    mean_data_array = []
    error_data_array = []
    for data_2d_array in data:

        ## transpose so that each array is now all the values for a given sample
        transposed = zip(*data_2d_array)
        cleaned = []
        for sample_array in transposed:
            cleaned.append( [ float( val ) for val in sample_array if val != "nan" ] ) ## filter out nan's and convert to floating point 

        means = []
        for sample in cleaned:
            means.append( np.mean( sample ) )
        mean_data_array.append( means )

        if options.calculate_error:
            errors = []
            for sample in cleaned:
                errors.append( bootstrap_error( sample ) )
            error_data_array.append( errors )
            
    ## now, plot the things
    for i in range(0, len(mean_data_array)):

        if options.calculate_error:
            data_plus_error = [ (point + error) for (point, error) in zip( mean_data_array[i], error_data_array[i] ) ]
            data_minus_error = [ (point - error) for (point, error) in zip( mean_data_array[i], error_data_array[i] ) ]

            plottable_error_top = np.add( data_plus_error, 0 )
            plottable_error_top = np.transpose(plottable_error_top)

            plottable_error_bottom = np.add( data_minus_error, 0 )
            plottable_error_bottom = np.transpose(plottable_error_bottom)
            
            xes = range(0, len(plottable_error_bottom))
            axes[ axis_indexes[i] ].fill_between( xes, plottable_error_top, plottable_error_bottom, 
                                                  facecolor=data_colors[ color_indexes[i] ], 
                                                  edgecolor=data_colors[ color_indexes[i] ] )

        plottable = np.add( mean_data_array[i], 0 )
        plottable = np.transpose( plottable )

        axes[ axis_indexes[i] ].plot( plottable, 
                                      marker=line_markers[marker_indexes[i]], 
                                      color=median_colors[color_indexes[i]],
                                      linestyle=line_styles[style_indexes[i]]) 

### final plot tweaks
#axes[0].plot( [0] ) ## add one so it displays 0 at least!

## set the labels and titles
if options.title:
    pl.title( options.title )

if options.xlabel:
    axes[0].set_xlabel( options.xlabel )

if options.ylabel:
    axes[0].set_ylabel( options.ylabel )

if options.y_label_alt_axis:
    axes[1].set_ylabel( options.y_label_alt_axis )

if options.ylog:
    axes[0].set_yscale('log')

## set the ylim/xlim
ylim_min, ylim_max = pl.ylim()
xlim_min, xlim_max = pl.xlim()

if options.ylim_min:
    ylim_min = options.ylim_min
if options.ylim_max:
    ylim_max = options.ylim_max
if options.xlim_min:
    xlim_min = options.xlim_min
if options.xlim_max:
    xlim_max = options.xlim_max

pl.ylim(ylim_min,ylim_max)
pl.xlim(xlim_min,xlim_max)

## reset the ticks per a provided multiplier
if options.xtick_multiplier:

    interval = int(options.xtick_multiplier)   
    xlocs, xlabels = pl.xticks()

    xmodlabels = []
    xmodlocs = []
    for i in range(0, len(xlocs)):
        xmodlabels.append( int(xlocs[i] * interval) )
        xmodlocs.append( xlocs[i] )

    pl.xticks( xmodlocs, xmodlabels )

def proxy_artist( color, marker, style ):
    p = pl.Line2D([0,0], [0,1], color=color, marker=marker, linestyle=style)
    return p

## set the legend
if options.legend:
    legend_labels = options.legend.split(",")

    if len(legend_labels) != len(data):
        ## raise some sort of warning TODO
        print "LEGEND LABELS MUST MATCH DATA FILE COUNT"
    else:

        proxies = []
        for i in range(0, len(data)): ## set it by file
            proxies.append( proxy_artist( median_colors[color_indexes[i]], line_markers[marker_indexes[i]], line_styles[style_indexes[i]] ) )

        pl.legend( proxies, legend_labels, bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0. )
        leg = pl.gca().get_legend()
        ltext = leg.get_texts()
        pl.setp( ltext, fontsize='small')

        l,b,w,h = pl.axes().get_position().bounds
        pl.axes().set_position([0.1,b,w*.78,h])

if options.show:
    pl.show()

pl.savefig(outfilename)
