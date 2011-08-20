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

### LEFT OFF HERE 8-18-11 3:28pm
### todo here, calculate the stats and print them off
##    print task_name + "," + str(mann_whitney_u[0]) + "," + str(mann_whitney_u[1])
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

# Within a treatment, I want to verify that the mean oscillations of the replicates are not significantly different from each other. 
# In other words, that my replicates are true replicates. 

# So, I want to get the standard devation of my means
## pull out just the means
#for task_name in task_names: ## tasks first
#    means = []
#    print task_name + ": "
#    for sample in stats_by_sample_and_task:
#        print str(sample[ task_name ]) ## print the stats
#        means.append( sample[task_name][mean] )        
#    print

#    std = np.std( means )

#no_punish_median_oscillations_andnot = [226.5,152.0,260.0,235.5,264.5,216.0,268.0,279.0,144.0,223.5,346.0,144.0,228.5,255.5,236.5]
#control_median_oscillations_andnot = [87.5,98.0,79.5,104.5,90.5,106.5,95.0,115.0,74.5,98.0,90.5,116.0,98.0,99.5,80.0]

#result = spstats.mannwhitneyu(no_punish_median_oscillations_andnot, control_median_oscillations_andnot)

#print str(result)
