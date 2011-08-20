# Do Runs

# Written in Python 2.7
# RCK
# 3-28-11


import os
import shutil
import commands
import gzip
from optparse import OptionParser
import sys

# Set up options
usage = """usage: %prog [options] seed_range_start seed_range_stop config_directory output_dir avida_parameters
"""
parser = OptionParser(usage)
  #parser.add_option("-q", "--quiet", action = "store_false", dest = "verbose",
#                default = True, help = "don't print processing messages to stdout")
  #parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
#                default = False, help = "print debug messages to stdout")

## fetch the args
#(options, args) = parser.parse_args()

## parameter error
if len(sys.argv) < 6:
    parser.error("incorrect number of arguments")

## seed_range_start
seed_range_start = int(sys.argv[1])

## seed_range_stop
seed_range_stop = int(sys.argv[2])

## config_directory
config_directory = sys.argv[3]

## output directory
output_directory = sys.argv[4]

## avida command
avida_command = sys.argv[5]


## avida command
avida_params = ""
if len(sys.argv) > 6:
    avida_params = " ".join(sys.argv[6:])

errors = []

for i in range(seed_range_start, seed_range_stop+1):
    outdir = output_directory + '_' + str(i)
    try:
        shutil.copytree( config_directory, outdir )
    except (IOError, os.error), why:
        errors.append((config_directory, outdir, str(why)))
    # catch the Error from the recursive copytree so that we can
    # continue with other files
    except Error, err:
        errors.extend(err.args[0])

if errors:
    print errors
    exit()

currdir = os.getcwd()
for j in range(seed_range_start, seed_range_stop+1):
    outdir = output_directory + '_' + str(j)
    command = avida_command + ' -s ' + str(j) + ' ' + avida_params
    print "Running: " + command
    os.chdir( currdir )
    os.chdir( outdir )
    (status, output) = commands.getstatusoutput( command )
    if status > 0:
        errors.append("avida command failed: " + command)
        
if errors:
    print errors
        