
# Written in Python 2.7
# RCK
# 2-20-12


import gzip
import math
import numpy
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile infile1 [infile2]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-l", "--length_ct", action = "store_true", dest = "length_ct",
                  default = False, help = "test length/ct ratio")
parser.add_option("-s", "--std", action = "store_true", dest = "std",
                  default = False, help = "test std")
parser.add_option("-r", "--std_ratio", action = "store_true", dest = "std_ratio",
                  default = False, help = "test optstd/std ratio")
parser.add_option("-d", "--std_difference", action = "store_true", dest = "std_diff",
                  default = False, help = "test std-opt_std difference")
parser.add_option("-a", "--std_ratdiff", action = "store_true", dest = "std_ratdiff",
                  default = False, help = "test std-opt_std/opt_std difference ratio")
parser.add_option("-g", "--gapstd", action = "store_true", dest = "gapstd",
                  default = False, help = "test gap std")
parser.add_option("-q", "--sqrtgap", action = "store_true", dest = "sqrtgap",
                  default = False, help = "test average square root of gap")


parser.add_option("-i", "--length_insensitivity", action = "store_true", dest = "insensitivity",
                  default = False, help = "test length insensitivity")
parser.add_option("-t", "--distrubtion_sensitivity", action = "store_true", dest = "dist_sensitivity",
                  default = False, help = "test distribution sensitivity")
parser.add_option("-o", "--outlier", action = "store_true", dest = "outlier",
                  default = False, help = "test outlier")
## fetch the args
(options, args) = parser.parse_args()

def length_ct_ratio( task_positions ):
    if len(task_positions) == 0 or task_positions[-1] == 0:
        return 0
    return len(task_positions) / float(task_positions[-1]+1)

def calc_std( task_positions ):
    return numpy.std( task_positions )

optimal_task_positions = range(0,300)
optimal_std = []
for i in optimal_task_positions:
    optimal_std.append( numpy.std( optimal_task_positions[0:i] ) )

def calcstd_ratio( task_positions ):
    std = numpy.std( task_positions )
    opt_std = optimal_std[ len(task_positions) ]
    return opt_std/float(std)

def calcstd_difference( task_positions ):
    std = numpy.std( task_positions )
    opt_std = optimal_std[ len(task_positions) ]
    return std - opt_std

def calcstd_ratdiff( task_positions ):
    std = numpy.std( task_positions )
    opt_std = optimal_std[ len(task_positions) ]
    return (std - opt_std)/opt_std

def calcgap_std( task_positions ):
    gaps = []
    lastpos = -1
    #print
    #print task_positions
    for position in task_positions:
        if lastpos > -1:
            gap = position - lastpos
            gaps.append( gap )
        lastpos = position
    #print gaps
    return numpy.std( gaps )

def calc_sqrtgap( task_positions ):
    gaps = []
    lastpos = -1
    #print
    #print task_positions
    for position in task_positions:
        if lastpos > -1:
            gap = position - lastpos
            gaps.append( math.sqrt(gap) )
        lastpos = position
    #print gaps
    return numpy.mean( gaps )



##### Generate some data to test
## Length Insensitivity
test_tasks_length_insensitivity = []
for j in range(1,10):

    test_tasks = []
    for i in range(1,100):
        task = []
        task.extend( range(0, i) )
        task.extend( range(i*j, (i*j)+i) )

        test_tasks.append( task )

    test_tasks_length_insensitivity.append( test_tasks )

## Distribution Sensitivity
test_tasks_distribution_sensitivity = []
for gap_size_multiplier in range(1,20): ## ten sets of lines (the sizes of the gaps (the multiplier for the gap))

    #print "MULT:"
    #print gap_size_multiplier
    test_tasks_gaptoothed = []
    test_tasks_distributed = []

    ## this section increases the size of the task segments, and increases the gap between them by a fixed multiplier
    ## thus, each set contains a set of zoomed tasks
    for task_segment_length in range(1,100): ## the length of the tasks segments

        ## do the XXXXX________X
        task = []
        task.extend( range(0, task_segment_length) )
        task.extend( range(task_segment_length*gap_size_multiplier, (task_segment_length*gap_size_multiplier)+1) )
        test_tasks_gaptoothed.append( task )
        #print "OUTLIER:"
        #print task

        ## do the equivalent distributed one
        #### for simplicity, only doing the even # multipliers
        if gap_size_multiplier % 2 == 0:
            task = []
            spacefill = gap_size_multiplier/2

            task = range(1,  ((task_segment_length*gap_size_multiplier)+1)+1, spacefill+2)
            #print "DISTRIBUT:"
            #print task
            test_tasks_distributed.append( task )

    test_tasks_distribution_sensitivity.append( test_tasks_gaptoothed )
    test_tasks_distribution_sensitivity.append( test_tasks_distributed )

#print test_tasks_distribution_sensitivity



## Single Outlier
test_tasks_single_outlier = []
for i in range(2, 100): ## start w/ no spaces, keep adding spaces, pushing the outlier further and further
    positions = [0] ## always start with a zero position
    positions.extend( range(i, 99+i) ) ## count up from there.

   # print "LINE"

    tasks = []
    for j in range(1, 100):
       # print "TASK"
        tasks.append( positions[0:j] )
   # print tasks
    test_tasks_single_outlier.append( tasks )

#print test_tasks_length_insensitivity

test_tasks = []
if options.insensitivity:
    test_tasks = test_tasks_length_insensitivity
elif options.dist_sensitivity:
    test_tasks = test_tasks_distribution_sensitivity
elif options.outlier:
    test_tasks = test_tasks_single_outlier

for task_set in test_tasks:
        measures = []
        for task in task_set:
            val = 0
            if options.length_ct:
                #print "HI"
                val = length_ct_ratio( task )
            elif options.std:
                val = calc_std( task )
            elif options.std_ratio:
                val = calcstd_ratio( task )
            elif options.std_diff:
                val = calcstd_difference( task )
            elif options.std_ratdiff:
                val = calcstd_ratdiff( task )
            elif options.gapstd:
                val = calcgap_std( task )
            elif options.sqrtgap:
                val = calc_sqrtgap( task )

            measures.append( str( val ) )
        print ",".join( measures )


