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
                  
parser.add_option("--neutraldensity", action="store_true", dest="neut_density",
                  default=False, help="output neutral density")                  

parser.add_option("--variability", action="store_true", dest="variability",
                  default=False, help="output variability")                  

parser.add_option("--gdr", action="store_true", dest="gdr",
                  default=False, help="output genomic diffusion rate")                  

parser.add_option("--pdr", action="store_true", dest="pdr",
                  default=False, help="output phenotypic diffusion rate")                  

parser.add_option("--epistasis", action="store_true", dest="epistasis",
                  default=False, help="output epistasis for two-step")

parser.add_option("-s", "--steps", dest = "steps", type="int", default = 1,
                  help = "Distance to explore from live genomes")

## fetch the args
(options, args) = parser.parse_args()
if len(args) < 1:
    parser.error("Not enough arguments.\n"+usage)

networkfiles = args[0:]
graphs = []
###### LOAD THE NETWORK FILE

for networkfile in networkfiles:

    graphs.append({})

    g = load_graph(networkfile, "gt")
    print "LOADED"
    print g
 
    graphs[-1]['graph'] = g
   
    #num_cpus = g.vertex_properties["num_cpus"]
    graphs[-1]['fitnesses'] = g.vertex_properties["fitnesses"]
    graphs[-1]['steps'] = g.vertex_properties["steps"]
    graphs[-1]['alleles_cluster'] = g.vertex_properties['alleles_cluster']
    graphs[-1]['phenotypes'] = g.vertex_properties["phenotypes"]
    graphs[-1]['surveyed'] = g.vertex_properties["surveyed"]
          
    graphs[-1]['deg'] = g.degree_property_map("in")
    
    ### Find the home vertex. It should be right in the beginning
    graphs[-1]['ancestor'] = None
    for v in g.vertices():
        if graphs[-1]['alleles_cluster'][v] == -1:
            graphs[-1]['ancestor'] = v
            break
        
    graphs[-1]['ancestor_fitness'] = graphs[-1]['fitnesses'][graphs[-1]['ancestor']]
    graphs[-1]['ancestor_phenotype'] = graphs[-1]['phenotypes'][graphs[-1]['ancestor']]    
    graphs[-1]['ancestor_log_fitness'] = math.log(graphs[-1]['ancestor_fitness'])
 


def calc_diffusion_rates():
    
    ## defaults
    mu = 0.0075 # per-site copy mutation rate -- R_c in the paper
    l = 121 # genome length
    D = 26 # inst-set size        
    ### Fidelity -- probability of birthing a genetically unchanged offspring
    F = (1 - mu)**l

    for ginfo in graphs:

        neutral = []    
        beneficial = []
        neutben = []
        
        neut_phen = []
        ben_phen = []
        neutben_phen = []
        
        neut_samephen = []
        ben_samephen = []
        neutben_samephen = []
            
        for v in ginfo['graph'].vertices():        
            if (ginfo['surveyed'][v] == True): ## we are a mutant parent
                neighbor_total = float(v.out_degree())
                nct = 0
                bct = 0
                nbct = 0
                
                nct_p = 0
                bct_p = 0
                nbct_p = 0
    
                nct_samep = 0
                bct_samep = 0
                nbct_samep = 0
    
                for n in v.all_neighbours():
                    if (ginfo['fitnesses'][n] >= (ginfo['ancestor_fitness'] * .99) and 
                        ginfo['fitnesses'][n] <= (ginfo['ancestor_fitness'] * 1.01)): ## neutral and nearly neutral
                        nct += 1
                        nbct += 1
                        if ginfo['phenotypes'][n] != ginfo['ancestor_phenotype']:
                            nct_p += 1
                            nbct_p += 1
                        else:
                            nct_samep += 1
                            nbct_samep += 1
                    elif ginfo['fitnesses'][n] > ginfo['ancestor_fitness']: ## beneficial
                        bct += 1
                        nbct += 1
                        if ginfo['phenotypes'][n] != ginfo['ancestor_phenotype']:
                            bct_p += 1
                            nbct_p += 1
                        else:
                            bct_samep += 1
                            nbct_samep += 1     
                neutral.append((nct)/(neighbor_total))                             
                beneficial.append((bct)/(neighbor_total))
                neutben.append((nbct)/(neighbor_total))
                
                neut_phen.append(nct_p/neighbor_total)
                ben_phen.append(bct_p/neighbor_total)
                neutben_phen.append(nbct_p/neighbor_total)
                
                neut_samephen.append((nct_samep)/neighbor_total)
                ben_samephen.append((bct_samep)/neighbor_total)
                neutben_samephen.append((nbct_samep)/neighbor_total)
    
        ####### PHENOTYPIC NEUTRALITY ACROSS DIFFERENT ENVIRONMENTS ######## -- setting the below aside for now.
        # your phenotype is neutral or beneficial in one or more accessible environment -- how many environments are there? how many are you neutral in?
        # WHAT IS The probability of being in that environment in which you are neutral?         
        ## Initially, assume all environments are equaly likely (1/e)
        ## Must evaluate the phenotype in each possible environment.
        #### EXPECTED VALUE
        ## proportion of mutants, neutral in a given environment (n/m) * 1/e
        #### this is the probability of being the right kind of mutant in a given kind of environment.
        ## Overall, sum the probabilities across all the environments -- this gives you the probability of being good in any of the possible environments.
        ####### EVOLVABLE NEUTRALITY??? ####################################
        ## Objections: 
        ### 1. not all environments are equally probable
        
        ## From Ofria/Adami 2002
        ### Neutrality - proportion of neutrals
        # v = N_neut / l(D-1) 
        #  D == inst set size (26)
        #  N_neut == raw number of neutrals 
        # PICK and say v = 0.01 ## 1%
        ## EMPIRICALLY DERIVED
        ginfo['nu_g'] = np.average(neutben)
        ginfo['nu_p'] = np.average(neutben_samephen)
        
        ### Neutral Fidelity
        # F_neut = (1 - f_c)^l
        #  f_c = R_c(1 - v) -- probability of offspring both mutating AND being non-neutral
        #  f_c = 0.0075(1 - 0.01)
        #  f_c = 0.0075(0.99) ## most mutants are non-neutral * prob of BEING mutated to that mutant
        #  f_c = 0.007424999 -- portion of the probability that any given mutation is non-neutral (most of it)
        # F_neut = (1 - 0.007424999)^121 ## inversed (the prob that you WON'T get that non-neutral mutant)
        # F_neut = (0.992575001)^121 ## evaluated over each site
        # F_neut = 0.405848 ## the chance that an offspring you WON'T be anything bad by either being genetically same, or being genetically different but otherwise same 
        ginfo['f_c_prob_nonneut'] = mu * (1 - ginfo['nu_g'])
        ginfo['F_neut'] = (1 - ginfo['f_c_prob_nonneut'])**l
        ginfo['f_cp_prob_nonneut_diffphen'] = mu * (1 - ginfo['nu_p'])
        ginfo['F_pheno'] = (1 - ginfo['f_cp_prob_nonneut_diffphen'])**l
        
        ### Genomic Diffusion Rate -- divides those two by subtracting the plain-old-same ones from the equivalent ones.
        # D_g = F_neut - F
        # D_g = 0.405848 - 0.4021539
        # D_g = 0.0036954 ## residual equivalent babies.
        ginfo['D_g'] = ginfo['F_neut'] - F
        ginfo['D_p'] = ginfo['F_neut'] - ginfo['F_pheno']
        
        #print "# mu, l, D, F, nu_g, nu_p, f_c_prob_nonneut, F_neut, f_cp_prob_nonneut_diffphen, F_pheno, D_g, D_p"
        #print mu, l, D, F, nu_g, nu_p, f_c_prob_nonneut, F_neut, f_cp_prob_nonneut_diffphen, F_pheno, D_g, D_p
    #   

    print "Mutation Rate: ", mu
    print "Genome Length: ", l
    print "Inst Set Size: ", D
    print "Fidelity:      ", F

    nu_g = np.mean([ginfo['nu_g'] for ginfo in graphs])    
    print "nu_g:          ", nu_g, " -- Proportion of fitness neutrals"
 
    nu_p = np.mean([ginfo['nu_p'] for ginfo in graphs])
    print "nu_p:          ", nu_p, " -- Proportion of fitness neutrals that share a phenotype"

    print "nu_g - nu_p:   ", nu_g - nu_p, " -- Proportion of fitness neutrals that are a different phenotype"
    
    print "f_c:           ", np.mean([ginfo['f_c_prob_nonneut'] for ginfo in graphs]), " -- Probability that a mutation will result in a non-neutral fitness offspring"
    print "f_cp:          ", np.mean([ginfo['f_cp_prob_nonneut_diffphen'] for ginfo in graphs]), " -- Probability that a mutation will result in an offspring that is NOT a fitness neutral with the same phenotype"
    print "F_neut:        ", np.mean([ginfo['F_neut'] for ginfo in graphs]), " -- Probability that an offspring will be neutral (including identical offspring)"
    print "F_pheno:       ", np.mean([ginfo['F_pheno'] for ginfo in graphs]), " -- Probability that an offspring will be neutral and share your phenotype (including identical offspring)"
    print "D_g:           ", np.mean([ginfo['D_g'] for ginfo in graphs]), " -- Probability that an offspring will be non-identical, yet neutral"
    print "D_p:           ", np.mean([ginfo['D_p'] for ginfo in graphs]), " -- Probability that an offspring will be non-identical, neutral, and not share your phenotype"
          


calc_diffusion_rates()    

