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
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
                  
parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
                  
#parser.add_option("--tasks", dest = "tasks", type="int", default = 9,
#                  help = "Number of possible task.")                  
## fetch the args
(options, args) = parser.parse_args()
if len(args) < 1:
    parser.error("Not enough arguments.\n"+usage)

networkfile = args[0]
###### LOAD THE NETWORK FILE

#possible_phenotypes = 2**options.tasks

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
print "# num_cpus, lethal, deleterious, neutral, beneficial, same_p_lethal, same_p_deleterious, same_p_neutral, same_p_beneficial, diff_p_lethal, diff_p_deleterious, diff_p_neutral, diff_p_beneficial, whitenodes_lethal, whitenodes_deleterious, whitenodes_neutral, whitenodes_beneficial, blacknodes_lethal, blacknodes_deleterious, blacknodes_neutral, blacknodes_beneficial, phenotypic_entropy"

for v in g.vertices():        
    #print num_cpus[v]
    if (surveyed[v] == True): ## we are a mutant parent
        neighbor_total = float(v.out_degree())

        fitness_cts        = {'l':0, 'd':0, 'n':0, 'b':0}
        same_phenotype_cts = {'l':0, 'd':0, 'n':0, 'b':0}
        diff_phenotype_cts = {'l':0, 'd':0, 'n':0, 'b':0}

        ## Network Density
        ## living nodes that connect to other living nodes of the same phenotype
        whitenodes_cts = {'l': 0, 'd': 0, 'n':0, 'b':0}
        ## Unrealized Network Robustness
        ## living nodes that connect to non-living nodes of the same phenotype
        blacknodes_cts = {'l': 0, 'd': 0, 'n':0, 'b':0}
        ## Network Evolvability
        ## entropy of edges going to different phenotypes
        phenotype_cts = { ancestor_phenotype: 0 }        

        for n in v.all_neighbours():
            if fitnesses[n] == 0: ## dead
                fitness_cts['l'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['l'] += 1
                    if phenotypes[n] not in phenotype_cts:
                        phenotype_cts[phenotypes[n]] = 1
                    else:
                        phenotype_cts[phenotypes[n]] += 1
                else:
                    same_phenotype_cts['l'] += 1
                    phenotype_cts[ancestor_phenotype] += 1
                    if num_cpus[v] > 0:
                        if num_cpus[n] > 0:
                            whitenodes_cts['l'] += 1
                        else:
                            blacknodes_cts['l'] += 1                
                
            elif fitnesses[n] >= (ancestor_fitness * .99) and fitnesses[n] <= (ancestor_fitness * 1.01) : ## neutral and nearly neutral
                fitness_cts['n'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['n'] += 1
                    if phenotypes[n] not in phenotype_cts:
                        phenotype_cts[phenotypes[n]] = 1
                    else:
                        phenotype_cts[phenotypes[n]] += 1
                else:
                    same_phenotype_cts['n'] += 1
                    phenotype_cts[ancestor_phenotype] += 1                    
                    if num_cpus[v] > 0:
                        if num_cpus[n] > 0:
                            whitenodes_cts['n'] += 1
                        else:
                            blacknodes_cts['n'] += 1
                            
            elif fitnesses[n] < ancestor_fitness: ## deleterious
                fitness_cts['d'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['d'] += 1
                    if phenotypes[n] not in phenotype_cts:
                        phenotype_cts[phenotypes[n]] = 1
                    else:
                        phenotype_cts[phenotypes[n]] += 1
                else:
                    same_phenotype_cts['d'] += 1
                    phenotype_cts[ancestor_phenotype] += 1
                    if num_cpus[v] > 0:
                        if num_cpus[n] > 0:
                            whitenodes_cts['d'] += 1
                        else:
                            blacknodes_cts['d'] += 1
                            
            elif fitnesses[n] > ancestor_fitness: ## beneficial
                fitness_cts['b'] += 1
                if phenotypes[n] != ancestor_phenotype:
                    diff_phenotype_cts['b'] += 1

                    if phenotypes[n] not in phenotype_cts:
                        phenotype_cts[phenotypes[n]] = 1
                    else:
                        phenotype_cts[phenotypes[n]] += 1
                else:
                    same_phenotype_cts['b'] += 1
                    phenotype_cts[ancestor_phenotype] += 1
                    if num_cpus[v] > 0:
                        if num_cpus[n] > 0:
                            whitenodes_cts['b'] += 1
                        else:
                            blacknodes_cts['b'] += 1       

        phenos = [0]
        for key in phenotype_cts:
            if key == ancestor_phenotype:
                phenos[0] = phenotype_cts[key]
            else:
                phenos.append(phenotype_cts[key])

        ents = []
        for ct in phenos:
            prob = ct/neighbor_total
            if prob > 0:
                inf = math.log(prob, 2)
            else:
                inf = 0
            ent = prob * inf
            ents.append(ent)

#        print phenos
#        print ents


        ## ENTROPY
        total_entropy = -1 * sum(ents)        

        ## Portion of entropy contributed by the ancestor phenotype
        ancestor_bits = -1 * ents[0]        
        
        ## Portion of entropy contributed by the non-ancestor phenotypes         
        remaining_bits = -1 * sum(ents[1:])

        ## bits devoted - the ratio of bits that are from colored        
        if sum(ents) == 0:
            total_entropy_ratio_devoted = 1
        else:
            total_entropy_ratio_devoted = (sum(ents[1:])/sum(ents))        
        
        ## Entropy per-bit, normalized by message size 
        metric = -1 * sum(ents)/math.log(neighbor_total,2)

        ## E_k - total entropy * the fraction of nodes that make it colored
        ## Normalizes the colored portion of the entropy by the number of contributing nodes
        total_ek = -1 * (sum(ents) * sum(phenos[1:]))/neighbor_total
        
        ## mE_k - metric E_k - average per-bit entropy, grabbing the portion of it created by the fraction of colored nodes.
        metric_ek = (metric * sum(phenos[1:]))/neighbor_total
#        print "metric Ek",  (metric * sum(phenos[1:]))/neighbor_nodes

        ## E_k_c - colored portion of entropy (remaining bits) * number of colored nodes, all divided by the total number of nodes
        ## Normalizes the colored portion of the entropy by the number of contributing nodes
        total_ekc = -1 * (sum(ents[1:]) * sum(phenos[1:]))/neighbor_total
 
        ## mE_k_c - colored portion of entropy (remaining bits), metricised * number of colored nodes, all divided by the total number of nodes
        ## Normalizes the colored portion of the entropy by the number of contributing nodes
        metric_ekc = -1 * ( (metric * total_entropy_ratio_devoted) * sum(phenos[1:]))/neighbor_total 
        
        
        entropy_vals = [total_entropy,
                        ancestor_bits,
                        remaining_bits,
                        total_entropy_ratio_devoted,                                       
                        metric,
                        total_ek,
                        metric_ek,
                        total_ekc,
                        metric_ekc]

        ct = 0;
        for x in entropy_vals:
            print ct, x
            ct += 1                         

                            
        line_fit   = ",".join( str(fitness_cts[key]/neighbor_total) for key in ['l','d','n','b']  )                    
        line_samep = ",".join( str(same_phenotype_cts[key]/neighbor_total) for key in ['l','d','n','b']  )
        line_diffp = ",".join( str(diff_phenotype_cts[key]/neighbor_total) for key in ['l','d','n','b']  )

        line_whitenodes = ",".join( str(whitenodes_cts[key]/neighbor_total) for key in ['l','d','n','b']  )       
        line_blacknodes = ",".join( str(blacknodes_cts[key]/neighbor_total) for key in ['l','d','n','b']  ) 
        
        line_phen_entropy = ",".join( [str(x) for x in entropy_vals])

        full_line = ",".join( [str(num_cpus[v]), line_fit, line_samep, 
                               line_diffp, line_whitenodes, line_blacknodes,
                               line_phen_entropy])

   
        print full_line
