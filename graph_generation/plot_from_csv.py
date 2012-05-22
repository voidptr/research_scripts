# Plot from a CSV 

# Written in Python 2.7
# RCK
# 1-10-12


import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile infile1 [infile2]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-a", "--all", action="store_true", dest = "all",
                  default = False, help = "display all lines of a source")
parser.add_option("-m", "--medianplus", action="store_true", dest = "median",
                  default = False, help = "calculate and display median plus the original lines")
parser.add_option("-o", "--medianonly", action="store_true", dest = "median_only",
                  default = False, help = "calculate and display median ONLY")
parser.add_option("-l", "--legend", type="string", dest = "legend",
                  help = "include a legend, (values)")
parser.add_option("-x", "--xlabel", dest="x_label", type="string", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="y_label", type="string", 
                  help="Y-axis Label")
parser.add_option("--x_tick_intervals", dest="x_tick_intervals", type="string", 
                  help="X-axis Tick Intervals")
parser.add_option("-w", "--ylabel_alt_axis", dest="y_label_alt_axis", type="string", 
                  help="Alternative Y-axis Label")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Graph Title")
parser.add_option("--data_sources", dest="source_count", type="int",
                  help="Number of Sources Per Treatment (the number of lines to be drawn in a treatment)")
parser.add_option("--alt_axis", dest="alt_axis", type="int",
                  help="Use an alternative axis for the Nth data source")
parser.add_option("--include_error", dest="include_error", action="store_true", default = False,
                  help="include error bars - each data file must have a corresponding std error file")
parser.add_option("--calculate_error", dest="calculate_error", action="store_true", default = False,
                  help="include error bars - error values will be calculated from data")
parser.add_option("--ylim_max", dest="ylim_max", type="float",
                  help="Set the max ylim")
parser.add_option("--ylim_min", dest="ylim_min", type="float",
                  help="Set the min ylim")
parser.add_option("--xlim_max", dest="xlim_max", type="float",
                  help="Set the max xlim")
parser.add_option("--show_phase", dest="show_phase", type="int",
                  help="Show the phase, at interval")
parser.add_option("--start_at", dest="start_at", type="int",
                  help="Only start plotting from datapoint <start_at>")
parser.add_option("--has_header", dest="has_header", action="store_true", default = False, help = "Contains header line, so ignore it")
parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")
if options.median_only and options.median:
    parser.error("-m and -o are mutually exclusive")
if options.alt_axis:
    if options.source_count:
        if options.alt_axis > options.source_count:
            parser.error("--alt_axis must correspond with a source.")
    else:
        if options.alt_axis > len(args[1:]):
            parser.error("--alt_axis must correspond with a source.")
if options.source_count:
    if len(args[1:]) % options.source_count > 0:
        parser.error("The number of input files provided must be a multiple of source count") 

if options.show_phase and not options.x_tick_intervals:
    parser.error("Phases require x-tick intervals being defined.")

## output file name
outfilename = args[0]

## input filenames
inputfilenames = args[1:]

## source and treatment counts, if not provided
if not options.source_count:
    options.source_count = 1

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


data = []
for inputfilename in inputfilenames:

    data_2d_array = [] ## each row is run, each column is a datapoint in that run
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    line_ct = 0
    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        if line_ct == 0 and options.has_header: ## the first line is a header line. skip it.
            line_ct += 1
            continue

        line = line.split(',') ## break the line up on commas    

        if options.start_at:
            line = line[options.start_at:] ## chop off whatever.

        data_2d_array.append( line )

        line_ct += 1
        
    fd.close()

    data.append( data_2d_array )

class Colors:
    Black = (0.0, 0.0, 0.0, 1.0)
    TBlack = (0,0,0,0.2)
    DarkGray = (0.65, 0.65, 0.65, 1.0)
    Gray = (0.75, 0.75, 0.75, 1.0)
    TGray = (0.75, 0.75, 0.75, 1.0)
    LightGray = (0.85, 0.85, 0.85, 1.0)
    TLightGray = (0.85, 0.85, 0.85, 0.5)
    VeryLightGray = (0.9, 0.9, 0.9, 1.0)
    White = (1.0, 1.0, 1.0, 1.0)
    Transparent = (0, 0, 0, 0)


    Purple = (0.55, 0.0, 0.55, 1.0)
    TPurple = (0.55, 0.0, 0.55, 0.5)
    LightPurple = (0.8, 0.7, 0.8, 1.0) 
    TLightPurple = (0.8, 0.7, 0.8, 0.5) 

    Blue = (0.20, 0.49, 0.95, 1.0)
    TBlue = (0.20, 0.49, 0.95, 0.5)
    LightBlue = (0.6, 0.7, 0.95, 1.0)
    TLightBlue = (0.6, 0.7, 0.95, 0.5)

    BlueGreen = (0.0, 1.0, 1.0, 1.0)
    TBlueGreen = (0.0, 1.0, 1.0, 0.5)
    LightBlueGreen = (0.8, 1.0, 0.8, 1.0)
    TLightBlueGreen = (0.8, 1.0, 0.8, 0.5)

    Green = (0.0, 0.7, 0.0, 1.0)
    TGreen = (0.0, 0.7, 0.0, 0.5)
    LightGreen = (0.8, 1.0, 0.8, 1.0)
    TLightGreen = (0.8, 1.0, 0.8, 0.5)

    Yellow = (0.9, 0.9, 0.0, 1.0)   

    Orange = (0.93, 0.67, 0.13, 1.0)

    OrangeRed = (1.0, 0.7, 0.0, 1.0)
    TOrangeRed = (1.0, 0.7, 0.0, 0.5)
    LightOrangeRed = (0.9, 0.7, 0.6, 1.0)
    TLightOrangeRed = (0.9, 0.7, 0.6, 0.5)

    Red = (0.95, 0, 0.0, 1.0)
    LightPink = (0.8, 0.7, 0.7, 1.0)
    TLightPink = (0.8, 0.7, 0.7, 0.5)
    DarkPink = (0.86, 0.62, 0.65, 1.0)

    TransparentGray = (0.75, 0.75, 0.75, 0.5)
    Default = (0.0, 0.0, 0.0, 1.0)

    

## a max of four treatments (black, blue, yellow, green)
median_colors = [ Colors.Black,  Colors.Blue ,      Colors.OrangeRed,       Colors.Green,       Colors.BlueGreen,       Colors.Purple ]
data_colors =   [ Colors.TGray,  Colors.TLightBlue, Colors.TLightOrangeRed, Colors.TLightGreen, Colors.TLightBlueGreen, Colors.TLightPurple]
edge_colors =   [ Colors.TBlack, Colors.TBlue,      Colors.TOrangeRed,      Colors.TGreen,      Colors.TBlueGreen,      Colors.TPurple]


line_styles = ['-','--', ':', '-.'] ## a max of four different lines, sigh.
line_markers = ['*','p','d','o','v','x']
artists = []

fig = pl.figure()
ax1 = fig.add_subplot(111)

ax2 = None
if options.alt_axis:
    ax2 = ax1.twinx()

if options.include_error:
    if len(data) != len(error):
        print "ERROR: data set must have the same number of items as error set"
        exit(1) ## ARGH DIE 

if options.median_only:

    

    max_val = 0
    if options.ylim_max:
        max_val = options.ylim_max
    else:
        for data_2d_array in data:
            for samples in data_2d_array:
                localmax = max( [ float(val) if val != 'nan' else 0 for val in samples ] )
                if localmax > max_val and localmax != 'nan':
                    max_val = localmax

    input_count = 0
    for data_2d_array in data:
   
        median_data_array = []
        error_data_array = []
        for i in range(0, len(data_2d_array[0])):

            if options.debug_messages:
                print
                print "file: %s current_value_index: %s" % (inputfilenames[input_count], i)

                ct = 1
                for run in data_2d_array:
                    print "replicate_line: %s values_ct: %s" % (ct, len(run))
                    ct += 1

            sample_point_collection = [ float(run[i]) for run in data_2d_array if run[i] != "nan" ] ## filter out nan's
            median_data_array.append( np.mean( sample_point_collection ) )
            if options.calculate_error:
                error_data_array.append( bootstrap_error( sample_point_collection ) ) ## use bootstrap error
                #error_data_array.append( np.std( sample_point_collection ) / math.sqrt( len( sample_point_collection ) ) ) ## std and std error (parametric)

        plottable = np.add( median_data_array, 0 )
        plottable = np.transpose(plottable)

        plottable_error_top = None
        plottable_error_bottom = None
        if options.calculate_error:

            data_plus_error = [ (data + error) for (data, error) in zip( median_data_array, error_data_array ) ]
            data_minus_error = [ (data - error) for (data, error) in zip( median_data_array, error_data_array ) ]

            plottable_error_top = np.add( data_plus_error, 0 )
            plottable_error_top = np.transpose(plottable_error_top)

            plottable_error_bottom = np.add( data_minus_error, 0 )
            plottable_error_bottom = np.transpose(plottable_error_bottom)


        in_alt_axis = False      
        if options.alt_axis:
            if input_count % options.source_count == alt_axis:
                in_alt_axis = True

        axis_to_plot_on = ax1
        if in_alt_axis:
            axis_to_plot_on = ax2

        color_index = ( input_count / options.source_count ) % len( median_colors )
        line_style_index = ( input_count % options.source_count ) % len( line_styles )

        if options.debug_messages:
            print
            print input_count
            print "Treatment: " + str(color_index) + " " + str(median_colors[color_index])
            print "Source: " + str(line_style_index)

        xes = range(0, len(plottable))
        if options.show_phase and input_count == 0:
            interval = int(options.x_tick_intervals)
            phase = options.show_phase
            half_phase = phase/2

            inphase = [ ((val * interval) % phase) - half_phase > 0 if (val*interval) > phase else False for val in xes ]
            axis_to_plot_on.fill_between( xes, 0, max_val, where=inphase, facecolor=Colors.VeryLightGray, edgecolor=Colors.Transparent)

        if options.calculate_error:
            axis_to_plot_on.fill_between( xes, plottable_error_top, plottable_error_bottom, facecolor=data_colors[color_index], edgecolor=edge_colors[color_index] )


        if options.source_count > 0:
            artists.append( axis_to_plot_on.plot( plottable, color=median_colors[color_index], marker=line_markers[color_index], markevery=200, linestyle=line_styles[line_style_index]) )
        else:
            artists.append( axis_to_plot_on.plot( plottable ) )

        input_count += 1

elif options.median:
    input_count = 0

    max_val = 0
    if options.ylim_max:
        max_val = options.ylim_max
    else:
        for data_2d_array in data:
            for samples in data_2d_array:
                localmax = max( [ float(val) if val != 'nan' else 0 for val in samples ] )
                if localmax > max_val and localmax != 'nan':
                    max_val = localmax


    for data_2d_array in data:

        sanitized = data_2d_array ## clean the NANs out of the plottable, make them zeroes
        for run in sanitized:
            for i in range(0, len(run)):
                if run[i] == "nan":
                    run[i] = 0
                else:
                    run[i] = float(run[i])

        plottable = np.add( sanitized, 0 )
        plottable = np.transpose(plottable)

        in_alt_axis = False      
        if options.alt_axis:
            if input_count % options.source_count == alt_axis:
                in_alt_axis = True
        color_index = ( input_count / options.source_count ) % len( median_colors )
        line_style_index = ( input_count % options.source_count ) % len( line_styles )


        xes = range(0, len(plottable))
        if options.show_phase and input_count == 0:
            interval = int(options.x_tick_intervals)
            phase = options.show_phase
            half_phase = phase/2

            inphase = [ ((val * interval) % phase) - half_phase > 0 if (val*interval) > phase else False for val in xes ]
            ax1.fill_between( xes, 0, max_val, where=inphase, facecolor=Colors.VeryLightGray, edgecolor=Colors.Transparent)




        if in_alt_axis: ## use the alt axis
            artists.append( ax2.plot( plottable, color=data_colors[color_index], marker=line_markers[color_index], markevery=200, linestyle=line_styles[line_style_index]) )
        else:
            artists.append( ax1.plot( plottable, color=data_colors[color_index], marker=line_markers[color_index], markevery=200, linestyle=line_styles[line_style_index]) )

        median_data_array = []
        for i in range(0, len(data_2d_array[0])):
            sample_point_collection = [ float(run[i]) for run in data_2d_array if run[i] != "nan" ] ## filter out nan's
            median_data_array.append( np.mean( sample_point_collection ) )

        plottable = np.add( median_data_array, 0 )

        if in_alt_axis: ## use the alt axis
            artists.append( ax2.plot( plottable, color=median_colors[color_index], marker=line_markers[color_index], markevery=200, linestyle=line_styles[line_style_index]) )
        else:
            artists.append( ax1.plot( plottable, color=median_colors[color_index], marker=line_markers[color_index], markevery=200, linestyle=line_styles[line_style_index]) )

        input_count += 1
elif options.all:
    for data_2d_array in data:
        plottable = np.add( data_2d_array, 0 )
        plottable = np.transpose(plottable)
        pl.plot( plottable, marker=',' )

ax1.plot( [0] ) ## add one so it displays 0 at least!

ax1.set_xlabel( options.x_label )
ax1.set_ylabel( options.y_label )

if not options.ylim_min:
    options.ylim_min = 0
if not options.alt_axis and options.ylim_max:
    pl.ylim(options.ylim_min,options.ylim_max)

if options.xlim_max:
    pl.xlim(0,options.xlim_max)

if options.y_label_alt_axis:
    ax2.set_ylabel( options.y_label_alt_axis )

if options.x_tick_intervals:

    interval = int(options.x_tick_intervals)

    

    xmin, xmax = pl.xlim()

    xlocs, xlabels = pl.xticks()

    #print xmin
    #print xmax
    #print xlocs
    #print xlabels

    xmodlabels = []
    xmodlocs = []
    for i in range(0, len(xlocs)):
#        if ( xlocs[i] * interval ) >= xmin and (xlocs[i]* interval) <= xmax:
        xmodlabels.append( int(xlocs[i] * interval) )
        xmodlocs.append( xlocs[i] )

    pl.xticks( xmodlocs, xmodlabels )

def proxy_artist( color ):
    p = pl.Line2D([0,0], [0,1], color=color)
    return p

if options.legend and len(artists) > 0:

    legend_labels = options.legend.split(",")

    proxies = []
    for i in range(0, len(legend_labels)):
        proxies.append( proxy_artist( median_colors[i] ) )

#    if options.stack:
#        proxies.reverse()
#        legend_labels.reverse()

    pl.legend( proxies, legend_labels, bbox_to_anchor=(1.03, 1), loc=2, borderaxespad=0. )
    leg = pl.gca().get_legend()
    ltext = leg.get_texts()
    pl.setp( ltext, fontsize='small')

    l,b,w,h = pl.axes().get_position().bounds
    pl.axes().set_position([0.1,b,w*.78,h])




#    pl.legend( artists, labels, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0. )
#    leg = pl.gca().get_legend()
#    ltext = leg.get_texts()
#    pl.setp( ltext, fontsize='small')

#    l,b,w,h = pl.axes().get_position().bounds
#    pl.axes().set_position([0.08,b,w*.8,h])


if options.title:
    pl.title( options.title )

if options.show:
    pl.show()

pl.savefig(outfilename)
