#!/usr/bin/python

# Extract single column to csv, and possibly perform some operations to it.

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

networkfile = args[0]

## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")
 
def calc_stats():
    g = load_graph(networkfile, "gt")
    print "LOADED"
    print g
 
    #num_cpus = g.vertex_properties["num_cpus"]
    fitnesses = g.vertex_properties["fitnesses"]
    steps = g.vertex_properties["steps"]
    alleles_cluster = g.vertex_properties['alleles_cluster']
    phenotypes = g.vertex_properties["phenotypes"]
      
    deg = g.degree_property_map("in")

    ### Find the home vertex. It should be right in the beginning
    ancestor = None
    for v in g.vertices():
        if alleles_cluster[v] == -1:
            ancestor = v
            break
        
    ancestor_fitness = fitnesses[ancestor]
    ancestor_phenotype = phenotypes[ancestor]    
    ### Edgeyness
    
    lethal_fit_ct = 0
    deleterious_fit_ct = 0
    neutral_fit_ct = 0
    beneficial_fit_ct = 0
    
    nothing_phen_ct = 0
    deleterious_phen_ct = 0
    neutral_phen_ct = 0
    beneficial_phen_ct = 0
    
    lethal_degrees = []
    deleterious_degrees = []
    neutral_degrees = []
    beneficial_degrees = []
    
    lethal_degrees_part = {'lethal': [], 'deleterious': [], 'neutral': [], 'beneficial': [] }
    deleterious_degrees_part = {'lethal': [], 'deleterious': [], 'neutral': [], 'beneficial': [] }
    neutral_degrees_part = {'lethal': [], 'deleterious': [], 'neutral': [], 'beneficial': [] }
    beneficial_degrees_part = {'lethal': [], 'deleterious': [], 'neutral': [], 'beneficial': [] }
    
    node_ct = g.num_vertices()

    
    for v in g.vertices():
   
        if fitnesses[v] == 0:
            lethal_fit_ct += 1
            lethal_degrees.append(v.out_degree())

            lct = 0
            dct = 0
            nct = 0
            bct = 0
            for n in v.all_neighbours():
                if fitnesses[n] == 0:
                    lct += 1
                elif fitnesses[n] < ancestor_fitness:
                    dct += 1
                elif fitnesses[n] == ancestor_fitness:
                    nct += 1
                elif fitnesses[n] > ancestor_fitness:
                    bct += 1
                    
            lethal_degrees_part['lethal'].append(lct)
            lethal_degrees_part['deleterious'].append(dct)
            lethal_degrees_part['neutral'].append(nct)
            lethal_degrees_part['beneficial'].append(bct)
            
        elif fitnesses[v] < ancestor_fitness:
            deleterious_fit_ct += 1
            deleterious_degrees.append(v.out_degree())
            
            lct = 0
            dct = 0
            nct = 0
            bct = 0
            for n in v.all_neighbours():
                if fitnesses[n] == 0:
                    lct += 1
                elif fitnesses[n] < ancestor_fitness:
                    dct += 1
                elif fitnesses[n] == ancestor_fitness:
                    nct += 1
                elif fitnesses[n] > ancestor_fitness:
                    bct += 1
                    
            deleterious_degrees_part['lethal'].append(lct)
            deleterious_degrees_part['deleterious'].append(dct)
            deleterious_degrees_part['neutral'].append(nct)
            deleterious_degrees_part['beneficial'].append(bct)
            
        elif fitnesses[v] == ancestor_fitness:
            neutral_fit_ct += 1
            neutral_degrees.append(v.out_degree())
            
            lct = 0
            dct = 0
            nct = 0
            bct = 0
            for n in v.all_neighbours():
                if fitnesses[n] == 0:
                    lct += 1
                elif fitnesses[n] < ancestor_fitness:
                    dct += 1
                elif fitnesses[n] == ancestor_fitness:
                    nct += 1
                elif fitnesses[n] > ancestor_fitness:
                    bct += 1
                    
            #print len(neutral_degrees_part['lethal'])        
            neutral_degrees_part['lethal'].append(lct)
            neutral_degrees_part['deleterious'].append(dct)
            neutral_degrees_part['neutral'].append(nct)
            neutral_degrees_part['beneficial'].append(bct)            
        elif fitnesses[v] > ancestor_fitness:
            beneficial_fit_ct += 1       
            beneficial_degrees.append(v.out_degree())
            
            lct = 0
            dct = 0
            nct = 0
            bct = 0
            for n in v.all_neighbours():
                if fitnesses[n] == 0:
                    lct += 1
                elif fitnesses[n] < ancestor_fitness:
                    dct += 1
                elif fitnesses[n] == ancestor_fitness:
                    nct += 1
                elif fitnesses[n] > ancestor_fitness:
                    bct += 1
                    
            beneficial_degrees_part['lethal'].append(lct)
            beneficial_degrees_part['deleterious'].append(dct)
            beneficial_degrees_part['neutral'].append(nct)
            beneficial_degrees_part['beneficial'].append(bct)
            
            
        if phenotypes[v] == 0:
            nothing_phen_ct += 1
        if phenotypes[v] & ancestor_phenotype < ancestor_phenotype:
            deleterious_phen_ct += 1
        if phenotypes[v] & ancestor_phenotype == ancestor_phenotype:
            neutral_phen_ct += 1
        if phenotypes[v] & ancestor_phenotype > ancestor_phenotype:
            beneficial_phen_ct += 1 
            
        ## TODO - count the number of Lethal,Delet,Neut, and Beneficial nodes that connect to each of the before types of node. 
            
    print "         Lethal, Deleterious, Neutral, Beneficial"
    print "Fitness",lethal_fit_ct, deleterious_fit_ct, neutral_fit_ct, beneficial_fit_ct 
    print "Phen   ",nothing_phen_ct, deleterious_phen_ct, neutral_phen_ct, beneficial_phen_ct
    print "Mean D.",np.mean(lethal_degrees), np.mean(deleterious_degrees), np.mean(neutral_degrees), np.mean(beneficial_degrees)
    print "Med D. ",np.median(lethal_degrees), np.median(deleterious_degrees), np.median(neutral_degrees), np.median(beneficial_degrees)    
    print
    print "Degree Types, mean"
    print "Lethal:", np.mean(lethal_degrees_part['lethal']),np.mean(lethal_degrees_part['deleterious']),np.mean(lethal_degrees_part['neutral']),np.mean(lethal_degrees_part['beneficial'])
    print "Delete:", np.mean(deleterious_degrees_part['lethal']),np.mean(deleterious_degrees_part['deleterious']),np.mean(deleterious_degrees_part['neutral']),np.mean(deleterious_degrees_part['beneficial'])
    print "Neutra:", np.mean(neutral_degrees_part['lethal']),np.mean(neutral_degrees_part['deleterious']),np.mean(neutral_degrees_part['neutral']),np.mean(neutral_degrees_part['beneficial'])
    print "Benefi:", np.mean(beneficial_degrees_part['lethal']),np.mean(beneficial_degrees_part['deleterious']),np.mean(beneficial_degrees_part['neutral']),np.mean(beneficial_degrees_part['beneficial'])
    print
    print "Degree Types, median"
    print "Lethal:", np.median(lethal_degrees_part['lethal']),np.median(lethal_degrees_part['deleterious']),np.median(lethal_degrees_part['neutral']),np.median(lethal_degrees_part['beneficial'])
    print "Delete:", np.median(deleterious_degrees_part['lethal']),np.median(deleterious_degrees_part['deleterious']),np.median(deleterious_degrees_part['neutral']),np.median(deleterious_degrees_part['beneficial'])
    print "Neutra:", np.median(neutral_degrees_part['lethal']),np.median(neutral_degrees_part['deleterious']),np.median(neutral_degrees_part['neutral']),np.median(neutral_degrees_part['beneficial'])
    print "Benefi:", np.median(beneficial_degrees_part['lethal']),np.median(beneficial_degrees_part['deleterious']),np.median(beneficial_degrees_part['neutral']),np.median(beneficial_degrees_part['beneficial'])

calc_stats()

