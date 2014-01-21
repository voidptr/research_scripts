# Extract clade information from detail population dumps 

# Written in Python 2.7
# RCK
# 2-23-12


import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] clade_ids file.spop [file.spop ...]

Permitted types for outfile are png, pdf, ps, eps, and svg
Make sure the order the .spop files in the increasing order!!!
"""

parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-m","--dominant_column", dest = "dominant_column", type="int",
                  help = "We are reading a dominant.dat file and here's the column we want to use")
parser.add_option("-o","--outputfile", dest = "outputfile", type="string",
                  help = "Direct the output to a file. Otherwise, to standard out.")

#parser.add_option("--dimensionality", dest = "dimensionality", type="int",
#                  help = "treat input data as one or two dimensional")
#parser.add_option("-s","--separator", dest = "separator", type="string",
#                  help = "the separator (comma, or space)")
#parser.add_option("--name", dest = "column_name", help = "name of the data")
#parser.add_option("-c", "--calculate_stats", action = "store_true", dest = "calc_stats",
#                  default = False, help = "in a given file, calculate the stats of the column and print those out instead")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## cladeIDs 
clade_ID_file = args[0]

## population dump(s)
population_dump_files = args[1:]

if clade_ID_file[-3:] == ".gz":
    fd = gzip.open(clade_ID_file)
else:
    fd = open(clade_ID_file)

if options.verbose:
    print "Processing: '" + clade_ID_file + "'"

## loading the clade ids file
clade_ids = {}
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    if (options.dominant_column):
        line = line.split(" ")
        clade_ids[ line[ options.dominant_column-1 ] ] = 0
    else:
        clade_ids[ line ] = 0

fd.close()

## loading the population dump files
organisms = {}
def find_clade_recursively( org_id ):
    if org_id not in organisms: ## this will only ever happen if we've hit the root, the virgin birth, the parent of -1
        return "0" ## the root clade is always 0, I can only assume

    organism = organisms[ org_id ] ## fetch it ONCE
    clade_id = organism[ 1 ]
    if clade_id == -1: ## no clade, keep looking down
        clade_id = find_clade_recursively( organism[ 0 ] )
        organisms[ org_id ] = ( organism[ 0 ], clade_id, organism[ 2 ] )

    return clade_id

outfilehandle = None
if options.outputfile:
    outfilehandle = open(options.outputfile, 'w')

for dump in population_dump_files:

    update = dump.split("-")[1].split(".")[0] ## pull the update out of the filename :/

    ## reset organisms
    organisms = {}

    if options.verbose:
        print "Processing: '" + dump + "'"

    ## ok, this shit needs to be done twice, because the organisms aren't in order.

    ## get all the organisms and their parents in here.
    if dump[-3:] == ".gz":
        fd = gzip.open(dump)
    else:
        fd = open(dump)

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        line = line.split(" ") ## break the line up on spaces

        org_id = line[0]
        parent_id = line[3]
        currentlyliving_ct = line[4]
        everlived_ct = line[5] 
        clade_id = -1 ## there will be many assigned this, because the file isn't in order
        
        if org_id in clade_ids: ## I'm a clade founder! holy shit!
            clade_id = org_id
        elif parent_id in organisms: ## not a clade founder, inherit my parent's clade, if they exist.
            clade_id = organisms[ parent_id ][ 1 ]
        organisms[ org_id ] = (parent_id, clade_id, currentlyliving_ct) ## create the new entry
           
    fd.close()

    ## now recurse as required in order to get the -1 ones in there.
    if dump[-3:] == ".gz":
        fd = gzip.open(dump)
    else:
        fd = open(dump)

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        line = line.split(" ") ## break the line up on spaces

        org_id = line[0]

        organism = organisms[ org_id ] ## fetch it ONCE

        if organism[ 1 ] == -1: ## no clade assigned
            clade_id = find_clade_recursively( organism[ 0 ] )
            organisms[ org_id ] = ( organism[ 0 ], clade_id, organism[ 2 ] )

    fd.close()

    clades = {}
    for value in organisms.itervalues():
        if value[1] not in clades:
            clades[ value[1] ] = 0
        clades[ value[1] ] += int(value[ 2 ])

    parts = []
    for (clade_id, count) in clades.items():
        parts.append( str(clade_id) )
        parts.append( str(count) )

    outstring = update + " " + str(len(clades)) + " " + " ".join(parts)

    if options.outputfile:
        outfilehandle.write( outstring + "\n" )
    else:
        print outstring
        
if options.outputfile:
    outfilehandle.close()

#print organisms



