#!/usr/bin/python
### copy the data from somewhere

import os
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] source_directory 
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-g", "--gunzip", action = "store_true", dest="gunzip", 
                  default=False, help="Gunzip the data")

## fetch the args
(options, args) = parser.parse_args()

if len(args) < 1:
    parser.error("Not enough arguments.")

source_dir = args[0]

print "Copying from %s to ./data/" % source_dir
os.popen("cp -r %s ./data/" % source_dir)

if options.gunzip:
    print "Gunzipping."
    os.popen("gunzip -r ./data/")

