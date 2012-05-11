# Multi-Column Graph

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser

# Set up options
usage = """usage: %prog environment_file rewarded_task non_rewarded_task tasks_filename1 [tasks_filename2 ...]
"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 3:
    parser.error("incorrect number of arguments")

env_file = args[0]

rewarded_task = args[1]
non_rewarded_task = args[2]

## tasks filename
inputfilenames = args[3:]


## read in the env file and figure out what the environment looks like

## Setup oscillating environment
#u 10001:1000:100000 SetReactionValue NOT 3.0 
#u 10001:1000:100000 SetReactionValue NAND 0
#u 10501:1000:100000 SetReactionValue NOT 0
#u 10501:1000:100000 SetReactionValue NAND 3.0 
## set up the long tail - NAND (kick it off from the last state of NAND rewarded)
#u 100001 SetReactionValue NOT 0
#u 100001 SetReactionValue NAND 3.0

if env_file[-3:] == ".gz"
    fd = gzip.open(env_file)
else
    fd = open(env_file)

rewards = {}

for line in fd:
    line = line.strip()

    if len(line) == 0:
        found = False
 
    if found:
        line = line.split() ## split on the spaces
        cycles = line[1].split(":") ## split on the : in the cycle

        task = line[3]
        reward = float(line[4])

        if ( reward > 0 ):
            rewards[task]["start"] = int(cycles[0])

        if ( reward <= 0 ):
            rewards[task]["stop"] = int(cycles[0])

        if ( rewards[task].has_key("start") && rewards[task].hash_key("stop") ): ## they're both there
            rewards[task]["cycle"] = abs( rewards[task]["stop"] - rewards[task]["start"] )


    if line == "# Setup oscillating environment": # found the first line
        found = True
    



## tasks array matrix
## x - task
## y - sample point (update)
## z - data point (as many as we have files)

tasks_array_matrix = [] ## 3d lists
task_names = []

updates = []

task_level_100percent = 2500
task_level_2percent = task_level_100percent * 0.02

## setup stuff
populated = False
for inputfilename in inputfilenames:
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)  
    
#    if options.verbose:
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
            updates.append( line[0] ) ## put in the updates.

        else:
            for task_num in range( 0, len(line)-1 ):
                tasks_array_matrix[task_num][sample_ct].append( float( line[task_num + 1] ) ) ## append further samples
            
        sample_ct += 1
    fd.close()
    populated = True ## done with the first run-through

## generate the medians to be displayed
tasks_array_matrix_medians = []
task_mean_time_to_loss = []
task_num = 0
for task in tasks_array_matrix:
    tasks_array_matrix_medians.append([]) ## set up the samples bucket for this task
    task_mean_time_to_loss.append( [0,0] ) ## init with -1
    sample_index = 0
    for sample_set in task: 
        median = np.median( sample_set )
        tasks_array_matrix_medians[task_num].append( median )
        #if ( sample_index > 100 and median < task_level_2percent and task_mean_time_to_loss[-1] == -1 ):
        #print updates[sample_index]
        if ( int(updates[sample_index]) == start_phase_update ):
            #print "hi"
            task_mean_time_to_loss[-1][0] = median

        if ( int(updates[sample_index])== end_phase_update ):
            task_mean_time_to_loss[-1][1] = median

#            task_mean_time_to_loss[-1] = updates[sample_index]
        sample_index += 1
        

    task_num += 1

print task_names
print task_mean_time_to_loss 


