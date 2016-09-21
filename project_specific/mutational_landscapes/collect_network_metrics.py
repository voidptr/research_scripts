#!/usr/bin/python

# survey a mutational network

# Written in Python 2.7
# RCK
# 3-24-11


from graph_tool.all import *
from optparse import OptionParser
import numpy as np
import random
import math

# Set up options
usage = """usage: %prog [options] <network.xml>

script must be run from the same directory as Avida."""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
                  
parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
                  
## fetch the args
(options, args) = parser.parse_args()
if len(args) < 1:
    parser.error("Not enough arguments.\n"+usage)

networkfile = args[0]
###### LOAD THE NETWORK FILE

g = load_graph(networkfile, "gt")
#print "LOADED"
#print g
 
#num_cpus = g.vertex_properties["num_cpus"]
fitnesses = g.vertex_properties["fitnesses"]
steps = g.vertex_properties["steps"]
alleles_cluster = g.vertex_properties['alleles_cluster']
phenotypes = g.vertex_properties["phenotypes"]
surveyed = g.vertex_properties["surveyed"]
num_cpus = g.vertex_properties["num_cpus"]
  
deg = g.degree_property_map("in")

ancestors = []
for v in g.vertices():
    if alleles_cluster[v] == -1:
        ancestors.append( v )
        
if len(ancestors) == 1:
    ancestor = ancestors[0]
else: ## find the dominant, and treat them as the ancestor for neutrality purposes. ## TODO talk to charles about the implications.
    ancestor = None
    dom_ct = -1
    for a in ancestors:
        if num_cpus[a] > dom_ct:
            ancestor = a
            dom_ct = num_cpus[a]
            
            
    
ancestor_fitness = fitnesses[ancestor]
ancestor_phenotype = phenotypes[ancestor]    
ancestor_log_fitness = math.log(ancestor_fitness) 

print "# Proportion of mutants separated by neutrality, and again by same or different phenotype from ancestor"
print "# One line per surveyed ancestor"
print "# num_cpus, lethal, deleterious, neutral, beneficial, same_p_lethal, same_p_deleterious, same_p_neutral, same_p_beneficial, diff_p_lethal, diff_p_deleterious, diff_p_neutral, diff_p_beneficial"

for v in g.vertices():        
    #print num_cpus[v]
    if (surveyed[v] == True): ## we are a mutant parent
        neighbor_total = float(v.out_degree())

        fitness_cts        = {'l':0, 'd':0, 'n':0, 'b':0}
        same_phenotype_cts = {'l':0, 'd':0, 'n':0, 'b':0}
        diff_phenotype_cts = {'l':0, 'd':0, 'n':0, 'b':0}

        for n in v.all_neighbours():
            if fitnesses[n] == 0: ## dead
                fitness_cts['l'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['l'] += 1
                else:
                    same_phenotype_cts['l'] += 1
                
            elif fitnesses[n] >= (ancestor_fitness * .99) and fitnesses[n] <= (ancestor_fitness * 1.01) : ## neutral and nearly neutral
                fitness_cts['n'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['n'] += 1
                else:
                    same_phenotype_cts['n'] += 1

            elif fitnesses[n] < ancestor_fitness: ## deleterious
                fitness_cts['d'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['d'] += 1
                else:
                    same_phenotype_cts['d'] += 1

            elif fitnesses[n] > ancestor_fitness: ## beneficial
                fitness_cts['b'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['b'] += 1
                else:
                    same_phenotype_cts['b'] += 1
       
                                 
        line_fit = ",".join( str(fitness_cts[key]/neighbor_total) for key in ['l','d','n','b']  )                    
        line_samep = ",".join( str(same_phenotype_cts[key]/neighbor_total) for key in ['l','d','n','b']  )
        line_diffp = ",".join( str(diff_phenotype_cts[key]/neighbor_total) for key in ['l','d','n','b']  )
       
        full_line = ",".join( [str(num_cpus[v]), line_fit, line_samep, line_diffp])
   
        print full_line
