# Generate a summary file from a run_list 

# Written in Python 2.7
# RCK
# 8-21-11

#import sys
#sys.path.append('../common modules and helper scripts')

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] run_directory output_directory scripts_directory
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 3:
    parser.error("incorrect number of arguments")

title = args[0]

pngs = args[1:]

print "<p>" + title + "</p>"
for png in pngs:
    print "<img src=" + png + " width=200 >"

print "<br>"


