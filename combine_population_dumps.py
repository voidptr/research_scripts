# Combine detail population dumps 

# Written in Python 2.7
# RCK
# 2-24-12

import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] -o file.spop [file.spop ...]

Permitted types for outfile are png, pdf, ps, eps, and svg
"""

parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-o","--outputfile", dest = "outputfile", type="string",
                  help = "Direct the output to a file. Otherwise, to standard out.")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## population dump(s)
population_dump_files = args[0:]

outfilehandle = None
if options.outputfile:
    outfilehandle = open(options.outputfile, 'w')

## loading the population dumps
ids = set() 

files_by_key = {}
for filename in population_dump_files:
    update = filename.split("-")[1].split(".")[0] ## pull the update out of the filename :/filename
    files_by_key[ int(update) ] = filename

keys = files_by_key.keys()
keys.sort()
keys.reverse()

if options.debug_messages:
    print files_by_key.keys()
    print keys

comments = []
comments_closed = False
for update in keys:
    filename = files_by_key[ update ]
    if options.verbose:
        print "Processing: '" + filename + "'"

    if filename[-3:] == ".gz":
        fd = gzip.open(filename)
    else:
        fd = open(filename)

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            if comments_closed:
                continue
            else:
                comments.append( line )

        bits = line.split(" ") ## break the line up on spaces

        org_id = bits[0]
       
        if org_id not in ids:
            ids.add( org_id )
            if options.outputfile:
                outfilehandle.write( line + "\n" )
            else:
                print line

    fd.close()

    comments_closed = True
        
if options.outputfile:
    outfilehandle.close()



