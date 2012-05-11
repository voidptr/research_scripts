# Calculate the population entropy over time.

# Written in Python 2.7
# RCK
# 4-17-12

import gzip
import numpy as np
import math
from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] populationdump1 [popdump2 ...]

Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose!")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--num_cpu", dest="num_cpu_col", type="int", 
                  help = "Column of num_cpu")
parser.add_option("--seq", dest="seq_col", type="int", 
                  help = "Column of seq")
parser.add_option("--fitness", dest="fitness_col", type="int", 
                  help = "Column of fitness")

parser.add_option("-o", "--output", dest="output", type="string", 
                  help = "output to file, not STDOUT")

parser.add_option("--output_probabilities", dest="output_probabilities", type="string", 
                  help = "output site probabilities to file as well")



## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")
    
### Fetch Parameters
inputfilenames = args[0:]

## parameter defaults
num_cpu_col = 5
if options.num_cpu_col:
    num_cpu_col = options.num_cpu_col

seq_col = 17
if options.seq_col:
    seq_col = options.seq_col

fitness_col = 10
if options.fitness_col:
    fitness_col = options.fitness_col

## regular defaults
alphabet = "abcdefghijklmnopqrstuvwxyz"
alphabet_len = len(alphabet)

all_entropies = [] # 2D array
mean_fitnesses = []
max_fitnesses = []

all_probabilities = [] ## 3D array
for inputfilename in inputfilenames:
    
    if inputfilename[-3:] == ".gz":
        fd = gzip.open(inputfilename)
    else:
        fd = open(inputfilename)

    if options.verbose:
        print "Processing: '" + inputfilename + "'"

    sequences = []
    fitnesses = []

    for line in fd:
        line = line.strip()
        if len(line) == 0 or line[0] == "#":
            continue

        line = line.split(' ')

        num_cpu = int(line[num_cpu_col - 1])

#        if num_cpu == 0: ## we only want the live ones.
#            continue

        for i in range(0, num_cpu): ## normalize by organism       
            sequences.append( line[seq_col - 1] )
            fitnesses.append( float(line[fitness_col - 1]) )

    fd.close()

    site_ct = len(sequences[0]) ## grab a length. They should be fixed-length.
    seq_ct = float(len(sequences))

    ## calculate probabilities
    # 2D array with probabilities per-site/per-letter
    probabilities = [ [ 0 for i in range(0, len(alphabet)) ] for i in range(0, site_ct ) ]  
    for site in range(0, site_ct):
        for letter in range(0, alphabet_len):
            ct = sum( [ 1 for seq in sequences if seq[site] == alphabet[letter] ] )
            probabilities[site][letter] = ct / seq_ct

    ## calculate entropies per site
    entropies = [ 0 for i in range(0, site_ct) ]
    for site in range(0, site_ct):
        H = 0; # entropy
        for letter in range(0, alphabet_len):
            if probabilities[site][letter] > 0:
                H = H - ( probabilities[site][letter] * math.log(probabilities[site][letter], alphabet_len ) ) 

        entropies[site] = H        
    
    all_entropies.append(entropies)

    if options.output_probabilities:
        all_probabilities.append( probabilities )


    mean_fitnesses.append( np.mean( fitnesses ) )
    max_fitnesses.append( max( fitnesses ) )

if options.output_probabilities:
    fpop = open( options.output_probabilities, 'w' )

    fpop.write(  "#probabilities by letter (column) by site (26 columns) and by sample (rows)\n" )
    for probabilities in all_probabilities:
        fpop.write( ",".join( [ ",".join( [ str(prob) for prob in site_probs ] ) for site_probs in probabilities ] ) )
        fpop.write( "\n" )

    fpop.close()

if options.output:

    fpo = open( options.output, 'w' )

    fpo.write( "#mean_fitnesses by sample\n" )
    fpo.write( ",".join( [ str(fitness) for fitness in mean_fitnesses ] ) )
    fpo.write( "\n" )

    fpo.write(  "#max_fitnesses by sample\n" )
    fpo.write(  ",".join( [ str(fitness) for fitness in max_fitnesses ] ) )
    fpo.write( "\n" )

    fpo.write(  "#entropies by site (columns) and by sample (rows)\n" )
    for entropies in all_entropies:
        fpo.write(  ",".join( [ str(entropy) for entropy in entropies ] ) )
        fpo.write( "\n" )

    fpo.close()

else:

    print "#mean_fitnesses by sample"
    print ",".join( [ str(fitness) for fitness in mean_fitnesses ] )

    print "#max_fitnesses by sample"
    print ",".join( [ str(fitness) for fitness in max_fitnesses ] )

    print "#entropies by site (columns) and by sample (rows)"
    for entropies in all_entropies:
        print ",".join( [ str(entropy) for entropy in entropies ] )
