#!/usr/bin/python

# Takes a mutational landscaping run from a single ancestor, and outputs a histogram of what sites had a certain mutational effect. 

# Written in Python 2.7
# RCK
# 5-11-12


import gzip
import math
import numpy
import itertools
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] mutation_landscape.dat

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--ancestor", dest = "ancestor", type = "string", 
                  help = "Compare mutants against an ancestor")
parser.add_option("--ancestor_task1", action = "store_true", dest = "ancestor_task1",
                  default = False, help = "Ancestor performs task1")
parser.add_option("--ancestor_task2", action = "store_true", dest = "ancestor_task2",
                  default = False, help = "Ancestor performs task2")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

## defaults
ancestor_fitness_col = 8
ancestor_task1_col = 10
ancestor_task2_col = 11
ancestor_seq_col = 14 ## what is it?

landscape_fitness_col = 2
landscape_task1_col = 3
landscape_task2_col = 4
landscape_seq_col = 6

## input filename
mutation_landscape_file = args[0]

## calibrate ancestor information
ancestor_fitness = 0
ancestor_task1 = 0
ancestor_task2 = 0

## default alphabet length
alphabet_length = 27

if options.ancestor:
    ancestor_file = options.ancestor
    ## read ancestor
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

        ancestor_seq = line[ ancestor_seq_col - 1 ]

    fd.close()
else:
    if options.ancestor_task1:
        ancestor_task1 = 1

    if options.ancestor_task2:
        ancestor_task2 = 1
    
    if mutation_landscape_file[-3:] == ".gz":
        fd = gzip.open(mutation_landscape_file)
    else:
        fd = open(mutation_landscape_file)

    ## deduce the canonical sequence, since it is not provided
    sequences = []
    ancestor_seq = ""
    seq_ct = 0
    for line in fd:
        line = line.strip() ## strip off the end of line crap

        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue

        line = line.split() ## break the line up on spaces

        sequences.append( line[ landscape_seq_col - 1 ] )
        seq_ct += 1

        if seq_ct > alphabet_length:
            break ## done

    fd.close()

    for pos in range( len( sequences[0] ) ):
        characters = {}

        for seq in sequences:
            if seq[pos] in characters:
                ancestor_seq += seq[pos]
                break
            else:
                characters[seq[pos]] = 1 ## assign it

    if options.verbose:
        print ancestor_seq

## read mutation landscape
if mutation_landscape_file[-3:] == ".gz":
    fd = gzip.open(mutation_landscape_file)
else:
    fd = open(mutation_landscape_file)

ancestor_seq_len = len(ancestor_seq)
positions_does_t1 = [0] * ancestor_seq_len
positions_does_t2 = [0] * ancestor_seq_len 
positions_does_both = [0] * ancestor_seq_len
positions_changed_t1 = [0] * ancestor_seq_len
positions_changed_t2 = [0] * ancestor_seq_len
positions_changed_both = [0] * ancestor_seq_len

positions_gained_t1 = [0] * ancestor_seq_len
positions_gained_t2 = [0] * ancestor_seq_len
positions_gained_both = [0] * ancestor_seq_len

positions_lost_t1 = [0] * ancestor_seq_len
positions_lost_t2 = [0] * ancestor_seq_len
positions_lost_both = [0] * ancestor_seq_len

positions_gained_t1_lost_t2 = [0] * ancestor_seq_len
positions_lost_t1_gained_t2 = [0] * ancestor_seq_len

for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        continue

    line = line.split() ## break the line up on spaces

    f =  float(line[ landscape_fitness_col - 1 ] ) 
    t1 = int( line[ landscape_task1_col - 1] )
    t2 = int( line[ landscape_task2_col - 1] )
    seq = line[ landscape_seq_col - 1 ]

    for pos in range( ancestor_seq_len ):
        if ancestor_seq[pos] != seq[pos]:
            mutation_location = pos
            break

    if f > 0:

        if t1:
            positions_does_t1[pos] += 1
        if t2:
            positions_does_t2[pos] += 1
        if t1 and t2:
            positions_does_both[pos] += 1

        if t1 != ancestor_task1:
            positions_changed_t1[pos] += 1
            if t1 > ancestor_task1:
                positions_gained_t1[pos] += 1
            else:
                positions_lost_t1[pos] += 1

        if t2 != ancestor_task2:
            positions_changed_t2[pos] += 1
            if t2 > ancestor_task2:
                positions_gained_t2[pos] += 1
            else:
                positions_lost_t2[pos] += 1

        if t1 != ancestor_task1 and t2 != ancestor_task2:
            positions_changed_both[pos] += 1

            if t1 > ancestor_task1 and t2 > ancestor_task2:
                positions_gained_both[pos] += 1
            elif t1 < ancestor_task1 and t2 < ancestor_task2:
                positions_lost_both[pos] += 1
            elif t1 < ancestor_task1 and t2 > ancestor_task2:
                positions_lost_t1_gained_t2[pos] += 1
            elif t1 > ancestor_task1 and t2 < ancestor_task2:
                positions_gained_t1_lost_t2[pos] += 1

fd.close()

## print the histograms

print ",".join( [ str(val) for val in  positions_does_t1 ] )
print ",".join( [ str(val) for val in  positions_does_t2 ] )
print ",".join( [ str(val) for val in  positions_does_both ] )

print ",".join( [ str(val) for val in  positions_changed_t1 ] )
print ",".join( [ str(val) for val in  positions_changed_t2 ] )
print ",".join( [ str(val) for val in  positions_changed_both ] )

print ",".join( [ str(val) for val in  positions_gained_t1 ] )
print ",".join( [ str(val) for val in  positions_gained_t2 ] )
print ",".join( [ str(val) for val in  positions_gained_both ] )

print ",".join( [ str(val) for val in  positions_lost_t1 ] )
print ",".join( [ str(val) for val in  positions_lost_t2 ] )
print ",".join( [ str(val) for val in  positions_lost_both ] )

print ",".join( [ str(val) for val in  positions_gained_t1_lost_t2 ] )
print ",".join( [ str(val) for val in  positions_lost_t1_gained_t2 ] )

