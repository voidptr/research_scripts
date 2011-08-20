# Multi-Column Graph

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile y-axis x-axis tasks_filename1 [tasks_filename2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-g", "--graph", action = "store_true", dest = "showgraph",
                  default = False, help = "show the graph")
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

## output file name
outfilename = args[0]

## y-axis label
yaxislabel = args[1]

xaxislabel = args[2]

## tasks filename
inputfilenames = args[3:]

## tasks array matrix
## x - task
## y - sample point (update)
## z - data point (as many as we have files)

tasks_array_matrix = [] ## 3d lists
task_names = []


## setup stuff
populated = False
for inputfilename in inputfilenames:
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)  
    
    if options.verbose:
        print "Processing: '" + inputfilename + "'"
    
    sample_ct = 0
    line_ct = 0
    for line in fd:
        ## prep the line
        line = line.strip() ## strip off the end of line crap
        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            if line_ct > 4 and len(line) > 0 and not populated:
                line = line.split()
                task_names.append( line[ (len(line)-1) ] )
            line_ct += 1
            continue
        line = line.split() ## break the line up on spaces
        
        if not populated and len(tasks_array_matrix) < len(line) - 1: ## set up the initial array of tasks
            for i in range( 1, len(line) ): 
                tasks_array_matrix.append( [] ) ## task arrays
        
        if not populated:
            for task_num in range( 0, len(line)-1 ):
                tasks_array_matrix[task_num].append([ float( line[task_num + 1] ) ]) ## insert the first sample
        else:
            for task_num in range( 0, len(line)-1 ):
                tasks_array_matrix[task_num][sample_ct].append( float( line[task_num + 1] ) ) ## append further samples
            
        sample_ct += 1
    fd.close()
    populated = True ## done with the first run-through

## generate the medians to be displayed
tasks_array_matrix_medians = []
task_num = 0
for task in tasks_array_matrix:
    tasks_array_matrix_medians.append([]) ## set up the samples bucket for this task
    for sample_set in task: 
        tasks_array_matrix_medians[task_num].append( np.median( sample_set ) )
    task_num += 1

## plot and do labels
artists = []
for task in tasks_array_matrix_medians:
    plottable = np.add( task, 0 )
    
    thingy = pl.plot( plottable)
    
    artists.append(thingy)
pl.legend(artists,task_names)

# set scale to log, but I don't really need this.
#pl.yscale('log')

pl.xlabel(xaxislabel)
pl.ylabel(yaxislabel)

pl.xlim(0,3500)

pl.savefig(outfilename)



