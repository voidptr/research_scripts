# Plot the differences in means

# Written in Python 2.7
# RCK
# 8-24-11

import sys
import math
sys.path.append('../common modules and helper scripts')

from optparse import OptionParser
import read_intermediate_files as rif
import numpy as np
import matplotlib.pyplot as plt

# Set up options
usage = """usage: %prog [options] output_file control_data_file treatment_data_file
"""
parser = OptionParser(usage)
## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 3:
    parser.error("incorrect number of arguments")

output_filename = args[0]

control_filename = args[1]
treatment_filename = args[2]

control_data = rif.read_intermediate_datafile(control_filename)
treatment_data = rif.read_intermediate_datafile(treatment_filename)

def calculate_means( data ):
    ## calculate means across replicates

    #gather the values
    tasks = {}
    for task_and_replicate in data['Task_Oscillation_Amplitudes_By_Sample_And_Task'].keys():
        taskname = task_and_replicate.split('_')[0]

        if not taskname in tasks:
            tasks[taskname] = []

        tasks[taskname].append( data['Task_Oscillation_Amplitudes_By_Sample_And_Task'][ task_and_replicate ] )

    #calculate a mean curve ## treat this as a 2d matrix
    mean_task = {}
    ste_task = {}
    for task in tasks.keys():
        mean_task[task] = [] 
        ste_task[task] = []
        for point in range(0, len(tasks[task][0])):
            values = []
            for replicate in tasks[task]:
                values.append(int(replicate[point]))
            #print values
            mean_task[task].append( np.mean(values) )
            ste_task[task].append( np.std(values) / math.sqrt( len(values) ) )

    return mean_task

control_mean_task = calculate_means( control_data )
treatment_mean_task = calculate_means( treatment_data )

        




## plot and do labels
artists = []
task_names = []
for task in control_mean_task.keys():

    task_names.append( task + "_control" )
    plottable = np.add( control_mean_task[task], 0 )
    thingy = plt.plot( plottable )
    artists.append(thingy)


    task_names.append( task + "_treatment" )
    plottable = np.add( treatment_mean_task[task], 0 )
    thingy = plt.plot( plottable )
    artists.append(thingy)

plt.legend(artists,task_names)

# set scale to log, but I don't really need this.
#pl.yscale('log')

#pl.xlabel(xaxislabel)
#pl.ylabel(yaxislabel)

#pl.xlim(0,3500)

plt.savefig(output_filename)

print output_filename












