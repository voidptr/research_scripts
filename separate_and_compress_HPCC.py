#!/usr/bin/python

import glob
import os
from optparse import OptionParser
import sys

# Set up options
usage = """usage: %prog [options] 

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--simple", action = "store_true", dest = "simple",
                  default = False, help = "do only the simple tar.gz-ing. No cleanup.")

parser.add_option("-p", "--primaries", dest="primaries", help="primary designators: contr,noreward,punish etc.")
parser.add_option("-s", "--secondaries", dest="secondaries", help="primary designators: sep,int etc.")
parser.add_option("-t", "--tertiaries", dest="tertiaries", help="tertiary designators: 1,2,3,4 etc.")

## fetch the args
(options, args) = parser.parse_args()

if options.simple:
    command = """for i in *_??????
do
    if [ ! -e $i.tar.gz ]
    then
        tar -cvf $i.tar.gz $i
    else
        echo Skipping $i
    fi
done
"""
    print "#Copy and Paste the below:"
    print command
    #os.popen(command)
else:

    primaries = ['c','n','p']
    if options.primaries:
        primaries = options.primaries.split(',')

    secondaries = ['s','i']
    if options.secondaries:
        secondaries = options.secondaries.split(',')

    tertiaries = ['0','1','2','3','4','5','6','7','8','9']
    if options.tertiaries:
        tertiaries = options.tertiaries.split(',')

    command = "screen -dmS %s_%s_%s bash -c \"mkdir populations/; mkdir individual_modularity/ ; mkdir physical_modularity_stats__organisms ; mkdir two_task_only_individual_modularity; mkdir two_task_only_individual_modularity__organisms ; for i in %s*_%s*_????%s?; do if [ ! -e \$i.tar.gz ] ; then mkdir \$i/data/populations/; mv \$i/data/detail* \$i/data/populations/; mv \$i/data/populations/ ./populations/\$i; mkdir \$i/data/individual_modularity/; mv \$i/data/individual_modularity*.dat* \$i/data/individual_modularity/; mv \$i/data/individual_modularity/ ./individual_modularity/\$i ; mv \$i/data/physical_modularity_stats__organisms/ ./physical_modularity_stats__organisms/\$i; mv \$i/data/two_task_only_individual_modularity ./two_task_only_individual_modularity/\$i ; mv \$i/data/two_task_only_individual_modularity__organisms ./two_task_only_individual_modularity__organisms/\$i ; tar -cvf \$i.tar.gz \$i ; else echo \\\"Skipping \$i\\\" ; fi; done ; echo \\\"Waiting 10 seconds for excess tertiaries to clear.\\\" ; sleep 10; rm *\\\?.tar.gz\""

    for prim in primaries:
        for sec in secondaries:
            for tern in tertiaries:
                spec_command = command % (prim, sec, tern, prim, sec, tern)
                print spec_command
                os.popen(spec_command)

