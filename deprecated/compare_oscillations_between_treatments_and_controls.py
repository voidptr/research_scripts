# Quantify the Amplitude of the Oscillation
# of Task Execution

# Written in Python 2.7
# RCK
# 5-26-11

import numpy as np
import scipy.stats as spstats
from optparse import OptionParser
import read_intermediate_files as rif

# Set up options
usage = """usage: %prog [options] median_amplitudes_filename median_amplitudes_filename2
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

medians_file1 = args[0]
medians_file2 = args[1]

## read the datafile and get the data out
medians1 = rif.read_datafile( medians_file1 )
medians2 = rif.read_datafile( medians_file2 )

#print medians1
#print medians2

mean_of_medians1 = {}
mean_of_medians2 = {}

for key in medians1.keys():

    mean_of_medians1[ key ] = np.mean( medians1[ key ] )
    mean_of_medians2[ key ] = np.mean( medians2[ key ] )
    manwhitney_result = spstats.mannwhitneyu( medians1[key], medians2[key] )
    print key + ": "
    print medians_file1 + " mean: " + str(mean_of_medians1[ key ])
    print medians_file2 + " mean: " + str(mean_of_medians2[ key ])

    print str(manwhitney_result)

