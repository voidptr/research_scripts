# Plot the Distribution of the Amplitude of the Oscillation
# of Task Execution

# Written in Python 2.7
# RCK
# 5-28-11

import numpy as np
import pylab as pl
from optparse import OptionParser
import multidimensional_avida_datafiles as md
import calculate_task_oscillation as cto

# Set up options
usage = """usage: %prog [options] outfile start_update stop_update cycle_length backbone_task datasets last_divider tasks_filename1 [tasks_filename2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser( usage )
parser.add_option( "-g", "--graph", action = "store_true", dest = "showgraph",
                  default = False, help = "show the graph" )
parser.add_option( "-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout" )
parser.add_option( "-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout" )

## fetch the args
( options, args ) = parser.parse_args()

## parameter error
if len( args ) < 8:
    parser.error( "incorrect number of arguments" )

outfile = args[0]
start_update = int( args[1] )
stop_update = int( args[2] )
cycle_length = int( args[3] )
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
    if len( line ) > 0:
        inputfilenamesbydataset[line] = []
        dataset_names.append( line )
fd.close()

for filename in inputfilenames:
    inputfilenamesbydataset[filename[0:filename.rfind( last_divider ) + 1]].append( filename )


dataout = {}

for dataset in inputfilenamesbydataset.keys():
    inputfilenames = inputfilenamesbydataset[dataset]
    if len( inputfilenames ) > 0:

        print dataset
        ## read the datafile and get the data out
        ( samples, task_names, updates_list ) = md.load_tasks_files_as_samples_by_file( inputfilenames, start_update, stop_update )

        amplitudes_by_sample_and_task = cto.calculate_task_amplitudes( samples, task_names, updates_list, start_update, stop_update, cycle_length )
 
        for taskname in amplitudes_by_sample_and_task[0].keys():
            allamplitudes = []
            for sample in amplitudes_by_sample_and_task:
                allamplitudes.append( sample[taskname] )

            bin_width_fraction = .5 #1/float(len(task))
            N = len( allamplitudes )
            ind = np.arange( N )
            width = 0.35

            pl.hist( allamplitudes )#, rwidth=bin_width_fraction,color=colors[file_num] )
            pl.ylabel( "Cyclic Task Execution Oscillation Amplitude" )
#                #pl.xticks( ind+width/2., names, rotation=20)
            pl.savefig( dataset + taskname + "_" + outfile, bins = 1 )


#        samplenum = 0
#        for sample in amplitudes_by_sample_and_task:
#            for taskname in sample.keys():
#
#                task = sample[taskname]
#                bin_width_fraction = .5 #1/float(len(task))
#                N = len(task)
#                ind = np.arange(N)
#                width = 0.35
#
#                pl.hist( task )#, rwidth=bin_width_fraction,color=colors[file_num] )
#
#                #plot = pl.hist( ind, task, width, ecolor='black', align='center'  )
#                pl.ylabel( "Cyclic Task Execution Oscillation Amplitude" )
#                #pl.xticks( ind+width/2., names, rotation=20)
#
#                pl.savefig( dataset + taskname + "_" + str(samplenum) + "_" + outfile, bins=1 )
#            samplenum += 1
