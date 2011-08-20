# Plot signficances of Mann-Whitney 

# Written in Python 2.7
# RCK
# 8-2-11

import scipy.stats as spstats
from optparse import OptionParser
import read_intermediate_files as rif

# Set up options
usage = """usage: %prog [options] backbone_task mann_whitney_stats [ mann_whitney_stats2 ... ]
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

backbone_task = args[0]

mann_whitney_stats_files = args[1:]

results_collection = {}

for filename in mann_whitney_stats_files:
    results = rif.read_mannwhitney_output_datafile( filename )

#    print str(results)

    for taskname in results.keys():
        if (taskname != backbone_task):
            results_collection[ taskname ] = results[ backbone_task ]
            break

for key in results_collection.keys():
    print key + ": " + str(results_collection[ key ])


