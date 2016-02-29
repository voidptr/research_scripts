# Extract the number of a particular instruciton in a given population file.

# Written in Python 2.7
# RCK
# 1-17-16


import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] instruction_code infile

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-p", "--proportion", action = "store_true", dest = "proportion",
                  default = False, help = "print the proportion instead of the raw count.")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

instruction_code = args[0]

count_col_id = 6
sequence_col_id = 17

inputfilename = args[1]

if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
else:
    fd = open(inputfilename)

if options.verbose:
    print "Processing: '" + inputfilename + "'"

total = 0;
proportions = 0.0;
orgs = 0;
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    whole_line = line

    line = line.split() ## break the line up on spaces

    org_count = int(line[count_col_id - 1])
    sequence = line[sequence_col_id - 1]
    
    prop = float(sequence.count(instruction_code)) / len(sequence)
    
    proportions += prop
    
    total += sequence.count(instruction_code) * org_count
    orgs += org_count

fd.close()

if (options.proportion):
    print proportions/orgs
else:
    print total/orgs
