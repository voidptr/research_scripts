#!/usr/bin/python

# Extract a series of metrics from the mutational landscape information.

# Written in Python 2.7
# RCK
# 3-24-11


import gzip
import math
import numpy
import itertools
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] ancestor.dat mutation_landscape.dat

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")


## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

## defaults
ancestor_fitness_col = 8
ancestor_task1_col = 10
ancestor_task2_col = 11

landscape_fitness_col = 2
landscape_task1_col = 3
landscape_task2_col = 4

## input filename
ancestor_file = args[0]
mutation_landscape_file = args[1]

## read ancestor
ancestor_fitness = -1.0
ancestor_task1 = -1
ancestor_task2 = -1

if ancestor_file[-3:] == ".gz":
    fd = gzip.open(ancestor_file)
else:
    fd = open(ancestor_file)

for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.split() ## break the line up on spaces

    ancestor_fitness = float(line[ ancestor_fitness_col - 1 ])    
    ancestor_task1 = int( line[ ancestor_task1_col - 1] )
    ancestor_task2 = int( line[ ancestor_task2_col - 1] )


fd.close()

## read mutation landscape
landscape_fitnesses = []
landscape_task1s = []
landscape_task2s = []

landscape_viable_fitnesses = []
landscape_viable_task1s = []
landscape_viable_task2s = []


if mutation_landscape_file[-3:] == ".gz":
    fd = gzip.open(mutation_landscape_file)
else:
    fd = open(mutation_landscape_file)

landscape_does_t1 = 0
landscape_does_t2 = 0
landscape_does_both = 0
landscape_changed_t1 = 0
landscape_changed_t2 = 0
landscape_changed_both = 0

landscape_gained_t1 = 0
landscape_gained_t2 = 0
landscape_gained_both = 0

landscape_lost_t1 = 0
landscape_lost_t2 = 0
landscape_lost_both = 0

landscape_gained_t1_lost_t2 = 0
landscape_lost_t1_gained_t2 = 0

for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.split() ## break the line up on spaces

    f =  float(line[ landscape_fitness_col - 1 ] ) 
    t1 = int( line[ landscape_task1_col - 1] )
    t2 = int( line[ landscape_task2_col - 1] )

    landscape_fitnesses.append( f )   
    landscape_task1s.append ( t1 )
    landscape_task2s.append ( t2 )

    if f > 0:
        landscape_viable_fitnesses.append( f )   
        landscape_viable_task1s.append ( t1 )
        landscape_viable_task2s.append ( t2 )

        if t1:
            landscape_does_t1 += 1
        if t2:
            landscape_does_t2 += 1
        if t1 and t2:
            landscape_does_both += 1

        if t1 != ancestor_task1:
            landscape_changed_t1 += 1
            if t1 > ancestor_task1:
                landscape_gained_t1 += 1
            else:
                landscape_lost_t1 +=1

        if t2 != ancestor_task2:
            landscape_changed_t2 += 1
            if t2 > ancestor_task2:
                landscape_gained_t2 += 1
            else:
                landscape_lost_t2 +=1

        if t1 != ancestor_task1 and t2 != ancestor_task2:
            landscape_changed_both += 1

            if t1 > ancestor_task1 and t2 > ancestor_task2:
                landscape_gained_both += 1
            elif t1 < ancestor_task1 and t2 < ancestor_task2:
                landscape_lost_both +=1
            elif t1 < ancestor_task1 and t2 > ancestor_task2:
                landscape_lost_t1_gained_t2 +=1
            elif t1 > ancestor_task1 and t2 < ancestor_task2:
                landscape_gained_t1_lost_t2 +=1






fd.close()

## calculate the metrics

# frac viable
frac_viable = len(landscape_viable_fitnesses) / float( len(landscape_fitnesses) )

frac_does_task1 = landscape_does_t1 / float( len(landscape_fitnesses) )
frac_does_task2 = landscape_does_t2 / float( len(landscape_fitnesses) )
frac_does_both = landscape_does_both / float( len(landscape_fitnesses) )

frac_changed_task1 = landscape_changed_t1 / float( len(landscape_fitnesses) )
frac_changed_task2 = landscape_changed_t2 / float( len(landscape_fitnesses) )
frac_changed_both = landscape_changed_both / float( len(landscape_fitnesses) )

frac_gained_task1 = landscape_gained_t1 / float( len(landscape_fitnesses) )
frac_gained_task2 = landscape_gained_t2 / float( len(landscape_fitnesses) )
frac_gained_both = landscape_gained_both / float( len(landscape_fitnesses) )

frac_lost_task1 = landscape_lost_t1 / float( len(landscape_fitnesses) )
frac_lost_task2 = landscape_lost_t2 / float( len(landscape_fitnesses) )
frac_lost_both = landscape_lost_both / float( len(landscape_fitnesses) )

frac_gained_task1_lost_task2 = landscape_gained_t1_lost_t2 / float( len(landscape_fitnesses) )
frac_lost_task1_gained_task2 = landscape_lost_t1_gained_t2 / float( len(landscape_fitnesses) )


## commented out because I don't have the proper analysis information (missing the phase and the background they are in)
#frac_pos_fitness_effect
#frac_neg_fitness_effect
#frac_neut_fitness_effect

#print "#FracViable, FracDoesTask1, FracDoesTask2, FracDoesBoth, FracChangedTask1, FracChangedTask2, FracChangedBoth"

print "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s" % \
   (frac_viable, 
    frac_does_task1, 
    frac_does_task2, 
    frac_does_both, 
    frac_changed_task1, 
    frac_changed_task2, 
    frac_changed_both,
    frac_gained_task1,
    frac_gained_task2,
    frac_gained_both,
    frac_lost_task1,
    frac_lost_task2,
    frac_lost_both,
    frac_gained_task1_lost_task2,
    frac_lost_task1_gained_task2)

