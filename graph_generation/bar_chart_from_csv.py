# bar chart from a CSV 

# Written in Python 2.7
# RCK
# 1-10-12


import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile infile1_group1 [infile2_group1 infile3_group2 infile4_group2]

Permitted types for outfile are png, pdf, ps, eps, and svg
"""
parser = OptionParser(usage)
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print verbose messages to stdout")
                 
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

parser.add_option("--ignorenan", action="store_true",dest="ignorenan",  default=False, help = "If a line includes something that isn't a number, ignore that line.")

### grouping options
parser.add_option("--groups", dest="groups", type="int", help="The number of groups (X-ticks)") ## bars in the same group go on top of each other
parser.add_option("--xticks", dest="group_labels", type="string", 
                  help="X-axis Column Label(s) (ticks)")                 
parser.add_option("--legend", dest="legend", type="string", 
                  help="Labels to go in the legend, by colors") ## the individuals within a group
parser.add_option("--columns", dest="columns", type="string", 
                  help="If in a multi-column file, select the columns you want to work.")                 


### display options
parser.add_option("--stack", dest="stack", action = "store_true", help="Stacked Bar Chart") ## bars in the same group go on top of each other
parser.add_option("--pair", dest="pair", action = "store_true", help="Paired Bar Chart") ## bars in the same group go next to each other

parser.add_option("--show", dest="show", action="store_true", default = False, help = "Show the thing to be able to edit the image.")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## labels to use for the columns
group_labels = []
if options.group_labels:
    group_labels = options.group_labels.split(",")

legend_labels = []
if options.legend:
    legend_labels = options.legend.split(",")

columns = []
if options.columns:
    columns = [ (int(val) - 1) for val in options.columns.split(",") ]

if options.stack and options.pair: ## mutually exclusive
    parser.error("--stack and --pair are mutually exclusive. Pick one")

if options.groups:
    if not (options.stack or options.pair):
        options.stack = True ## default            

## output file name
outfilename = args[0]

## input filenames
inputfilenames = args[1:]

if options.groups:
    if len(inputfilenames) % options.groups:
        parser.error("Inputfile count must be evenly divisible by number of groups. That is, there must be the same number of items in each group.")
    if options.group_labels and len(group_labels) != options.groups:
        parser.error("The number of x-tick labels must match the number of groups.")
#    if options.legend and len(legend_labels) != ( len(inputfilenames) / options.groups):
#        parser.error("The number of legend labels must match the number of items in each group")

if not options.separator:
    options.separator="," ## default

## read the data from the files
data = []
for inputfilename in inputfilenames:

    file_data = []
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    line_ct = 0

    datums = []
    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        if line_ct == 0 and options.has_header: ## the first line is a header line. skip it.
            line_ct += 1
            continue

        line = line.split( options.separator )

        try:
            converted_line = [ float(val) for val in line ]
        except ValueError:
            if options.ignorenan:
                continue ## move along
            else: ## we want to FUCKING DIE
                raise

        if len(converted_line) > 1: ## multi-column! Yow!
            member_ct = len(converted_line)
            member_indexes = range(0, member_ct)
            if options.columns:
                member_ct = len(columns)
                member_indexes = columns

            for i in range(0, member_ct):    
                if len(datums) <= i:
                    datums.append( [] ) ## add another column.

                datums[i].append( converted_line[ member_indexes[i] ] )    
        else:
            file_data.append( converted_line[0] ) ## just do it as a single column
        
        line_ct += 1

    fd.close()

    if options.debug_messages:
        print "RAW INPUT"
        print file_data

    if len(datums) == 0:
        data.append( file_data )
    else:
        data.extend( datums )

## BOOT STRAP HELPER - mean error
def Quantile(data, q, precision=1.0):
    """
    Returns the q'th percentile of the distribution given in the argument
    'data'. Uses the 'precision' parameter to control the noise level.
    """
    N, bins = np.histogram(data, bins=precision*np.sqrt(len(data)))
    norm_cumul = 1.0*N.cumsum() / len(data)

#    print bins
#    print bins[0]
#    print len(bins)
    
#    print norm_cumul
#    print len(norm_cumul)

#    print q

#    thingy = [ bins[i] for i in range(0, len(norm_cumul)) if norm_cumul[i] > q ]
#    print thingy
#    print len(thingy)

#    return thingy

    for i in range(0, len(norm_cumul)):
        if norm_cumul[i] > q:
            return bins[i]

#    return bins[norm_cumul > q][0]

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

## split the files into groups, and calculate the means and bootstrap errors
group_count = len(data) ## by default, there are as many groups as there are files
member_count = 1 ## and by default, there is only one member in each group.
if options.groups:
    group_count = options.groups ## ooop, now there are this many groups
    member_count = len(data) / group_count

if options.debug_messages:
    print "GROUP COUNT %s" % group_count
    print "MEMBER COUNT %s" % member_count




means = []
errors = []

data_index = 0
for i in range(0, group_count):
    means.append( [] )
    errors.append( [] )
    for j in range(0, member_count): # tick 'em off (this is inefficient, but whatever)
        means[-1].append( np.mean( data[data_index] ) )

        errors[-1].append( bootstrap_error( data[data_index] ) )
        data_index += 1 ## NEXT

    if options.debug_messages:
        print means
        print errors
#        print data_index

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
    Colors.Gray, 
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

artists = []
fig = pl.figure()
ax1 = fig.add_subplot(111)

indexes = np.arange(group_count)

total_width = 0.75
if not options.pair: ## stack it up (same case as no-stack with single-member groups)
    width = total_width
    bottoms = [ 0 for i in range(0, group_count) ] ## fill the bottoms with zeroes
    for item_index in range(0, member_count): ## start at the zeroth member (bottommost) and stack from there.
        if options.debug_messages:
            print "SET!"
        mean_set = [ group[item_index] for group in means ] ## pull it out
        be_set = [ group[item_index] for group in errors ] ## pull it out

        artists.append( ax1.bar( indexes, mean_set, width, color=color_sets[ item_index ], yerr=be_set, bottom=bottoms ) )

        if options.stack: ## we're stacking
            for i in range(0, len(bottoms)): ## update the bottoms
                bottoms[i] += mean_set[i]

elif options.pair: ## really an else here.
    width = total_width / member_count ## divide this up appropriately

    for item_index in range(0, member_count): ## start at the zeroth member (bottommost) and stack from there.

        mean_set = [ group[item_index] for group in means ] ## pull it out
        be_set = [ group[item_index] for group in errors ] ## pull it out

        artists.append( ax1.bar( indexes+(width*item_index), mean_set, width, color=color_sets[ item_index ], yerr=be_set ) )



if options.x_label:
    ax1.set_xlabel( options.x_label )

if options.y_label:
    ax1.set_ylabel( options.y_label )

if options.title:
    pl.title( options.title )

#print ax1.get_ylim()

if options.ylim_max:
    pl.ylim(0,options.ylim_max)
else:
    pl.ylim(0, ax1.get_ylim()[1])

#else
#    pl.ylim(0,

## set the xticks
if len(group_labels) == 0: ## none defined
    trunc_names = [ val.split('_')[0] for val in inputfilenames ]
    for i in range(0, len(trunc_names), member_count):
        if options.debug_messages:
            print "G LABEL INDEX %s " % i
        group_labels.append( trunc_names[i] ) 

if options.debug_messages:
    print "GROUP LABELS"
    print group_labels

pl.xticks(indexes+total_width/2., group_labels )

## set the legend
def proxy_artist( color ):
    p = pl.Rectangle((0,0), 1,1, fc=color)
    return p


if options.legend and len(artists) > 0 and len(legend_labels) > 0:
    if options.debug_messages:
        print
        print "ARTISTS"
        print artists
        print "LABELS"
        print legend_labels

    proxies = []
    for i in range(0, member_count):
        proxies.append( proxy_artist( color_sets[i] ) )

    if options.stack:
        proxies.reverse()
        legend_labels.reverse()
    

    pl.legend( proxies, legend_labels, bbox_to_anchor=(1.01, 1), loc=2, borderaxespad=0. )
    leg = pl.gca().get_legend()
    ltext = leg.get_texts()
    pl.setp( ltext, fontsize='small')

    l,b,w,h = pl.axes().get_position().bounds
    pl.axes().set_position([0.1,b,w*.78,h])

if options.show:
    pl.show()

pl.savefig(outfilename)
