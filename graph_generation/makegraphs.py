#!/usr/bin/python

###################
# Make Graphs
###################

# system includes
import glob
import os
from optparse import OptionParser
import sys

sys.path.append( os.path.abspath( os.path.join( sys.path[0], "../common/" ) ) ) ## to common/
#print sys.path
import config as cf

cf.addpath( "fitness/" )
#cf.addpath( "modularity/" )
#cf.addpath( "coalescence/" )
#cf.addpath( "mutations/" )
cf.addpath( "task_ct/" )
cf.addpath( "stats.dat/" )
cf.addpath( "count.dat/" )

import fitness as fitness
import task_ct as task_ct
#import functional_modularity as functional_modularity
#import coalescence as coalescence
#import mutations as mutations
import stats_dat as stats_dat
import count_dat as count_dat

# Set up options
usage = """usage: %prog [options] action 

          
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

## testing options
parser.add_option("-g","--grouping", dest = "grouping", help = "primary grouping")
parser.add_option("-s","--subgrouping", dest = "subgrouping", help = "Add an additional sub-grouping")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

## actions
action = args[0]

## groupings (optional)
grouping = ""
if options.grouping:
    grouping = options.grouping

## subgroupings (optional)
subgrouping = ""
if options.subgrouping:
    subgrouping = options.subgrouping

######## do the work

## timeseries
returns = True
if action == "fitness_timeseries": 
        returns = fitness.plot_timeseries( grouping=grouping, subgrouping=subgrouping )
elif action == "tasks_timeseries": 
        returns = task_ct.plot_timeseries( grouping=grouping, subgrouping=subgrouping )


elif action == "genome_change_timeseries": 
        returns = stats_dat.plot_genome_change_timeseries( grouping=grouping, subgrouping=subgrouping )
elif action == "genotypic_entropy_timeseries": 
        returns = stats_dat.plot_genotypic_entropy_timeseries( grouping=grouping, subgrouping=subgrouping )
elif action == "genotype_count_timeseries": 
        returns = count_dat.plot_genotype_count_timeseries( grouping=grouping, subgrouping=subgrouping )





#elif action == "coalescent_timeseries": 
#        returns = coalescence.aggregate_timeseries( directories, grouping=grouping, subgrouping=subgrouping, test=options.test, expected=options.expected )
#elif action == "functional_modularity_timeseries": 
#        returns = functional_modularity.aggregate_timeseries( directories, grouping=grouping, subgrouping=subgrouping, test=options.test, expected=options.expected )
#elif action == "coding_mutations_timeseries": 
#        returns = mutations.aggregate_coding_mutations_timeseries( directories, grouping=grouping, subgrouping=subgrouping, test=options.test, expected=options.expected )
#elif action == "degenerate_mutations_timeseries": 
#        returns = mutations.aggregate_degenerate_mutations_timeseries( directories, grouping=grouping, subgrouping=subgrouping, test=options.test, expected=options.expected )
#elif action == "noncoding_mutations_timeseries": 
#        returns = mutations.aggregate_noncoding_mutations_timeseries( directories, grouping=grouping, subgrouping=subgrouping, test=options.test, expected=options.expected )
### timeseries compression - not all are represented, but more can easily be added as required
elif action == "fitness_max": 
        returns = fitness.plot_barchart( grouping=grouping, subgrouping=subgrouping, type="max" )
elif action == "fitness_average": 
        returns = fitness.plot_barchart( grouping=grouping, subgrouping=subgrouping, type="mean" )

#elif action == "coding_mutations_average": 
#        returns = mutations.coding_mutations_collapse( grouping=grouping, subgrouping=subgrouping, type="mean", test=options.test, expected=options.expected )
#elif action == "degenerate_mutations_average": 
#        returns = mutations.degenerate_mutations_collapse( grouping=grouping, subgrouping=subgrouping, type="mean", test=options.test, expected=options.expected )
#elif action == "noncoding_mutations_average": 
#        returns = mutations.noncoding_mutations_collapse( grouping=grouping, subgrouping=subgrouping, type="mean", test=options.test, expected=options.expected )
### dunno wtf
else: 
    print "unknown action: %s" % action
    exit(1)

if returns:

    print "DONE!"
    exit(0)
else:

    print "FAILED WITH ERROR"
    exit(1)

