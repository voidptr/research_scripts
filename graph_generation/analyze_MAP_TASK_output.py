# Read a datafile produced by MAP_TASK analyze mode command and extract the information neccessary to ascertain what sites are required for what task

# Written in Python 2.7
# RCK
# 10-2-11


import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile parent_col child_col infile1

Permitted types for outfile are png, pdf, ps, eps, and svg"""

parser = OptionParser(usage)

parser.add_option("-v", "--verbose", action="store_true", dest="verbose", default=False, help="Verbose" )


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 4:
    parser.error("incorrect number of arguments")

outfile = args[0]

parent_col = int( args[1] )
child_col = int( args[2] )

## datafile file name
inputfilename = args[3]

if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)


## each entry is a site in the genome, and contains the bit string describing what tasks that organism can do with that site disabled
parent = "00"
parent_tasks = []
sites = []
sites_fatal_or_deleterious = []

for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.replace(' ',',') ## replace all spaces with commas    
    line = line.split(",") ## break the line up on commas

    if (line[0] == '-1'): ## this is the header line
        parent = line[parent_col]
        parent_tasks = list( parent )

        if ( options.verbose ):
            for i in range(0, len(line)):
                print str(i) + " " + line[i]
    else:
        if ( options.verbose ):
            for i in range(0, len(line)):
                print str(i) + " " + line[i]
 

        tasks = list(line[child_col]) ## just split every character

        affected_tasks = []
        for i in range(0, len(parent_tasks)): ## loop through the tasks
            if options.verbose:
                print parent_tasks
                print tasks
            if parent_tasks[i] != tasks[i]:
                affected_tasks.append(1)
            else:
                affected_tasks.append(0)
        sites.append( affected_tasks )

fd.close()

## ok, now I have a matrix that goes in the wrong direction. switch it

sites_by_task = []

for i in range(len(parent_tasks)):
    sites_by_task.append([])
    for site in sites:
        sites_by_task[i].append( site[i] )

sum = [ np.sum(tasks_affected) for tasks_affected in sites ]


#print parent_tasks
#print sites
#print sites_by_task


pl.xlabel("site")
pl.ylabel("matters for task")
pl.ylim(0,2)

offset = 0.0
for task in sites_by_task:
#    print task

    task = [ site + offset for site in task ]

    plottable = np.add( task , 0 )
    #pl.plot( plottable )
    pl.scatter( np.arange( len(task) ), plottable, c = 'r' )

    offset += 0.1

#pl.plot(sum)
    

pl.savefig( outfile )











#pl.xlabel(x_axis)
#pl.ylabel(column_name)
#
#if options.log_scale:
#    # set to log scale
#    pl.yscale('log')
#
#if options.median_only:
#    median_fitness_array = []
#    for datapoint in fitness_2d_array:
#        median_fitness_array.append( np.mean( datapoint ) )
#    plottable = np.add( median_fitness_array, 0 )
#    pl.plot( plottable )
#elif options.median:
#    plottable = np.add( fitness_2d_array, 0 )
#    pl.plot( plottable, '#CCCCCC' )
# 
#    median_fitness_array = []
#    for datapoint in fitness_2d_array:
#        median_fitness_array.append( np.mean( datapoint ) )
#    plottable = np.add( median_fitness_array, 0 )
#
##    for datapoint in fitness_2d_array:
##        datapoint.append( np.mean( datapoint ) )
#    pl.plot( plottable, 'k' )
#else:
#    plottable = np.add( fitness_2d_array, 0 )
#    pl.plot( plottable )
#
#pl.savefig(outfilename)

