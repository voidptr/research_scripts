
import glob
import os
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] 

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

## fetch the args
(options, args) = parser.parse_args()

primaries = ['c','n','p']
secondaries = ['s','i']
tertiaries = ['0','1','2','3']

command = "screen -dmS %s_%s_%s bash -c \"mkdir populations/; for i in %s*_%s*_????%s?; do if [ ! -e \$i.tar.gz ] ; then mkdir \$i/data/populations/; mv \$i/data/detail* \$i/data/populations/; mv \$i/data/populations/ ./populations/\$i; tar -cvf \$i.tar.gz \$i ; else echo \\\"Skipping \$i\\\" ; fi; done\""

for prim in primaries:
    for sec in secondaries:
        for tern in tertiaries:
            spec_command = command % (prim, sec, tern, prim, sec, tern)
            print spec_command
            os.popen(spec_command)

