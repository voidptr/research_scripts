#!/usr/bin/python

# combine columns in a set of files according to a given mathematical expression.

# Reworked to behave more flexibly
# RCK
# 2-16-16


import gzip
import string
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] expression FileA ColumnA [FileB ColumnB ...]

Expression must be in the form of a + b * c and will be executed in whatever 
order python does things with eval. variables MUST be a, b, c, d, (... etc.) and a, b, c 
is the order in which the columns are listed

Column numbers are 0-indexed"""

parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-s", "--separator", dest = "separator", help = "Data separator (default ' ')")


## fetch the args
(options, args) = parser.parse_args()

if not options.separator:
    options.separator = " "

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## expression to perform
expr = args[0]

if (len(args[1:]) % 2 != 0):
    parser.error("Incorrect file and column specification. Each file must have a column")


files_and_columns = collections.OrderedDict()
for (i in range(1, len(args[]), 2)):
    files_and_columns[args[i]] = args[i+1]


handles = []
for inputfilename in files_and_columns.keys():
    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    if inputfilename[-3:] == ".gz":
        handles.append( gzip.open(inputfilename) )
    else:
        handles.append( open(inputfilename, mode='r') )

while(1): ## loop!

    values = []
    outputs = []
    for handle, key in zip(handles, files_and_columns.keys()):
        line = ""
        while(1): ## loop until I get a line with data in it
            line = handle.readline()
            #print line
            if not line:
                if options.debug_messages:
                    print "readline() failed"
                break
            line = line.strip() ## strip off the end of line crap
            if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
                continue
            break

        if not line:
            if options.debug_messages:
                print "No Line Found"
            break
                    
        line = line.split(options.separator) ## break the line up on separator
        values.append(line[ int(files_and_columns[key]) ])



    if len(values) < len(handles):
        if options.debug_messages:
            print "Not enough lines retrieved"
        break

    if options.debug_messages:
        print values

    eval_string = expr ## new string!
    
    for letter_index in range(26):
        eval_string = string.replace( eval_string, string.letters[letter_index], values[letter_index] )
                    

    if options.debug_messages:
        print eval_string

    output = ""
    try:
        output = eval( eval_string )
    except ZeroDivisionError:
        output = 0

    outputs.append(output)

    outputs = [ str(val) for val in outputs ]

    print options.separator.join(outputs)

for handle in handles:
    handle.close()




if options.columns:

    inputfilename = options.inputfilename

    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        line = line.split(options.separator) ## break the line up on spaces

        eval_string = expr ## new string!
    
        for (col, variable) in zip(columns, string.letters):
            value = line[ col - 1 ]
            eval_string = string.replace( eval_string, variable, value )

            if options.debug_messages:
                print evaluate_string

            output = eval( eval_string )

            print output

        fd.close()