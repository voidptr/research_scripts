# Compare the median amplitudes using mann whitney u

# Written in Python 2.7
# RCK
# 8-18-11

import sys
sys.path.append('../common modules and helper scripts')

import math
import scipy.stats as spstats
from optparse import OptionParser
import read_intermediate_files as rif

# Set up options
usage = """usage: %prog [options] control_amplitudes.txt treatment_amplitudes.txt
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

control_filename = args[0]
treatment_filename = args[1]

control_data = rif.read_intermediate_datafile(control_filename)['Median_Task_Oscillation_Amplitudes_By_Task'] ## there's only one thing
treatment_data = rif.read_intermediate_datafile(treatment_filename)['Median_Task_Oscillation_Amplitudes_By_Task'] ## there's only one thing

print 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Control'
print "Task_Name,mean,median,std,ste,variance"
for task_name in control_data.keys():
    control_medians = control_data[task_name]

    median =  np.median (control_medians )
    mean = np.mean ( control_medians )
    std = np.std ( control_medians )
    ste = std / math.sqrt( len ( control_medians ) )
    variance = np.var ( control_medians )

    print task_name + "," + mean + "," + median + "," + std + "," + ste + "," + variance

print

print 'Mean_Median_Task_Oscillation_Amplitude_By_Task__Treatment'
print "Task_Name,mean,median,std,ste,variance"
for task_name in treatment_data.keys():
    treatment_medians = treatment_data[task_name]

    median =  np.median ( treatment_medians )
    mean = np.mean ( treatment_medians )
    std = np.std ( treatment_medians )
    ste = std / math.sqrt( len ( treatment_medians ) )
    variance = np.var ( treatment_medians )

    print task_name + "," + mean + "," + median + "," + std + "," + ste + "," + variance

print

## print the mann whitney u stats

print 'Mann_Whitney_U_Statistics_By_Task'
print "Task_Name, Mann_Whitney_U, PValue"
for task_name in control_data.keys():
    control_medians = control_data[task_name]
    treatment_medians = treatment_data[task_name]

    mann_whitney_u = spstats.mannwhitneyu(control_medians, treatment_medians)

    print task_name + "," + str(mann_whitney_u[0]) + "," + str(mann_whitney_u[1])
print



