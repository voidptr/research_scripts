#!/usr/bin/python

# Extract single column to csv

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import string
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] expression FileA/ColumnA [FileB/ColumnB ...]

Expression must be in the form of a + b * c and will be executed in whatever 
order python does things with eval. variables MUST be a, b, c, d, (... etc.) and a, b, c 
is the order in which the columns are listed"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("-s", "--separator", dest = "separator", help = "Data separator (default ' ')")
parser.add_option("-f", "--files", action = "store_true", dest = "files",
                  default = False, help = "files, not columns")
parser.add_option("-c", "--columns", action = "store_true", dest = "columns",
                  default = False, help = "use columns")
parser.add_option("-i", "--inputfile", dest = "inputfilename", help = "input filename")

## fetch the args
(options, args) = parser.parse_args()

if not options.separator:
    options.separator = " "

if options.columns and options.files:
    parser.error("--columns and --files are mutually exclusive")

if options.columns and not options.inputfilename:
    parser.error("--columns requires --inputfile being defined")

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## expression to perform
expr = args[0]

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


elif options.files:

    ## columns to combine
    files = args[1:]
    handles = []
    for inputfilename in files:
        if options.verbose:
            print "Processing: '" + inputfilename + "'"

        if inputfilename[-3:] == ".gz":
            handles.append( gzip.open(inputfilename) )
        else:
            handles.append( open(inputfilename, mode='r') )

    while(1): ## loop!

        lines = []
        outputs = []
        for handle in handles:
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
            lines.append(line)

        if len(lines) < len(handles):
            if options.debug_messages:
                print "Not enough lines retrieved"
            break

        if options.debug_messages:
            print lines

        for i in range(0, len(lines[0])):
            eval_string = expr ## new string!

            for (index, variable) in zip( range(0,len(lines)), string.letters ):
                if options.debug_messages:
                    print index
                    print variable
                    print i

                value = lines[index][i]
                if value == "nan": ## THIS IS HALF-ASSED
                    value = "0"
                eval_string = string.replace( eval_string, variable, value )

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

