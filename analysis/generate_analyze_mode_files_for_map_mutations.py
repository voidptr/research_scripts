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
usage = """usage: %prog [options] last_common_ancestor.dat [... last_common_ancestor.dat] 

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")

parser.add_option("--seq_col", dest="seq_col", type="int", 
                  help = "defaults to 13")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters

## parameter defaults
seq_col = 13 
if options.seq_col:
    seq_col = options.seq_col

inputfilenames = args[0:]

sequences = []
for inputfilename in inputfilenames:

    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    for line in fd:
        line = line.strip() 
        if len(line) == 0 or line[0] == "#":
            continue

        line_bits = line.split(' ')

        seq = line_bits[seq_col - 1]
        sequences.append(seq)

    fd.close()

analyze_string = """
PURGE_BATCH
LOAD_SEQUENCE %s
RECALCULATE
DETAIL %s/%s_%s.dat length fitness task.0 task.1 total_task_count sequence
"""

instructions = "abcdefghijklmnopqrstuvwxyzA"
instr_set_len = len(instructions)

for seq_index in range(0, len(sequences)):                    

    seq = sequences[ seq_index ]
    outdir = "mutations_%s" % seq_index

    for pos in range(0, len(seq)):
        for inst_index in range(0, instr_set_len):
            mod_seq = seq
            instr = instructions[ inst_index ]
            
            mod_seq = "%s%s%s" % ( seq[:pos], instr, seq[pos+1:] )

#            mod_seq[pos] = instr

            print analyze_string % (mod_seq, outdir, pos, instr)

