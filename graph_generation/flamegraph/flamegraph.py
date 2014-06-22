# This program takes a column number for phylogenetic depth (or any other key-able column), a column number
# for number of organisms, and a series of files.  It produces a flame graph,
# a colored version of a matrix where each row is a histogram of the relevant
# column.
#
# Adapted from Avida's source/utils/hist_map.cc
#
# Written in Python 2.5.1
# BLW
# 9-7-09
#
# Last Updated by RCK on 4/18/12

import matplotlib
matplotlib.use('Agg')

import gzip
import numpy as np
import pylab as pl
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile key_col count_col infile1 [infile2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-g", "--graph", action = "store_true", dest = "showgraph",
                  default = False, help = "show the graph")
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")

parser.add_option("--ylim_max", dest = "ylim_max", type="int",
                  help = "Max Y-Axis value")

parser.add_option("-x", "--xlabel", dest="x_label", type="string", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="y_label", type="string", 
                  help="Y-axis Label")
parser.add_option("--x_tick_intervals", dest="x_tick_intervals", type="string", 
                  help="X-axis Tick Intervals")
parser.add_option("-t", "--title", dest="title", type="string", 
                  help="Graph Title")


(options, args) = parser.parse_args()

if len(args) < 4:
    parser.error("incorrect number of arguments")

outfilename = args[0]

key_col = int( args[1] )
count_col = int( args[2] )

inputfilenames = args[3:]
num_files = len(inputfilenames)

count_arrays = []
count_dicts = []

for inputfilename in inputfilenames:
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    site_count_dict = {}
    total_count = 0
    line_num = 0

    for line in fd:
        line = line.strip()
        if len(line) == 0 or line[0] == '#':
            continue
        line = line.split()
        
        key_value = int(line[key_col - 1])
        count = int(line[count_col - 1])

        if count == 0: ## we don't care about dead ones.
            continue
            
        if key_value < 0:
            print "Error in file '" + args[i + 3] + "': Only positive values allowed."
            print "   (line =", line_num + 1, "count =", count, "key_value = " + str(key_value) + "')"
            sys.exit(1)

        if count < 0:
            print "Error in file '" + args[i + 3] + "': Only positive abundance allowed"
            sys.exit(1)
            
        # create dictionary of values : non-zero counts
        if key_value in site_count_dict:
            site_count_dict[key_value] += count
        else:
            site_count_dict[key_value] = count

        line_num += 1

    count_dicts.append(site_count_dict)

    fd.close()

# Now that we have all of the information:
#  - figure out how long our lists need to be
#  - create the lists, full of 0s
#  - populate relevant fields with actual data from the dictionaries
max_size = max([max(d.keys()) for d in count_dicts])

if options.ylim_max > max_size: ## set it here.
    max_size = options.ylim_max

count_arrays = [[0] * (max_size + 1) for i in range(num_files)]
for i in range(0, num_files):
    for key in count_dicts[i]:
        count_arrays[i][key] = math.log(count_dicts[i][key]) ## these should always be non-zero

# And now print it all out
print num_files, "rows,", max_size, "columns."

# Now we graph it!
flame_graphable = np.array( count_arrays )
flame_graphable = np.transpose(flame_graphable)


# We actually graph the transpose of the log of the matrix + 1
#flame_graphable = (np.log(np.add(count_arrays, 1))).conj().transpose()
print "graphing!"
pl.hot()
flame_graph = pl.pcolor(flame_graphable)

if options.ylim_max:
    pl.ylim((0, options.ylim_max))
else:
    pl.ylim((0, max_size))

pl.xlim((0, num_files))

if options.x_tick_intervals:

    interval = int(options.x_tick_intervals)

    xmin, xmax = pl.xlim()

    xlocs, xlabels = pl.xticks()
    xmodlabels = []
    xmodlocs = []
    for i in range(0, len(xlocs)):
        xmodlabels.append( int(xlocs[i] * interval) )
        xmodlocs.append( xlocs[i] )

    pl.xticks( xmodlocs, xmodlabels )

if options.x_label:
    pl.xlabel( options.x_label )
if options.y_label:
    pl.ylabel( options.y_label )

if options.title:
    pl.title( options.title )

pl.savefig(outfilename)

if options.showgraph:
    pl.show()
