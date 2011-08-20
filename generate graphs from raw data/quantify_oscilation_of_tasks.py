# Quantify the Amplitude of the Oscillation
# of Task Execution

# Written in Python 2.7
# RCK
# 5-26-11

import math
import gzip
import numpy as np
import pylab as pl
from optparse import OptionParser
import multidimensional_avida_datafiles as md
import calculate_task_oscillation as cto

# Set up options
usage = """usage: %prog [options] outfile start_update stop_update cycle_length backbone_task datasets last_divider tasks_filename1 [tasks_filename2 ...]

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
if len(args) < 8:
    parser.error("incorrect number of arguments")

outfile = args[0]

start_update = int(args[1])

stop_update = int(args[2])

cycle_length = int(args[3])

backbone_task = args[4]

datasets = args[5]

last_divider = args[6]

## tasks filenames
inputfilenames = args[7:]

## interpret the datasets file
fd = open( datasets )
inputfilenamesbydataset = {}
dataset_names = []
for line in fd:
    line = line.strip()
    if len(line) > 0:
        inputfilenamesbydataset[line] = []
        dataset_names.append(line)
fd.close()

for filename in inputfilenames:
    inputfilenamesbydataset[filename[0:filename.rfind(last_divider)+1]].append(filename)


dataout = {}
for dataset in inputfilenamesbydataset.keys():
    inputfilenames = inputfilenamesbydataset[dataset]
    if len(inputfilenames) > 0:

        print dataset
        ## read the datafile and get the data out
        (samples, task_names, updates_list) = md.load_tasks_files_as_samples_by_file( inputfilenames, start_update, stop_update )

        ## now calculate the oscillation
        stats_by_task = cto.calculate_oscillation_stats_by_task(samples, task_names, updates_list, start_update, stop_update, cycle_length)

#        (mean_amplitudes_by_task, std_mean_amplitudes_by_task, ste_mean_amplitudes_by_task) = cto.calculate_mean_task_oscillation(samples, task_names, updates_list, start_update, stop_update, cycle_length)

        dataout[dataset] = (stats_by_task['mean'], stats_by_task['std'], stats_by_task['ste'])

        ## now, output the median median (not a typo) amplitudes
        print "mean: " + str(stats_by_task['mean'])
        print "median:" + str(stats_by_task['median'])
        print "std:  " + str(stats_by_task['std'])
        print "ste:  " + str(stats_by_task['ste'])
        print "variance:" + str(stats_by_task['variance'])

    
## ok! Now that we have the data, plot it in a bar chart! :D

names = dataout.keys()
amplitudes = []
errors = []
colors = []
color_assignments = { 'punish': 'red', 'nopunish': 'green', 'control': 'blue' }
for name in dataset_names:
    #print dataout[name], dataout[name][0], dataout[name][0][backbone_task]

    if name in dataout.keys():

        if 'nopunish' in name:
            colors.append( color_assignments['nopunish'] )
        elif 'punish' in name:
            colors.append( color_assignments['punish'] )
        elif 'control' in name:
            colors.append( color_assignments['control'] )

        amplitudes.append( dataout[name][0][backbone_task] )
        errors.append( dataout[name][2][backbone_task] )


N = len(amplitudes)
ind = np.arange(N)
width = 0.35

plot = pl.bar( ind, amplitudes, width, color=colors, yerr=errors, ecolor='black', align='center'  )
pl.ylabel( "Cyclic Task Execution Oscillation Amplitude" )
pl.xticks( ind+width/2., names, rotation=20)

pl.savefig( outfile, bins=1 )

