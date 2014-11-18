# Using a complete population dump that includes historical data,
# map gene flow over time.
#
# The script will automatically figure out how many clades there are
# at any given time 

# Written in Python 2.7
# RCK
# 6-22-14

# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
import math
from optparse import OptionParser
import sys
import time

# Set up options
usage = """usage: %prog [options] historical_populationdump last_lineage_population_snapshot
"""

parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true", 
                  dest = "debug_messages", default = False, 
                  help = "print debug messages to stdout")

parser.add_option("-o", "--output", dest="output", type="string", 
                  help = "output to file, not STDOUT")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters
historical = args[0]
snapshot = args[1]

### pop file format declaration
pop_format = {}

### organisms
organisms = {}

#################################################
def populate_lineage(org_id):
    #print organisms[org_id]
    if (len(organisms[org_id]['parents']) == 0):
        print "I AM AT THE BOTTOM OF THE BARREL AND HAVE NO PARENTS - WHAT HOW COULD THIS HAPPEN"
        # fine, somehow we made it to the bottom of the barrel without ever having ascertained what the fuck lineage this is.
        organisms[org_id]['lineage'] = {-1: 1}
        organisms[org_id]['lineage_populated'] = True
        return

    for parent_id in organisms[org_id]['parents']:
        #print parent_id
        if parent_id in organisms:
            # this data isn't there when I needed it, so go fill it in
            if not organisms[parent_id]['lineage_populated']:
                #print "------->" + str(parent_id)
                populate_lineage(parent_id)

            # now fill in the data
            for key in organisms[parent_id]['lineage']:
                #print "<------|"
                if not key in organisms[org_id]['lineage']:
                    organisms[org_id]['lineage'][key] = 0

                if key == -1:
                    organisms[org_id]['lineage'][key] = 1
                else:
                    organisms[org_id]['lineage'][key] += organisms[parent_id]['lineage'][key]
        else:
            organisms[org_id]['lineage'][-1] = 1
    organisms[org_id]['lineage_populated'] = True     

    #print organisms[org_id]       
 
    return
#################################################

# populate the historical population set   
if historical[-3:] == ".gz":
    fd = gzip.open(historical)
else:
    fd = open(historical)

if options.verbose:
    print "Processing: '" + historical + "'"

site_count_dict = {}

for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        if line[:7] == "#format":
            pop_format = {line[8:].split(' ')[i]: i for i in range(len(line[8:].split(' ')))}
            print pop_format
        continue

    line = line.split(' ')
    organisms[int(line[pop_format["id"]])] = {'id': int(line[pop_format["id"]]), 'parents': [int(val) for val in line[pop_format['parents']].split(',') if val != "(none)"], 'depth': line[pop_format["depth"]], 'lineage': {}, 'num_units': int(line[pop_format["num_units"]]), 'lineage_populated': False }

    #print int(line[pop_format["id"]])    

fd.close()

# apply the known lineages
if snapshot[-3:] == ".gz":
    fd = gzip.open(snapshot)
else:
    fd = open(snapshot)

if options.verbose:
    print "Processing: '" + snapshot + "'"

site_count_dict = {}

for line in fd:
    line = line.strip()
    if len(line) == 0 or line[0] == "#":
        if line[:7] == "#format":
            pop_format = {line[8:].split(' ')[i]: i for i in range(len(line[8:].split(' ')))}
            print pop_format
        continue

    line = line.split(' ')
    try:
        if "," in line[pop_format["lineage"]]: # if there is bad data, skip it.
            #print line[pop_format["lineage"]]
            continue
        if not int(line[pop_format["id"]]) in organisms:
            print "WHAT ID NOT FOUND"
        else:
            print "YESSS"
        organisms[int(line[pop_format["id"]])]['lineage'] = {line[pop_format["lineage"]]: 1}
    except Exception as poop:
        #print "WHAT"
        #print poop
        continue

fd.close()

for org_id in sorted(organisms, reverse=True): # start at the latest organisms
    if organisms[org_id]['num_units'] == 0: # no living organisms, skip it
        continue
    
    populate_lineage(org_id)
    
    print organisms[org_id]




#for org in organisms:




#if options.output:

#    fpo = open( options.output, 'w' )

#    fpo.write(  "#phylogenetic depth abundances (columns) and by sample (rows)\n" )
#    for abundances in count_arrays:
#        fpo.write(  ",".join( [ str(abundance) for abundance in abundances ] ) )
#        fpo.write( "\n" )

#    fpo.close()

#else:
#    print "#phylogenetic depth abundances (columns) and by sample (rows)"
#    for abundances in count_arrays:
#        print ",".join( [ str(abundance) for abundance in abundances ] )

