# Take an Avida detail file and split it into individual organism files 

# Written in Python 2.7
# RCK
# 1-19-12


import gzip
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] infile [outfile]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
                  default = True, help = "don't print processing messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
#parser.add_option("-m", "--median", action="store_true", dest = "median",
#                default = False, help = "calculate and display median")
#parser.add_option("-o", "--medianonly", action="store_true", dest = "median_only",
#                  default = False, help = "calculate and display median ONLY")
#parser.add_option("-l", "--logscale", action="store_true", dest = "log_scale",
#                  default = False, help = "display y-axis as log scale")
#parser.add_option("-x", "--xlabel", dest="x_label", type="string", 
#                  help="X-axis Label")
#parser.add_option("-y", "--ylabel", dest="y_label", type="string", 
#                  help="Y-axis Label")
#parser.add_option("-t", "--title", dest="title", type="string", 
#                  help="Graph Title")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
        parser.error("incorrect number of arguments")

## input filenames
inputfilename = args[0]

if len(args) > 1:
    outfilename = args[1]
else:
    outfilename = ""

if inputfilename[-3:] == ".gz":
    fd = gzip.open(inputfilename)
    outputfilename_template = inputfilename[0:-3]
else:
    fd = open(inputfilename)
    outputfilename_template = inputfilename

file_id = 0
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue
    
    bits = line.split(' ')
    if int(bits[4]) == 0:
        continue
    
    outputfilename = outfilename + outputfilename_template + "_" + str(file_id) + ".spop"

    fout = open(outputfilename, 'w')
    fout.write( line )
    fout.close()

    file_id += 1
    
fd.close()
                                                                    
