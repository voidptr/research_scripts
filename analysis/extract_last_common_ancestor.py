# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
import math
from optparse import OptionParser
import os

# Set up options
usage = """usage: %prog [options] lineage.dat stats.dat 

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")

parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

parser.add_option("--last_ancestor_depth_column", dest="last_ancestor_depth_col", type="int", 
                  help = "In stats.dat - defaults to 10")

parser.add_option("--depth_col", dest="depth_col", type="int", 
                  help = "In lineage.dat - defaults to 4")

parser.add_option("--ancestor_without_fluct", dest="ancestor_without_fluct",action="store_true", default=False, 
                  help = "Pull out the ancestor nearest the last common that did NOT do the fluctuating task. In lineage.dat - column w/ this info defaults to 11")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters
lineage_file = args[0]
stats_file = args[1]

## parameter defaults
depth_col = 4
if options.depth_col:
    depth_col = options.depth_col

last_ancestor_depth_col = 10
if options.last_ancestor_depth_col:
    last_ancestor_depth_col = options.last_ancestor_depth_col

ancestor_without_fluct_col = 11

## read the stats file
cmd = "tail -1 %s" % stats_file
line = os.popen(cmd).read()

line = line.strip()
line = line.split()
last_ancestor_depth = int(line[ last_ancestor_depth_col - 1 ])

if lineage_file[-3:] == ".gz":
    fd = gzip.open(lineage_file)
else:
    fd = open(lineage_file)

stored_line = ""
for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        continue

    line_bits = line.split(' ')

    depth = int(line_bits[depth_col - 1])
   
    if int(line_bits[ ancestor_without_fluct_col - 1 ]) == 0: # this is ghetto
        stored_line = line

    if depth == last_ancestor_depth:
        if options.ancestor_without_fluct:
            if len(stored_line) > 0: 
                print stored_line
            break ## have it or not, we're done. :/

        print line
        break

fd.close()







