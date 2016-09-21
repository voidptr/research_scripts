#!/usr/bin/python

# Extract single column to csv, and possibly perform some operations to it.

# Written in Python 2.7
# RCK
# 3-24-11

import os
import glob
import sys
import subprocess
import time
from graph_tool.all import *
from optparse import OptionParser
import random

import math

# Set up options
usage = """usage: %prog [options] <popfile> <network_output>

script must be run from the same directory as Avida."""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")

parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--keepfiles", action = "store_true", dest = "keepfiles",
                  default = False, help = "Keep the intermediate data files around.")
                  
parser.add_option("--compress", action = "store_true", dest = "compress",
                  default = False, help = "Compress the output network file.")
### Collecting Data
parser.add_option("-s", "--steps", dest = "steps", type="int", default = 10,
                  help = "Distance to explore from live genomes")
                  
parser.add_option("-d", "--dominant", action = "store_true", dest = "dominant",
                  default = False, help = "only dominant")
parser.add_option("-p", "--phenotype", action = "store_true", dest = "phenotype",
                  default = False, help = "Match on Phenotype as well.")

### Avida Environments
parser.add_option("-e", "--environment", dest = "envfile", type="string", default = "environment.cfg",
                  help = "Environment file to pass in to Avida")

### Sampling
parser.add_option("--skimsample", dest = "skimsample", type="float", default = None,
                  help = "Reduce the exhaustive sampling to this fraction. Occurs at Avida level.")

parser.add_option("--skimsamplereductionfactor", dest = "skimsamplereductionfactor", type="float", default = None,
                  help = "Reduce the skim sampling factor by a continuously reducing operation. Occurs at Avida level.")

parser.add_option("--bloomsample", dest = "bloomsample", type="float", default = None,
                  help = "Fraction of neutral/beneficial mutants to follow to the next step. Probabilistic.")
parser.add_option("--sample", dest = "sample", type="float", default = None,
                  help = "Sample some fraction of the population. Analogous to bloom, but takes place at Avida level. Probabilistic.")

parser.add_option("-t", "--trim", dest = "trim", type="int", default = None,
                  help = "Trim the neutrals we're sampling. Takes place at Avida level. Cut-off. Terrible way to do it.")


### Error Checking
parser.add_option("-n", "--neutral", action = "store_true", dest = "neutralfile",
                  default = False, help = "just read a file with neutral steps")


"""
Neutrals Only, or All.

Default behavior (without --complete):
Gather every mutant, put only proceed to the next stage with neutrals.
Non-neutrals are gathered and retained as the edge-border around the neutral
network.

--complete:
Gather every mutant, and place all gathered (regardless of neutrality) on the
block for following.
"""
parser.add_option("--complete", action = "store_true", dest = "complete",
                  default = False, help = "Gather the entire landscape, not just neutrals.")

parser.add_option("--interconnect", action = "store_true", dest = "interconnect",
                  default = False, help = "Interconnect all the alleles in a cluster")

# TODO
#parser.add_option("-n", "--nearly_neutral", dest = "nearly_neutral",
#                  action = "store_true", default=False,
#                  help = "Allow mildly deleterious mutants to be treated as part of the neutral network.")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")


popfile = args[0]
outfile = args[1]

datadir = outfile+"_data"

## TODO - think about making this a graph property
genotypes = {}
neutral_network = Graph(directed=False)

steps = neutral_network.new_vertex_property("int")
neutral_network.vertex_properties['steps'] = steps

fitnesses = neutral_network.new_vertex_property("double")
neutral_network.vertex_properties['fitnesses'] = fitnesses

phenotypes = neutral_network.new_vertex_property("int")
neutral_network.vertex_properties['phenotypes'] = phenotypes

num_cpus = neutral_network.new_vertex_property("int")
neutral_network.vertex_properties['num_cpus'] = num_cpus

alleles_cluster = neutral_network.new_vertex_property("int")
neutral_network.vertex_properties['alleles_cluster'] = alleles_cluster

surveyed = neutral_network.new_vertex_property("bool")
neutral_network.vertex_properties['surveyed'] = surveyed

def runProcess(cmd):
    p = subprocess.Popen(cmd.split(' '), stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
    return iter(p.stdout.readline, b'')

def prepare_analyze_cfg(step, part, mutants_count, dominant, popfile, sample, trim, skimsample):
    if options.verbose:
        print "#########################################################"
        print "AVIDA PROCESSING -- Part", part

    if step == 0:
        load_step = """
        LOAD %s
        RECALCULATE
        %s ## dominant
        FILTER num_cpus > 0
        FILTER fitness > 0.0
         """ % (popfile, dominant)
    else:
        load_step = """
        LOAD_SEQUENCE_FILE neutral_mutants_step_%s.seq
        %s ## sample
        """ % (step, sample)

    analyze_file = """
    ################################################################
    # THIS FILE IS GENERATED BY collect_and_analyze_mut_network.py
    ################################################################

    PURGE_BATCH

    %s ## loading

     %s #trim?

    ECHO ##################
    ECHO Part %s of %s
    ECHO ##################
    REMOVE_TOP %s
    KEEP_TOP 1000
    RECALCULATE
    FILTER fitness > 0.0
    MAP_SINGLE_STEP_NETWORK single_step/ %s

    """ % (load_step,
           trim,
           part, int(math.ceil(mutants_count/1000)),
           (part * 1000), 
           skimsample)

    ## file is re-generated for each step and part.
    if options.verbose:
        print "#########################################################"
    analyze = open("analyze.cfg", 'w')
    analyze.write(analyze_file)
    analyze.close()

def run_avida():
    if options.verbose:
       print "#########################################################"
       print "AVIDA RUN"

    #time.sleep(3)

    ## run the Avida command. This may take a while.
    command = "./avida -v4 -a -set DATA_DIR "+datadir+ " -set ENVIRONMENT_FILE "+options.envfile
    if options.verbose:
       print command
       print "---------------------------------------------------------"

    for line in runProcess(command):
        print "    ", line

    if options.verbose:
       print "#########################################################"

def add_vertex(sequence, fitness, phenotype, step, living,
#               color,
               cluster=-1, parent=None):
    ## nothing should ever come in here that isn't already in the network
    v = neutral_network.add_vertex()

    genotypes[sequence] = v
    fitnesses[v] = fitness
    phenotypes[v] = phenotype
    steps[v] = step
    num_cpus[v] = living
    alleles_cluster[v] = cluster
    #color_data[v] = color

    if parent:
        neutral_network.add_edge(genotypes[parent], v)
    #else:
    #    surveyed[v] = True

    return v

def match_phenotype(phen, neut_phen):

    if options.phenotype:
        if (phen & neut_phen < neut_phen):
            return False

    return True

def collect_data():

    dominant = ""
    if options.dominant:
        dominant = "FIND_GENOTYPE num_cpus ## find the most abundant one, for now"

    trim = ""
    if options.trim:
        trim = "KEEP_TOP " + str(options.trim)

    sample = ""
    if options.sample:
        sample = "SAMPLE_GENOTYPES " + str(options.sample)       
        
    skimsample= ""
    skimreduction = 1.0    
    if options.skimsample:
        skimsample = str(options.skimsample)       
        skimreduction = options.skimsample ## reduction begins with the skim sample at step 0

    ## set up the initial data directories
    print os.popen("rm -rf ./"+datadir+"/").read()

    mutants_count = 3600 ## initializing this for convenience when loading from a pop file
    for i in range(options.steps):

        if options.verbose:
            print "#########################################################"
            print "NEUTRAL NETWORK -- Step", i

        if options.dominant and i == 0:
            mutants_count = 1

        ## SPLIT UP THE INPUT FILES INTO CHUNKS AVIDA CAN DIGEST
        for part in range(int(math.ceil(mutants_count/1000))+1):

            ## PREPARE THE ANALYZE.CFG FILE

            if options.skimsamplereductionfactor: ## reduce the starting point of the skim sample
                skimsample = str(skimreduction)
                skimreduction = skimreduction * options.skimsamplereductionfactor            

            prepare_analyze_cfg(i, part, mutants_count, dominant, popfile, sample, trim, skimsample)

            ## RUN AVIDA
            run_avida()

        #### DONE WITH AVIDA

        ## move the data around to be read by Avida next time around.
#        print os.popen("mkdir ./"+datadir+"/raw_mutants_step"+str(i+1)+"/").read()
        print os.popen("mv ./"+datadir+"/single_step ./"+datadir+"/raw_mutants_step"+str(i+1)+"/").read()

        glob_string = "./"+datadir+"/raw_mutants_step"+str(i+1)+"/mut_map.*.dat"

        if options.debug_messages:
           print "#########################################################"
           print glob_string
           print glob.glob(glob_string)

        neutrals = open("neutral_mutants_step_"+str(i+1)+".seq", 'w')

        neutral_fitness = sys.maxint
        neutral_phenotype = sys.maxint
        if options.verbose:
           print "#########################################################"
           print "Reading %s produced mutants from AVIDA run." % len(glob.glob(glob_string))


        ## LOOP THROUGH EVERY LANDSCAPED MUTANT (PRODUCED BY AVIDA) AND ADD THEM
        ## TO THE NETWORK GRAPH
        mutants_count = 0
        for inputfilename in sorted(glob.glob(glob_string)):
            fd = open(inputfilename)

            if options.verbose or options.debug_messages:
                print "Processing: '" + inputfilename + "'"

            parent = ""
            currentLocus = "-1"
            snps = []
            alleles_cluster_num = 0

            for line_orig in fd:

                ## prepare the line
                line = line_orig.strip() ## strip off the end of line crap
                if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
                    continue
                linebits = line.split(" ")

                locus = linebits[2]
                fitn = float(linebits[4])
                living = int(linebits[5])
                phen = int("".join(linebits[6:-1]),2)
                seq = linebits[-1]

                ##### WE'RE THE FIRST LINE ##### - We will spawn every mutant here.
                ##### We belong in every cluster, but also no cluster, really.
                if linebits[1] == '-1': ## parent
                    neutral_fitness = fitn ## everything is judged from the step's originating mutant.
                    neutral_phenotype = phen
                    parent = seq

                    if options.verbose:
                        print "PARENT: ", neutral_fitness, parent

                    # we're new! -- only occurs in STEP 0, FWIW
                    if parent not in genotypes:
                        v = add_vertex(seq, fitn, phen, -1, living)

                    ## we're a parent, so we'll catch everyone.
                    surveyed[genotypes[seq]] = True

                ##### OK, NOT THE PARENT, JUST A MUTANT THAT WE HAVE
                else: ## not parent

                    ## new locus. Clear the snps, and update the alleles_cluster number.
                    if currentLocus != locus:
                        currentLocus = locus
                        snps = []
                        alleles_cluster_num += 1

                    ## We're a brand new mutant! :D
                    if seq not in genotypes:
                        v = add_vertex(seq, fitn, phen, i, living, alleles_cluster_num, parent)
                        surveyed[v] = False

                        ## We're neutral (fitness and phenotypic(if desired) OR we're grabbing everyone,
                        ## so we're going to keep following this thread.
                        if ((fitn >= neutral_fitness and
                             match_phenotype(phen, neutral_phenotype)) or
                             options.complete == True):

                            if options.bloomsample: 
                                if random.random() < options.bloomsample: ##
                                    neutrals.write(seq+"\n")
                                    mutants_count += 1
                            else:
                                neutrals.write(seq+"\n")
                                mutants_count += 1

                    ## we've come across this genotype before, but not via this parent.
                    elif parent != seq: ## Seen, but not the parent
                        ## connect me with this parent.
                        neutral_network.add_edge(genotypes[parent], genotypes[seq])

                    if options.interconnect:
                        edges = []
                        for snp in snps: ## apply edges to all previously found polymorphisms
                            edges.append((genotypes[snp], genotypes[seq]))
                        neutral_network.add_edge_list(edges)

                    snps.append(seq)

            fd.close()
        neutrals.close()

    ## ok, now pickle the network graph
    if options.verbose:
           print "#########################################################"
           print "Saving the network graph to", outfile
    neutral_network.save(outfile, "gt")

    if options.compress:
        print os.popen("tar -zcvf "+outfile+".tgz "+outfile).read()
        print os.popen("rm "+outfile).read()
    
    if not options.keepfiles:
        print os.popen("rm -rf ./"+datadir+"/").read()

def neutral_file():

    fd = open(popfile)

    if options.verbose or options.debug_messages:
        print "Processing: '" + inputfilename + "'"

    parent = ""
    currentLocus = "-1"
    snps = []
    alleles_cluster_num = 0

    for line_orig in fd:

        ## prepare the line
        line = line_orig.strip() ## strip off the end of line crap
        if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
            continue
        linebits = line.split(" ")

        locus = linebits[2]
        fitn = float(linebits[4])
        living = int(linebits[5])
        phen = int("".join(linebits[6:-1]),2)
        seq = linebits[-1]

        ##### WE'RE THE FIRST LINE ##### - We will spawn every mutant here.
        ##### We belong in every cluster, but also no cluster, really.
        if linebits[1] == '-1': ## parent
            neutral_fitness = fitn ## everything is judged from the step's originating mutant.
            neutral_phenotype = phen
            parent = seq

            if options.verbose:
                print "PARENT: ", neutral_fitness, parent

            # we're new! -- only occurs in STEP 0, FWIW
            if parent not in genotypes:
                v = add_vertex(seq, fitn, phen, -1, living)

            ## we're a parent, so we'll catch everyone.
            surveyed[genotypes[seq]] = True

        ##### OK, NOT THE PARENT, JUST A MUTANT THAT WE HAVE
        else: ## not parent

            ## new locus. Clear the snps, and update the alleles_cluster number.
            if currentLocus != locus:
                currentLocus = locus
                snps = []
                alleles_cluster_num += 1

            ## We're a brand new mutant! :D
            if seq not in genotypes:
                v = add_vertex(seq, fitn, phen, 0, living, alleles_cluster_num, parent)
                surveyed[v] = False


            ## we've come across this genotype before, but not via this parent.
            elif parent != seq: ## Seen, but not the parent
                ## connect me with this parent.
                neutral_network.add_edge(genotypes[parent], genotypes[seq])

            if options.interconnect:
                edges = []
                for snp in snps: ## apply edges to all previously found polymorphisms
                    edges.append((genotypes[snp], genotypes[seq]))
                neutral_network.add_edge_list(edges)

            snps.append(seq)
    fd.close()

    ## ok, now pickle the network graph
    if options.verbose:
           print "#########################################################"
           print "Saving the network graph to", outfile
    neutral_network.save(outfile, "gt")

if options.neutralfile:
    neutral_file()
else:
    collect_data()
