# Plot the differences in means

# Written in Python 2.7
# RCK
# 8-24-11

import sys
sys.path.append('../common modules and helper scripts')

from optparse import OptionParser
import read_intermediate_files as rif
import numpy as np
import matplotlib.pyplot as plt

# Set up options
usage = """usage: %prog [options] output_file data_file 
"""
parser = OptionParser(usage)
## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

output_filename = args[0]

input_filename = args[1]
data = rif.read_intermediate_datafile(input_filename)
    

## get means

control_means = []
treatment_means = []

control_stds = []
treatment_stds = []

for task_name in data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'].keys():
    control_mean = float( data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'][task_name][0] )
    treatment_mean = float( data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Treatment'][task_name][0] )

    control_means.append( control_mean )
    treatment_means.append( treatment_mean )

    control_std = float( data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'][task_name][2] )
    treatment_std = float( data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Treatment'][task_name][2] )

    control_stds.append( control_std )
    treatment_stds.append( treatment_std )

    mann_whitney_u_stat = float( data[ 'Mann_Whitney_U_Statistics_By_Task'][task_name][0] )
    mann_whitney_u_pval = float( data[ 'Mann_Whitney_U_Statistics_By_Task'][task_name][1] )

indices = np.arange( len(data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'].keys()) )
indices = [ (val + 0.1) for val in indices ]
indices_offset = [ (val + 0.35) for val in indices ]

tick_locations = np.arange( len(data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'].keys()) )
tick_locations = [ (val + 0.45) for val in tick_locations ]
print tick_locations

width = 0.35


p1 = plt.bar( indices, control_means, width, color='r', yerr=control_stds )
p2 = plt.bar( indices_offset, treatment_means, width, color='y', yerr=treatment_stds )

plt.ylabel( 'Mean Median Task Oscillation Amplitude' )
plt.title( 'Mean Median Task Oscillation Amplitudes by Task' )
plt.xticks( tick_locations, data[ 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'].keys() )
plt.legend( (p1[0], p2[0]), ('control','treatment') )

plt.savefig(output_filename)


