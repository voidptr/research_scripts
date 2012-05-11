# Run combinatoric scripts, unfolded based on the parameters in a file

# Written in Python 2.7
# RCK
# 8-18-11

from optparse import OptionParser
import commands


# Set up options
usage = """usage: %prog [options] "script_name $1 $2 $3" dynamic_parameters_file ## define the template in bash form

eg. %% python run_combinatoric_scripts.py "python script.py -o directory/ $1 $2 --level=$3" dynamic_params.txt

the dynamic parameters file format should be as follows

  ## comment
  ## $1 $2 $3
  parameter1 parameter2 parameter3
  parameter1 parameter2.1 parameter3

No funny business with quotes or commas. I don't account for those.

"""
parser = OptionParser(usage)
## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

template = args[0] ## the template

dynamic_parameters_filename = args[1] ## the dynamic parameters file


## read the dynamic parameters file
dynamic_parameters_file = open( dynamic_parameters_filename )
for parameters in dynamic_parameters_file:
    parameters = parameters.strip()

    if (len(parameters) == 0 or parameters[0] == '#'): ## skip comments and blank lines
        continue

    parameters = parameters.split() ## split on the spaces.

    command = template ## start fresh
    for i in range(len(parameters)):
        pattern = "$" + str(i+1)
        command = command.replace(pattern, parameters[i]) ## replace all instances of $1, $2 with the ones defined. Essentially, do the bash parameter script preprocess. :/

    print "Running: " + command
    (status, output) = commands.getstatusoutput( command )
    #if status > 0:
    #   print "command failed: " + command
    print output
    
dynamic_parameters_file.close()

