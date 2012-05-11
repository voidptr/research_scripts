# Read the figures in a directory, and stack them up.

# Written in Python 2.7
# RCK
# 5-09-11

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] heading filename1 [filename2 ...]

"""
parser = OptionParser(usage)
#parser.add_option("-g", "--graph", action = "store_true", dest = "showgraph",
#                  default = False, help = "show the graph")
#parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
#                  default = True, help = "don't print processing messages to stdout")
#parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
#                  default = False, help = "print debug messages to stdout")

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

## heading
heading = args[0]

## filename(s)
inputfilenames = args[1:]

print "<p>"
print heading
print "</p>"

for inputfilename in inputfilenames:
    print "<img src=\"./" + inputfilename + "\" />" 

