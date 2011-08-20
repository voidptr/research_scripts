# Run combinatoric scripts, unfolded based on the parameters in a file

# Written in Python 2.7
# RCK
# 8-18-11

from optparse import OptionParser
import commands


# Set up options
usage = """usage: %prog [options] "script_name $ $ $" dynamic_parameters_file

eg. %% python run_combinatoric_scripts.py "python script.py -o directory/ $ $ --level=$" dynamic_params.txt

the dynamic parameters file format should be as follows

  ## comment
  ## item1, item2, item3
  parameter1, parameter2, parameter3
  parameter1, parameter2.1, parameter3

where each item is just sequentially stuck in place of a $
so there had better be the same number of $s as parameters in the dynamic parameters file
Also, no funny business with quotes or commas. I don't account for those.

"""
parser = OptionParser(usage)
## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

template = args[0] ## the template

dynamic_parameters_filename = args[1] ## the dynamic parameters file

slot_count = template.count('$')


## read the dynamic parameters file
dynamic_parameters_file = open( dynamic_parameters_filename )
for line in dynamic_parameters_file:
    line = line.strip()

    if (len(line) == 0 or line[0] == '#'): ## skip comments and blank lines
        continue

    line = line.split(',') ## split the line on commas
    line = [ val.strip() for val in line ] ## take out the spaces inherent

    assert (len(line) == slot_count) ## this had better be right

    command = template ## start fresh

    for i in range(slot_count):
        command = command.replace("$",line[i],1) ## go one at a time

    print "Running: " + command
    (status, output) = commands.getstatusoutput( command )
    #if status > 0:
    #   print "command failed: " + command
    print output
    
dynamic_parameters_file.close()

