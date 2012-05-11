#!/usr/bin/python

# generate metrics about the mutations

# Written in Python 2.7
# RCK
# 03-31-12

from optparse import OptionParser
#import numpy as np
#import matplotlib.pyplot as plt
#import matplotlib.cm as cm
#import os
import glob
import string
import gzip


# Set up options
usage = """usage: %prog [options] task.0_column task.1_column fitness_column lineage.dat tasksites_directory

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose mode")
parser.add_option("-d", "--debug", action = "store_true", dest = "debug_messages",
                  default = False, help = "debug mode")

## fetch the args
(options, args) = parser.parse_args()


## parameter error
if len(args) < 5:
    parser.error("incorrect number of arguments")

task_0_col = int(args[0])
task_1_col = int(args[1])
fitness_col = int(args[2])

lineage_file = args[3]
tasksites_directory = args[4]

## the stack of genotypes
genotypes = []

## the stack of organisms to display
organisms = []

## different meanings
class KnockOuts:
    GainBB_GainFL, GainBB_NeutFL, GainBB_LoseFL, NeutBB_GainFL, NeutBB_NeutFL, NeutBB_LoseFL, LoseBB_GainFL, LoseBB_NeutFL, LoseBB_LoseFL, Dead, Empty = range(1,12)

class KnockOutDegeneracy:
    FL_Neutral, BB_Neutral, BBFL_Neutral = range(12, 15)

class Mutations:
    Point, Insertion, Deletion, NoMutation = range(15,19)

class SiteStatus:
    Active, Degenerate = range(2)

class TaskStatus:
    Gained, Neutral, Lost = range(3)

## set up the probability matrix
Knockout_Effect_Matrix = [[KnockOuts.GainBB_GainFL,   KnockOuts.GainBB_NeutFL,   KnockOuts.GainBB_LoseFL], ## visually inverted (X coordinates go down)
                          [KnockOuts.NeutBB_GainFL,   KnockOuts.NeutBB_NeutFL,   KnockOuts.NeutBB_LoseFL],
                          [KnockOuts.LoseBB_GainFL,   KnockOuts.LoseBB_NeutFL,   KnockOuts.LoseBB_LoseFL]]

## load in the lineage file
if lineage_file[-3:] == ".gz":
    fp = gzip.open(lineage_file)
else:
    fp = open(lineage_file)

columns = {}

ids = []
alignments = {}
sequences = {}
parents = {}
does_xor = {}
does_equ = {}
fitness = {}
for line in fp:
    line = line.strip()
    if len(line) == 0 or line[0] == '#': ## skip it if it's not format
        if "#format" in line:
            formats = line.split()
            for i in range(1, len(formats)):
                columns[formats[i]] = i
        continue

    line = line.replace(' ',',') ## doing this because the split method concatenates spaces all in a row
    line = line.split(',') 

    ids.append( line[ columns['id'] - 1 ] )
    alignments[ line[ columns['id'] - 1 ] ] = line[ columns['alignment'] - 1 ]
    sequences[ line[ columns['id'] - 1 ] ] = line[ columns['sequence'] - 1 ]
    parents[ line[ columns['id'] - 1 ] ] = line[ columns['parent_id'] - 1 ]
    does_xor[ line[ columns['id'] - 1 ] ] = int(line[ 10 - 1 ]) ## both are called "task", so this isn't very helpful
    does_equ[ line[ columns['id'] - 1 ] ] = int(line[ 11 - 1 ]) ## ditto
    fitness[ line[ columns['id'] - 1 ] ] = float(line[ columns['fitness'] - 1 ])



fp.close()

## construct each genotype's task map
genome_task_maps = []
for genome_id in ids:

    tasksite_file_glob = "%s/tasksites.org-%s.dat*" % (tasksites_directory, genome_id)
    matching_files = glob.glob( tasksite_file_glob )

    tasksite_file = matching_files[0]

    if (options.verbose):
        print tasksite_file

    if tasksite_file[-3:] == ".gz":
        fp = gzip.open(tasksite_file)
    else:
        fp = open(tasksite_file)


    ## first, collect the task information

    genome_task_map = [] ## to hold the per-site data of the genome
    organism_task_execution = -1
    for line in fp:

        line = line.strip()
        if len(line) == 0 or line[0] == '#': ## skip it
            continue

        line = line.replace(' ',',') ## doing this because the split method concatenates spaces all in a row
        line = line.split(',') 

        if options.debug_messages:
            print line

        # the first line contains the base organism stuff
        if (organism_task_execution == -1): ## fill in the first line
            organism_task_execution = line[task_0_col - 1] + line[task_1_col - 1] ## the last two tasks
            continue

        site_task_execution = line[task_0_col - 1] + line[task_1_col - 1] ## the last two tasks
        site_fitness = float( line[fitness_col - 1] )

        if options.debug_messages:
            print site_fitness

        knockout_effect = KnockOuts.Empty
        if (site_fitness == 0): ## killed it
            knockout_effect = KnockOuts.Dead
        else: ## check the status           

            # deal with the backbone first
            if (int(site_task_execution[0]) < int(organism_task_execution[0])): ## lost the backbone
                backbone_status = TaskStatus.Lost 
            elif (int(site_task_execution[0]) == int(organism_task_execution[0])): ## neutral effect
                backbone_status = TaskStatus.Neutral
            else:
                backbone_status = TaskStatus.Gained

            # deal with the fluctuating task
            if (int(site_task_execution[1]) < int(organism_task_execution[1])): ## lost the backbone
                fluct_status = TaskStatus.Lost
            elif (int(site_task_execution[1]) == int(organism_task_execution[1])): ## neutral effect
                fluct_status = TaskStatus.Neutral
            else:
                fluct_status = TaskStatus.Gained

            knockout_effect = Knockout_Effect_Matrix[backbone_status][fluct_status] ## set the knockout effect on the probability matrix and the task status
    
            if (options.debug_messages):
                print tasksite_file + " WT vs Mut: "+ organism_task_execution  + " " + site_task_execution + " color: " + str(knockout_effect) + " status: " + str(backbone_status) + str(fluct_status)

        genome_task_map.append( knockout_effect ) ## add the site color to the organism site array        

    genome_task_maps.append( genome_task_map )

    fp.close()

## apply the alignments to the task map
aligned_genome_task_maps = []
for index in range(0, len(ids)):

    genome_id = ids[index]

    aligned_task_map = genome_task_maps[index][:] ## initialize

    for i in range(0, len(alignments[genome_id])):
        if alignments[genome_id][i] == '_':
            aligned_task_map.insert(i, KnockOuts.Empty)

    aligned_genome_task_maps.append( aligned_task_map )

## construct the mutation information map
mutation_maps = []
mutation_maps.append( [ Mutations.NoMutation for i in range(0, len(alignments[ ids[0] ]) ) ] ) ## populate the first mutation map (hint, there are none)
for index in range(1, len(ids)):

    genome_id = ids[index]

    mutation_map = []
    
    alignment = alignments[ genome_id ]
    parent_alignment = alignments[ parents[ genome_id ] ]

    for i in range(0, len(alignment)):
        if alignment[i] != parent_alignment[i]: ## no match
            if alignment[i] == "_": ## deletion!
                mutation_map.append( Mutations.Deletion )
            elif parent_alignment[i] == "_": ## insertion!
                mutation_map.append( Mutations.Insertion )
            else:
                mutation_map.append( Mutations.Point )
        else:
            mutation_map.append( Mutations.NoMutation )

    mutation_maps.append( mutation_map )

## now, put them together to produce the final mapping
lineage_maps = []
lineage_maps.append( aligned_genome_task_maps[0] ) ## the first parent is what it is.
for index in range(1, len(ids)):
    
    lineage_map = []

    mutation_map = mutation_maps[index]
    aligned_genome_task_map = aligned_genome_task_maps[index]
    aligned_parent_genome_task_map = aligned_genome_task_maps[ index - 1 ] ## pluck out the parent
    parent_lineage_map = lineage_maps[-1]

    ## apply degeneracy
    for i in range(0, len( mutation_map )):
        lineage_map.append( aligned_genome_task_map[i] ) ## default to what the task map says
        if aligned_genome_task_map[i] != aligned_parent_genome_task_map[i]: ## something changed from one to the next
            if mutation_map[i] == Mutations.NoMutation: ## if there wasn't a mutation at this spot, then we may have degeneracy going on
                if aligned_genome_task_map[i] == KnockOuts.NeutBB_NeutFL or \
                        aligned_genome_task_map[i] == KnockOuts.GainBB_NeutFL or \
                        aligned_genome_task_map[i] == KnockOuts.NeutBB_GainFL or \
                        aligned_genome_task_map[i] == KnockOuts.GainBB_GainFL: ## this site is neutral (or uninteresting) now
                    if aligned_parent_genome_task_map[i] == KnockOuts.GainBB_LoseFL or aligned_parent_genome_task_map[i] == KnockOuts.NeutBB_LoseFL:
                        lineage_map[i] = KnockOutDegeneracy.FL_Neutral ## switch!
                    elif aligned_parent_genome_task_map[i] == KnockOuts.LoseBB_GainFL or aligned_parent_genome_task_map[i] == KnockOuts.LoseBB_NeutFL:
                        lineage_map[i] = KnockOutDegeneracy.BB_Neutral ## switch!
                    elif aligned_parent_genome_task_map[i] == KnockOuts.LoseBB_LoseFL:
                        lineage_map[i] = KnockOutDegeneracy.BBFL_Neutral ## switch!
        else: ## no change to the function of this position, but...
            if parent_lineage_map[i] == KnockOutDegeneracy.FL_Neutral or \
                    parent_lineage_map[i] == KnockOutDegeneracy.BB_Neutral or \
                    parent_lineage_map[i] == KnockOutDegeneracy.BBFL_Neutral: ## our parent had a degenerate in this spot, so use it.
                lineage_map[i] = parent_lineage_map[i]

    lineage_maps.append( lineage_map ) ## put it in

########################## FINALLY #############################
## Troll the lineage map to gather the various metrics

class SiteFunction:
    NC, Cf, Cb, Cbf, Df, Db, Dbf = range(7)

    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v==val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)
    

class LineageAncestor:
    def __init__(self):
        ## mutation counts
        self.mutations_coding_region = 0
        self.mutations_noncoding_region = 0
        self.mutations_degenerate_region = 0

        ## not sure how accurate this is, because of when fitness is calculated
        ## and against what background :/
        self.net_fitness_effect = 0 # actual difference in fitness against parent

        ## genotype function changes (9 possibilities)
        self.function_effect_backbone = 0 # -1 removes, 0 no change, 1 restores
        self.function_effect_fluctuating = 0 # ditto

        ## site net functional change
        self.site_function_vector = [ [ 0 for j in range(7) ] for i in range(7) ]

        self.seq = ""
        self.parent_seq = ""

        self.comment = ""


    def __str__(self):
        output = "Seq:        %s\n" % self.seq
        output += "Parent Seq: %s\n" % self.parent_seq

        output += "mutations_coding_region: %s\n" % self.mutations_coding_region
        output += "mutations_noncoding_region: %s\n" % self.mutations_noncoding_region
        output += "mutations_degenerate_region: %s\n" % self.mutations_degenerate_region
        output += "net_fitness_effect: %s\n" % self.net_fitness_effect
        output += "function_effect_backbone: %s\n" % self.function_effect_backbone
        output += "function_effect_fluctuating: %s\n" % self.function_effect_fluctuating

        output += "site_function_vector:\n"
        ## prep the header
        vector_output = "    "
        for funct in range(7):
            vector_output += "%s" % string.ljust(SiteFunction.tostring(funct), 4)
        vector_output += "\n"

        ## output the thing
        for (funct, array) in zip(range(7), self.site_function_vector):

            arr = ""
            for val in array:
                arr += string.ljust( str(val), 4 )

            vector_output += "%s%s\n" % ( string.ljust(SiteFunction.tostring(funct), 4), arr)

        output += vector_output

        output += "Comment: %s" % self.comment

        return output

    def __header__(self):
        names = []

        ## scalars
        names.append( "mutations_coding_region" )
        names.append( "mutations_noncoding_region" )
        names.append( "mutations_degenerate_region" )
        names.append( "net_fitness_effect" )
        names.append( "function_effect_backbone" )
        names.append( "function_effect_fluctuating" )

        ## vectors
        for fr in range(7):
            for to in range(7):
                names.append( "%s_%s" % (SiteFunction.tostring(fr), SiteFunction.tostring(to)) )

        return ",".join(names)


    def __repr__(self):

        values = []

        ## scalars
        values.append( str( self.mutations_coding_region ) )
        values.append( str( self.mutations_noncoding_region ) )
        values.append( str( self.mutations_degenerate_region ) )
        values.append( str( self.net_fitness_effect ) )
        values.append( str( self.function_effect_backbone ) )
        values.append( str( self.function_effect_fluctuating ) )

        ## vectors
        for fr in range(7):
            for to in range(7):
                values.append( str(self.site_function_vector[fr][to]) )

        return ",".join( values )

#       return "%s(%r)" % (self.__class__, self.__dict__)
#       return ",".join( [ str(val) for val in vars(self).values() ] )

        #return output

#### Characterize the function of the knockouts
TranslateKnockOutToFunction = [ -1 for i in range(0, 19) ] ## 
## Non-coding artifact sites - might be useful at some point for mapping the fitness landscape
TranslateKnockOutToFunction[ KnockOuts.Empty ] = SiteFunction.NC ## came from an insertion or something (... may cause nc inflation. have to think about it)
TranslateKnockOutToFunction[ KnockOuts.Dead ] = SiteFunction.NC ## still non-coding :P
TranslateKnockOutToFunction[ KnockOuts.GainBB_GainFL ] = SiteFunction.NC 
TranslateKnockOutToFunction[ KnockOuts.GainBB_NeutFL ] = SiteFunction.NC
TranslateKnockOutToFunction[ KnockOuts.NeutBB_NeutFL ] = SiteFunction.NC
TranslateKnockOutToFunction[ KnockOuts.NeutBB_GainFL ] = SiteFunction.NC
## Coding Sites
TranslateKnockOutToFunction[ KnockOuts.GainBB_LoseFL ] = SiteFunction.Cf
TranslateKnockOutToFunction[ KnockOuts.NeutBB_LoseFL ] = SiteFunction.Cf
TranslateKnockOutToFunction[ KnockOuts.LoseBB_GainFL ] = SiteFunction.Cb
TranslateKnockOutToFunction[ KnockOuts.LoseBB_NeutFL ] = SiteFunction.Cb
TranslateKnockOutToFunction[ KnockOuts.LoseBB_LoseFL ] = SiteFunction.Cbf
## Degenerate Sites
TranslateKnockOutToFunction[ KnockOutDegeneracy.FL_Neutral ] = SiteFunction.Df
TranslateKnockOutToFunction[ KnockOutDegeneracy.BB_Neutral ] = SiteFunction.Db
TranslateKnockOutToFunction[ KnockOutDegeneracy.BBFL_Neutral ] = SiteFunction.Dbf

lineage_functions = [ LineageAncestor() ] ## the first is always blank

## for each ancestor in the lineage
for i in range(1, len(lineage_maps)): ## start with the second one

    lineage_ancestor = LineageAncestor()

    parent_lineage_map = lineage_maps[i - 1] ## fetch the parent for comparison
    lineage_map = lineage_maps[i]

    mutation_map = mutation_maps[i]

    ancestor_fitness = fitness[ ids[i] ]
    parent_fitness = fitness[ ids[i - 1] ]

    ancestor_does_equ = does_equ[ ids[i] ]
    parent_does_equ = does_equ[ ids[i - 1] ]

    ancestor_does_xor = does_xor[ ids[i] ]
    parent_does_xor = does_xor[ ids[i - 1] ]

    ## assign the ancestor-wide values
    lineage_ancestor.seq = alignments[ ids[i] ] 
    lineage_ancestor.parent_seq = alignments[ ids[i - 1] ]

    lineage_ancestor.function_effect_backbone = ancestor_does_xor - parent_does_xor
    lineage_ancestor.function_effect_fluctuating = ancestor_does_equ - parent_does_equ
    lineage_ancestor.net_fitness_effect = ancestor_fitness - parent_fitness

    ## for each site in the ancestor
    for j in range(0, len(lineage_map)):
        site_ko = lineage_map[j]
        parent_site_ko = parent_lineage_map[j]
        mut = mutation_map[j]

        ## document the target of each mutation
        if mut == Mutations.Insertion: ## we have a new instruction! how exciting!
            lineage_ancestor.comment += "%s INSERTION: NON CODING REGION" % i ## it didn't exist before, so it couldn't have been coding, could it?
            lineage_ancestor.mutations_noncoding_region += 1 ## increment non-coding region mutation
        elif mut == Mutations.Deletion or mut == Mutations.Point: ## we lost or changed an instruction, which WAS in some region
            if  parent_site_ko == KnockOuts.LoseBB_GainFL or \
                parent_site_ko == KnockOuts.LoseBB_NeutFL or \
                parent_site_ko == KnockOuts.GainBB_LoseFL or \
                parent_site_ko == KnockOuts.NeutBB_LoseFL: ## CODING REGION!!
                lineage_ancestor.mutations_coding_region += 1 ## increment coding region mutation!
                lineage_ancestor.comment += "%s CODING REGION" % i
            elif parent_site_ko == KnockOutDegeneracy.BB_Neutral or \
                 parent_site_ko == KnockOutDegeneracy.FL_Neutral or \
                 parent_site_ko == KnockOutDegeneracy.BBFL_Neutral: ## degenerate region
                lineage_ancestor.mutations_degenerate_region += 1 ## increment degenerate region mutation
                lineage_ancestor.comment += "%s DEGEN REGION" % i
            else: ## had to be a non-coding region
                lineage_ancestor.mutations_noncoding_region += 1 ## increment non-coding region mutation
                lineage_ancestor.comment += "%s NON CODING REGION" % i

        ## document the effect of all mutations on this ancestor (via documentable changes in function)
        if TranslateKnockOutToFunction[parent_site_ko] != TranslateKnockOutToFunction[site_ko]:
        #if site_ko != parent_site_ko: ## look for changes in function, regardless of mutations
            ## something changed, for whatever reason. catalogue the possibilities
            lineage_ancestor.site_function_vector[ TranslateKnockOutToFunction[parent_site_ko] ][ TranslateKnockOutToFunction[site_ko] ] += 1

    lineage_functions.append( lineage_ancestor )
    
print LineageAncestor().__header__()
for lf in lineage_functions:
    if options.debug_messages:
        print
        print lf
        print lf.__header__()
    print lf.__repr__()

