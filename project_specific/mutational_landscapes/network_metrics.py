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

networkfile = args[0]
 
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

def calc_two_step_epistasis():
    ## assumes that there is one ancestor
    ## ignores steps > 2

    g = load_graph(networkfile, "gt")
 
    fitnesses = g.vertex_properties["fitnesses"]
    steps = g.vertex_properties["steps"]
    surveyed = g.vertex_properties["surveyed"]

    ### Find the home vertex. It should be right in the beginning
    ancestor = None
    for v in g.vertices():
        if steps[v] == 0:
            ancestor = v
            break
    ancestor_fitness = fitnesses[ancestor]
    steps[ancestor] = -1    
    
    
    ## perform a nested loop here.
    epistasis = []
    net_fitness_effects = []
    
    #print ancestor.out_degree()
    #print
    
    for v in ancestor.all_neighbours(): ## all are step 1 (or fricking should be)
        if steps[v] == 0 and surveyed[v] == True:
            #print "v - ", steps[v]
            vfit = fitnesses[v]
            
            onestep_effect = 2    
            if vfit >= (ancestor_fitness * .99) and vfit <= (ancestor_fitness * 1.01):
                onestep_effect = 1 
            elif vfit < (ancestor_fitness * .99):
                onestep_effect = 0
            #print onestep_effect
            
            print v.out_degree()
                
            for w in v.all_neighbours():
                #print "  w - ", steps[w]
                
                if steps[w] == 1: ## we can evaluate
                    wfit = fitnesses[w]   
                    
                    twostep_effect = 8
                    if wfit >= (ancestor_fitness * .99) and wfit <= (ancestor_fitness * 1.01):
                        twostep_effect = 4  
                    elif wfit < (ancestor_fitness * .99):
                        twostep_effect = 0
                    
                    epistasis.append(onestep_effect + twostep_effect)
                    net_fitness_effects.append( wfit - vfit )
                    #print "  ", onestep_effect+twostep_effect
                
    print "# Epistatic effects "
    print "# 1. two-step episasis (signs)"
    print "# 2. net-fitness effects"    
    print "# "   
    print "# 1 - EPISTASES:"
    print ",".join([str(x) for x in epistasis])        
    print "# 2 - NET FITNESS EFFECTS:"
    print ",".join([str(x) for x in net_fitness_effects])   
    
def calc_neutral_density():
    g = load_graph(networkfile, "gt")
    #print "LOADED"
    #print g
 
    fitnesses = g.vertex_properties["fitnesses"]
    alleles_cluster = g.vertex_properties['alleles_cluster']
    surveyed = g.vertex_properties['surveyed']

    ### Find the home vertex. It should be right in the beginning
    ancestor = None
    for v in g.vertices():
        if alleles_cluster[v] == -1:
            ancestor = v
            break
        
    ancestor_fitness = fitnesses[ancestor]
    ancestor_log_fitness = math.log(ancestor_fitness)

    lethal = []
    deleterious = []
    neutral = []    
    beneficial = []
    
    avg_fitnesses = []
    med_fitnesses = []
    std_fitnesses = []        
    
    for v in g.vertices():        
        if (surveyed[v] == True): ## we are a mutant parent
            neighbor_total = float(v.out_degree())
            lct = 0
            dct = 0
            nct = 0
            bct = 0
            vertexrelfitnesses = []
            for n in v.all_neighbours():
                if fitnesses[n] == 0: ## dead
                    lct += 1
                elif fitnesses[n] >= (ancestor_fitness * .99) and fitnesses[n] <= (ancestor_fitness * 1.01) : ## neutral and nearly neutral
                    nct += 1
                elif fitnesses[n] < ancestor_fitness: ## deleterious
                    dct += 1
                elif fitnesses[n] > ancestor_fitness: ## beneficial
                    bct += 1
                    
                relfit = fitnesses[n] - ancestor_fitness
#                if relfit == 0:
#                    relfit = 0.000000001    
#                    print "WHAT"
                vertexrelfitnesses.append(relfit)    

            lethal.append((lct)/(neighbor_total))            
            deleterious.append((dct)/(neighbor_total))
            neutral.append((nct)/(neighbor_total))                             
            beneficial.append((bct)/(neighbor_total))
            
            avg_fitnesses.append( np.average(vertexrelfitnesses) )
            med_fitnesses.append( np.median(vertexrelfitnesses) )
            std_fitnesses.append( np.std(vertexrelfitnesses) )
            
    
    print "# Proportion of 1-step neighbors that are "
    print "# 1. proportion of dead mutants"
    print "# 2. proportion of deleterious mutants"
    print "# 3. proportion of (nearly) neutral mutants"
    print "# 4. proportion of beneficial mutants"
    print "# 5. avg fitness of neighboring mutants"
    print "# 6. median fitness of neighboring mutants"
    print "# 7. std of fitness of neighboring mutants"
    
    print "# "   
    print "# 1 - dead:"
    print ",".join([str(x) for x in lethal])        
    print "# 2 - deleterious"
    print ",".join([str(x) for x in deleterious])        
    print "# 2 - deleterious"
    print ",".join([str(x) for x in neutral])
    print "# 2 - deleterious"
    print ",".join([str(x) for x in beneficial])    
    print "# 2 - deleterious"
    print ",".join([str(x) for x in avg_fitnesses])
    print "# 2 - deleterious"
    print ",".join([str(x) for x in med_fitnesses])
    print "# 2 - deleterious"
    print ",".join([str(x) for x in std_fitnesses])
    
def calc_variability():
    g = load_graph(networkfile, "gt")
    #print "LOADED"
    #print g
 
    fitnesses = g.vertex_properties["fitnesses"]

    alleles_cluster = g.vertex_properties['alleles_cluster']
    phenotypes = g.vertex_properties["phenotypes"]
    surveyed = g.vertex_properties['surveyed']
    
    ### Find the home vertex. It should be right in the beginning
    ancestor = None
    for v in g.vertices():
        if alleles_cluster[v] == -1:
            ancestor = v
            break
        
    ancestor_fitness = fitnesses[ancestor]
    ancestor_phenotype = phenotypes[ancestor]    

    lethal_phens = []
    deleterious_phens = []
    neutral_phens = []
    beneficial_phens = []
        
    for v in g.vertices():        
        if (surveyed[v] == True): ## we are a mutant parent
            neighbor_total = float(v.out_degree())
                                    
            vertexphenotypes = {} ## phenotypes we've seen.
            phenofits = {}

            lct = 0
            dct = 0
            nct = 0
            bct = 0

            vertexfitnesses = []

            ## iterate over the neighbors and characterize them
            for n in v.all_neighbours():
                
                ## initialize if necessary
                if phenotypes[n] not in vertexphenotypes: ## new phenotype
                    vertexphenotypes[phenotypes[n]] = {"lethal":0, 
                                           "deleterious":0,
                                           "neutral":0,
                                           "beneficial":0}
                    phenofits[phenotype[n]] = []
                
                
                
                phenofits[phenotype[n]].append(fitnesses[n])                
                if fitnesses[n] == 0:
                    lct += 1
                    vertexphenotypes[phenotypes[n]]["lethal"] += 1
                elif fitnesses[n] < ancestor_fitness:
                    dct += 1
                    vertexphenotypes[phenotypes[n]]["deleterious"] += 1
                elif fitnesses[n] == ancestor_fitness:
                    nct += 1
                    vertexphenotypes[phenotypes[n]]["neutral"] += 1
                elif fitnesses[n] > ancestor_fitness:
                    bct += 1
                    vertexphenotypes[phenotypes[n]]["beneficial"] += 1
                        
            ## gather the raw proportions            
            lethal_phens.append(lctneighbor_total)
            deleterious_phens.append(dct/neighbor_total)
            neutral_phens.append(nct/neighbor_total)
            beneficial_phens.append(bct/neighbor_total)
            
            ## calculate the average fitness of the neighborhood
            
 

    print "# Proportion of 1-step neighbors that are phenotypically different, and are"
    print "# 1. Non-lethal mutants"
    print "# 2. Neutral mutants"    
    print "# "       
    print "# 1 - NONLETHAL PHENOTYPIC VARIATION"   
    print ",".join([str(x) for x in nonlethal_var])        
    print "# 2 - NEUTRAL PHENOTYPIC VARIATION:"            
    print ",".join([str(x) for x in neutral_var])

def calc_diffusion_rates():
    g = load_graph(networkfile, "gt")
 
    fitnesses = g.vertex_properties["fitnesses"]
    alleles_cluster = g.vertex_properties['alleles_cluster']
    surveyed = g.vertex_properties['surveyed']

    ### Find the home vertex. It should be right in the beginning
    ancestor = None
    for v in g.vertices():
        if alleles_cluster[v] == -1:
            ancestor = v
            break
        
    ancestor_fitness = fitnesses[ancestor]
    ancestor_log_fitness = math.log(ancestor_fitness)

    ## From Ofria/Adami 2002
    
    ### Fidelity -- probability of birthing a genetically unchanged offspring
    # F = (1 - R_c)^l
    #  R_c == per-instruction copy mutation rate (0.0075)
    #  l == genome length (121)
    # if R_c == 0.0075 and l == 121
    #  F = (1 - 0.0075)^121
    #  F = (0.9925)^121
    #  F = 0.4021539...
    
    ### Neutrality - proportion of neutrals
    # v = N_neut / l(D-1) 
    #  D == inst set size (26)
    #  N_neut == raw number of neutrals 
    # PICK and say v = 0.01 ## 1%
    
    ### Neutral Fidelity
    # F_neut = (1 - f_c)^l
    #  f_c = R_c(1 - v) -- probability of offspring both mutating AND being non-neutral
    #  f_c = 0.0075(1 - 0.01)
    #  f_c = 0.0075(0.99) ## most mutants are non-neutral * prob of BEING mutated to that mutant
    #  f_c = 0.007424999 -- portion of the probability that any given mutation is non-neutral (most of it)
    # F_neut = (1 - 0.007424999)^121 ## inversed (the prob that you WON'T get that non-neutral mutant)
    # F_neut = (0.992575001)^121 ## evaluated over each site
    # F_neut = 0.405848 ## the chance that an offspring you WON'T be anything bad by either being genetically same, or being genetically different but otherwise same 
    
    ### Genomic Diffusion Rate -- divides those two by subtracting the plain-old-same ones from the equivalent ones.
    # D_g = F_neut - F
    # D_g = 0.405848 - 0.4021539
    # D_g = 0.0036954 ## residual equivalent babies.
    
    #### I feel like there has to be a saner way to calculate this figure that doesn't add
    #### up to being a kind of IN/OUT shell game. This is terrible mathing.
    #### Un-elegant.
    
    ######### Ultimately, GDR is based on the proportion of neutral mutants scaled by the
    ######### mutation rate (per-site) ^ genome length.
    ######### So, Phenotypic DR would be based on proportion of phenotypically different non-lethals 
    
    ### Variability - proportion of non-lethal phenotypic variants
    # Var = N_pvar / l(D-1)
    # PICK and say Var = 0.01 ## 1% interesting (phen diff and non-dead)
    
    ### Variable Non-Lethality + Fidelity (a compound measure)
    # F_var = (1 - v_c)^l 
    #  v_c = R_c(1 - Var) -- prob of offspring both mutating and being phen non-different or dead
    #  v_c = 0.0075(1 - 0.01)
    #  v_c = 0.0075(0.99)
    #  v_c = 0.007424999 -- portion of the prob that you'll not be interesting (mutated and either same phen, or dead) 
    # F_var = (1 - 0.00742499)^121 -- inversed, prob that you'll be either SAME (genetically) plus the portion that is interesting
    # F_var = (0.992575001)^121
    
    #### would it work just to take the residual proportion? (0.0075 * 0.01) ? Could we ignore the
    #### Fidelity calculation step altogether?
    #### bleh = 0.0075*0.01 
    #### bleh = 0.000075 
    #### Guess not. 
    
    ### MY OWN IDEAS
    # 1. I want a measure that DOESN'T include mutation rates :P
    ## because I want to be able to think about it exhaustively rather than dicking around with 
    ## dumbassery like Fidelity that is only about excluding the mutation rate.
    ## but that may just be purely be the neutrality measure (proportion of neutral mutants)
    ## It's like a bunch of wrapping paper.
     
    # 2. I want an entropy measure of distribution of phenotypes
    
    
#    for neighbor in ancestor.all_neighbours():
 
 
 
        
    
#     for v in g.vertices():        
#         if (surveyed[v] == True): ## we are a mutant parent
#             neighbor_total = float(v.out_degree())
#             lct = 0
#             dct = 0
#             nct = 0
#             bct = 0
#             vertexrelfitnesses = []
#             for n in v.all_neighbours():
#                 if fitnesses[n] == 0: ## dead
#                     lct += 1
#                 elif fitnesses[n] >= (ancestor_fitness * .99) and fitnesses[n] <= (ancestor_fitness * 1.01) : ## neutral and nearly neutral
#                     nct += 1
#                 elif fitnesses[n] < ancestor_fitness: ## deleterious
#                     dct += 1
#                 elif fitnesses[n] > ancestor_fitness: ## beneficial
#                     bct += 1
#                     
#                 relfit = fitnesses[n] - ancestor_fitness
# #                if relfit == 0:
# #                    relfit = 0.000000001    
# #                    print "WHAT"
#                 vertexrelfitnesses.append(relfit)    
# 
#             lethal.append((lct)/(neighbor_total))            
#             deleterious.append((dct)/(neighbor_total))
#             neutral.append((nct)/(neighbor_total))                             
#             beneficial.append((bct)/(neighbor_total))
#             
#             avg_fitnesses.append( np.average(vertexrelfitnesses) )
#             med_fitnesses.append( np.median(vertexrelfitnesses) )
#             std_fitnesses.append( np.std(vertexrelfitnesses) )
#             
#     
#     print "# Proportion of 1-step neighbors that are "
#     print "# 1. proportion of dead mutants"
#     print "# 2. proportion of deleterious mutants"
#     print "# 3. proportion of (nearly) neutral mutants"
#     print "# 4. proportion of beneficial mutants"
#     print "# 5. avg fitness of neighboring mutants"
#     print "# 6. median fitness of neighboring mutants"
#     print "# 7. std of fitness of neighboring mutants"
#     
#     print "# "   
#     print "# 1 - dead:"
#     print ",".join([str(x) for x in lethal])        
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in deleterious])        
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in neutral])
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in beneficial])    
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in avg_fitnesses])
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in med_fitnesses])
#     print "# 2 - deleterious"
#     print ",".join([str(x) for x in std_fitnesses])

if options.neut_density:
    #print "NEUTRAL DENSITY (A)"
    calc_neutral_density()
elif options.variability:
    #print "VARIABILITY (B)"
    calc_variability()   
elif options.epistasis:
    #calc_two_step_epistasis()
    print "DISABLED"    
elif options.gdr or options.pdr:
    calc_diffusion_rates()    
else:
    print
    print "OTHER STATS"
    calc_stats()

