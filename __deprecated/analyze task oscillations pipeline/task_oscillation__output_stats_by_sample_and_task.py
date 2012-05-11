# Quantify the Amplitude of the Oscillation
# of Task Execution

# Written in Python 2.7
# RCK
# 5-26-11

import sys
sys.path.append('../common modules and helper scripts')


import math
import gzip
import numpy as np
import pylab as pl
import scipy.stats as spstats
#from scypi import *
from optparse import OptionParser
import multidimensional_avida_datafiles as md
import calculate_task_oscillation as cto

# Set up options
usage = """usage: %prog [options] start_update stop_update cycle_length tasks_filename1 [tasks_filename2 ...]
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 4:
    parser.error("incorrect number of arguments")

start_update = int(args[0])

stop_update = int(args[1])

cycle_length = int(args[2])

## tasks filenames
inputfilenames = args[3:]

## read the datafile and get the data out
(samples, task_names, updates_list) = md.load_tasks_files_as_samples_by_file( inputfilenames, start_update, stop_update )
            
## calculate the amplitudes for each sample
amplitudes_by_sample_and_task = cto.calculate_task_amplitudes(samples, task_names, updates_list, start_update, stop_update, cycle_length)
  

## now, calculate the amplitude stats for each sample
stats_by_sample_and_task = cto.calculate_stats_by_task_and_sample( amplitudes_by_sample_and_task, task_names )
 
## pull out the stats for each task, by sample
## these variance is the within replicate variance (unexplained variance)
print "#Median Amplitudes of Oscillation for each replicate, separated by task"
print "Median_Task_Oscillation_Amplitudes_By_Task"
print "Task_Name, Median_Task_Oscillation_Amplitudes"
for task_name in task_names: ## tasks first
    medians = []
    for sample in stats_by_sample_and_task:
        medians.append( str(sample[ task_name ]['median']) )       
    print task_name + "," + ",".join(medians)
print


