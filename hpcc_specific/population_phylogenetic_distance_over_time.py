# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] populationdump1 [popdump2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--num_cpu", dest="num_cpu_col", type="int", 
                  help = "Column of num_cpu")
parser.add_option("--phylo_depth", dest="phylo_depth_col", type="int", 
                  help = "Column of phylogenetic depth")

parser.add_option("-o", "--output", dest="output", type="string", 
                  help = "output to file, not STDOUT")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters
inputfilenames = args[0:]

## parameter defaults
num_cpu_col = 5
if options.num_cpu_col:
    num_cpu_col = options.num_cpu_col

phylo_depth_col = 14
if options.phylo_depth_col:
    phylo_depth_col = options.phylo_depth_col

## fetch the histograms
count_arrays = []
count_dicts = []

for inputfilename in inputfilenames:
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    site_count_dict = {}

    for line in fd:
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            continue

        line = line.split(' ')

        phylo_depth = int(line[phylo_depth_col - 1])
        num_cpu = int(line[num_cpu_col - 1])

        if num_cpu == 0: ## we only want the live ones.
            continue

        # create dictionary of values : non-zero counts
        if phylo_depth in site_count_dict:
            site_count_dict[phylo_depth] += num_cpu
        else:
            site_count_dict[phylo_depth] = num_cpu

    fd.close()

    count_dicts.append(site_count_dict)

max_size = max([max(d.keys()) for d in count_dicts])
num_files = len(inputfilenames)

count_arrays = [[0] * (max_size + 1) for i in range(num_files)]
for i in range(0, num_files):
    for key in count_dicts[i]:
        count_arrays[i][key] = count_dicts[i][key]


if options.output:

    fpo = open( options.output, 'w' )

    fpo.write(  "#phylogenetic depth abundances (columns) and by sample (rows)\n" )
    for abundances in count_arrays:
        fpo.write(  ",".join( [ str(abundance) for abundance in abundances ] ) )
        fpo.write( "\n" )

    fpo.close()

else:
    print "#phylogenetic depth abundances (columns) and by sample (rows)"
    for abundances in count_arrays:
        print ",".join( [ str(abundance) for abundance in abundances ] )

