#!/usr/bin/python

# Draw the placements of where the tasks are

# Written in Python 2.7
# RCK
# 03-21-12

import os
import glob
import gzip
from optparse import OptionParser

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable


# Set up options
usage = """usage: %prog [options] task.0_column task.1_column fitness_column lineage.dat tasksites_directory

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose mode")
parser.add_option("-d", "--debug", action = "store_true", dest = "debug_messages",
                  default = False, help = "debug mode")

parser.add_option("-a", "--aggregate", dest = "aggregate", type="string",
                  help = "aggregate the task mappings output into a single file")

parser.add_option("--task_map", action = "store_true", dest = "task_map",
                  default = False, help = "output the task map")

parser.add_option("--mutation_map", action = "store_true", dest = "mutation_map",
                  default = False, help = "output the mutation map")

parser.add_option("--aligned_task_map", action = "store_true", dest = "aligned_task_map",
                  default = False, help = "output the aligned task map")

parser.add_option("--aligned_lineage_map", action = "store_true", dest = "aligned_lineage_map",
                  default = False, help = "output the complete aligned lineage map")

parser.add_option("--lineage_map", action = "store_true", dest = "lineage_map",
                  default = False, help = "output the unaligned lineage map")

parser.add_option("--show_mutations", action = "store_true", dest = "show_mutations",
                  default = False, help = "include the mutations in the ouput")

## fetch the args
(options, args) = parser.parse_args()

if not options.aggregate:
    options.trim_whitespace = True

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

    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v==val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

class KnockOutDegeneracy:
    FL_Neutral, BB_Neutral, BBFL_Neutral = range(12, 15)
    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v==val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)


class Mutations:
    Point, Insertion, Deletion, NoMutation = range(15,19)
    @classmethod
    def tostring(cls, val):
        for k,v in vars(cls).iteritems():
            if v==val:
                return k

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

def tostring(val):
    if val < 12:
        return KnockOuts.tostring(val)
    elif val < 15:
        return KnockOutDegeneracy.tostring(val)
    else:
        return Mutations.tostring(val)

def is_functional(val):
    funct = tostring(val)
    if "Lose" in funct:# or "Dead" in funct:
        return True
    else:
        return False

def is_lethal(val):
    funct = tostring(val)
    if "Dead" in funct:
        return True
    else:
        return False

def is_neutral(val):
    if val == 1 or val == 2 or val == 4 or val == 5:
        return True
    else:
        return False

def is_mutation(val):
    if val >= 15 and val < 18:
        return True
    else:
        return False

def is_degenerate(val):
    if val >= 12 and val < 15:
        return True
    else:
        return False

def is_bb_only(val):
    if val == 7 or val == 8:
        return True
    else:
        return False

def is_fl_only(val):
    if val == 3 or val == 6:
        return True
    else:
        return False

def is_bb_fl(val):
    if val == 9:
        return True
    else:
        return False

def to_degen(val):
    if is_bb_only(val):
        return KnockOutDegeneracy.BB_Neutral
    elif is_fl_only(val):
        return KnockOutDegeneracy.FL_Neutral
    elif is_bb_fl(val):
        return KnockOutDegeneracy.BBFL_Neutral
    else:
        return 0

class Phases:
    Reward, NoReward, Border = range(19, 22)

class SiteStatus:
    Active, Degenerate = range(2)

class Colors:
    Black = (0.0, 0.0, 0.0, 1.0)
    Purple = (0.55, 0.0, 0.55, 1.0)
    Blue = (0.20, 0.49, 0.95, 1.0)
    Green = (0.0, 0.7, 0.0, 1.0)
    Yellow = (0.9, 0.9, 0.0, 1.0)
    Orange = (0.93, 0.67, 0.13, 1.0)
    Red = (0.95, 0, 0.0, 1.0)
    DarkPink = (0.86, 0.62, 0.65, 1.0)
    DarkGray = (0.65, 0.65, 0.65, 1.0)
    Gray = (0.75, 0.75, 0.75, 1.0)
    LightGray = (0.85, 0.85, 0.85, 1.0)
    White = (1.0, 1.0, 1.0, 1.0)
    LightPurple = (0.8, 0.7, 0.8, 1.0) ## degenerate site
    LightBlue = (0.7, 0.7, 0.8, 1.0) ## degenerate site
    LightPink = (0.8, 0.7, 0.7, 1.0) ## degenerate site
    TransparentGray = (0.75, 0.75, 0.75, 0.5)
    Default = (0.7, 0.53, 0.5, 1.0) ## pukey brown

ColorsMapping = [
    Colors.Default, ## this is unused -- an error code
    Colors.Gray, ## KO.GainBB_GainFL -- neutral
    Colors.Gray, ## KO.GainBB_NeutFL -- neutral
    Colors.Blue, #Colors.Green, ## fluctuating site, but you also gain BB, so a little different
    Colors.Gray, ## KO.NeutBB_GainFL -- neutral
    Colors.Gray, ## KO.NeutBB_NeutFL -- neutral
    Colors.Blue, ## fluctuating only site 
    Colors.Red,  #Colors.Orange, ## backbone site, but you gain FL, so interesting 
    Colors.Red,  ## backbone only site 
    Colors.Purple, ## both site 
    Colors.Black,  ## knocking out this site kills you -- KnockOuts.Dead
    Colors.LightGray, ## empty -- KnockOuts.Empty -- WEIRD -- 11
    Colors.LightBlue, ## degenerate fluctuating site -- KODegen.FLNeut
    Colors.LightPink, ## degenerate backbone site -- KODegen.BBNeut
    Colors.LightPurple, ## degenerate both site -- KODegen.BBFLNeut
    Colors.Yellow, ## Point Mutation -- 15
    Colors.Green, ## Insertion -- 16
    Colors.Orange, ## Deletion -- 17
    Colors.DarkPink, #Colors.TransparentGray,## No Mutation -- 18
    Colors.White, ## Phases.Reward -- 19
    Colors.Red, ## Phases.NoReward
    Colors.Black] ## Phases.Border -- 21

class TaskStatus:
    Gained, Neutral, Lost = range(3)

## set up the probability matrix
Knockout_Effect_Matrix = [[KnockOuts.GainBB_GainFL,   KnockOuts.GainBB_NeutFL,   KnockOuts.GainBB_LoseFL], ## visually inverted (X coordinates go down)
                          [KnockOuts.NeutBB_GainFL,   KnockOuts.NeutBB_NeutFL,   KnockOuts.NeutBB_LoseFL],
                          [KnockOuts.LoseBB_GainFL,   KnockOuts.LoseBB_NeutFL,   KnockOuts.LoseBB_LoseFL]]

######### load in the lineage file
if lineage_file[-3:] == ".gz":
    fp = gzip.open(lineage_file)
else:
    fp = open(lineage_file)

## default columns
columns = {}
columns['update_born'] = 1
columns['id'] = 2
columns['parent_id'] = 3
columns['depth'] = 4
columns['parent_dist'] = 5
columns['ancestor_dist'] = 6
columns['length'] = 7
columns['fitness']  = 8
columns['num_cpus']  = 9
columns['task']  = 10
columns['task']  = 11
columns['total_task_count']  = 12
columns['sequence']  = 13
columns['alignment'] = 14

ids = []
alignments = {}
sequences = {}
parents = {}
born = {}
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
    born[ line[ columns['id'] - 1 ] ] = int(line[ columns['update_born'] - 1 ])

fp.close()

######## construct each genotype's task map
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
    organism_task_execution = [-1,-1]
    for line in fp:

        line = line.strip()
        if len(line) == 0 or line[0] == '#': ## skip it
            continue

        line = line.replace(' ',',') ## doing this because the split method concatenates spaces all in a row
        line = line.split(',') 

        if options.debug_messages:
            print line

        # the first line contains the base organism stuff
        if (organism_task_execution[0] == -1): ## fill in the first line
            organism_task_execution[0] = int(line[task_0_col - 1]) ## organism task1
            organism_task_execution[1] = int(line[task_1_col - 1]) ## organism task2
            continue

        ## collect the tasks that this knockout morph does
        site_task_execution = [ int(line[task_0_col - 1]), int(line[task_1_col - 1]) ]
        ## collect its fitness        
        site_fitness = float( line[fitness_col - 1] )

        if options.debug_messages:
            print site_fitness

        ## determine the knockout effect
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

            ## set the knockout effect on the probability matrix and the task status
            knockout_effect = Knockout_Effect_Matrix[backbone_status][fluct_status] 
                
            if options.debug_messages:
                print tasksite_file + \
                    " WT vs Mut: "+ str(organism_task_execution)  + " " + str(site_task_execution) + \
                    " color: " + str(knockout_effect) + \
                    " status: " + str(backbone_status) + str(fluct_status)

        genome_task_map.append( knockout_effect ) ## add the site color to the organism's site array        

    genome_task_maps.append( genome_task_map ) ## add the organism to the set of organisms

    fp.close()

######## apply the alignments to the task map (assuming there need to be any)
aligned_genome_task_maps = []

size_difference = max( [ len(genome_task_map) for genome_task_map in genome_task_maps ] ) - \
    min( [ len(genome_task_map) for genome_task_map in genome_task_maps ] )

if size_difference:
    for index in range(0, len(ids)):

        genome_id = ids[index]

        aligned_task_map = genome_task_maps[index][:] ## initialize

        for i in range(0, len(alignments[genome_id])):
            if alignments[genome_id][i] == '_':
                aligned_task_map.insert(i, KnockOuts.Empty)

        aligned_genome_task_maps.append( aligned_task_map )

    ## resize the genome_task_maps to be the same width (assuming they need it)
    index = 0
    for task_map in genome_task_maps:
        task_map.extend( [KnockOuts.Empty for i in range(0, len(aligned_genome_task_maps[index]) - len(task_map)) ] )
        index += 1

else:
    aligned_genome_task_maps = genome_task_maps[:] ## just copy it over.


######## construct the mutation information map
mutation_maps = []
## populate the first mutation map (hint, there are none)
mutation_maps.append( [ Mutations.NoMutation for i in range(0, len(alignments[ ids[0] ]) ) ] ) 
for index in range(1, len(ids)): ## start with the first child.

    genome_id = ids[index]

    mutation_map = []
    
    ## sequence alignments
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

######## now, put them together to produce the final mapping
lineage_maps = [ [0 for site in task_map] for task_map in aligned_genome_task_maps ]
lineage_maps[0] = aligned_genome_task_maps[0][:] ## the first parent is what it is.

## we'll go site by site, because this is some serious bullshit.

for site_index in range(0, len(aligned_genome_task_maps[0])):
    for map_index in range(1, len(aligned_genome_task_maps)):

        ## gather up ALL THE INFO I WILL NEED
        site_funct = aligned_genome_task_maps[map_index][site_index]
        parent_site_funct = aligned_genome_task_maps[map_index - 1][site_index]
        mutation = mutation_maps[map_index][site_index]

        parent_lineage_map_site = lineage_maps[ map_index - 1][site_index]

        site = 0 ## default, fuckup color        

        ## ok!
        execution_path = []
        execution_path.append( "~~~~~~~~~~ %s to %s via %s -- SITE %s, site %s" % (tostring(parent_site_funct), tostring(site_funct), tostring(mutation), map_index, site_index) )
        ## if we're a mutant, it is easy.
        if is_mutation( mutation ):
            execution_path.append( "MUTANT" )
            if options.show_mutations:
                site = mutation
            else:
                site = site_funct # and we're done!
        else: ## ok, now, if the slate is not, in fact, wiped clean, we need to think a little harder
            if site_funct == parent_site_funct: ## we are just the same as our parent! Okay! But what is my parent was degenerate DUNDUNDUN
                execution_path.append( "SAME AS PARENT" )
                if is_degenerate( parent_lineage_map_site ): # yep, parent is degenerate. I should be too.
                    execution_path.append( "INHERITING DEGENERATE" )
                    site = parent_lineage_map_site
                else: ## so, my parent wasn't degenerate. Just honest to goodness whatever. Happens, I guess
                    execution_path.append( "JUST MYSELF" )
                    site = site_funct 
            else: # oh, bother. Let's figure out the extent of the damage
                ## first, were we functional, and are we still functional?
                if is_lethal( site_funct ): ## doesn't matter what I was. I'm deadly now, hell yeah.
                    execution_path.append( "LETHAL" )
                    site = site_funct
                elif is_lethal( parent_site_funct ): ## doesn't matter what I am, because I used to be lethal!
                    execution_path.append( "PARENT LETHAL" )
                    site = site_funct
                elif is_functional( parent_site_funct ) and is_functional( site_funct ): ## ok. phew!
                    execution_path.append( "EVERYONE IS FUNCTIONAL!" )
                    site = site_funct
                elif is_functional( parent_site_funct) and not is_functional( site_funct ): ## my parent was functional, but I am now not.
                    execution_path.append( "NEW DEGENERATE" )
                    site = to_degen( parent_site_funct )
                elif not is_functional( parent_site_funct ) and is_functional( site_funct ): ## my parent was not functional but I am now!
                    execution_path.append( "NEWLY FUNCTIONAL" )
                    site = site_funct
                elif not is_functional( parent_site_funct ) and not is_functional( site_funct ): ## neither my parent nor myself are functional
                    ## oookay. So, if my parent was non-functional, there's a chance he was a degenerate. Let's check for that.
                    if is_degenerate( parent_lineage_map_site ): # yep, parent is degenerate. I should be too.
                        execution_path.append( "INHERITING DEGENERATE" )
                        site = parent_lineage_map_site
                    else: ## so, my parent wasn't degenerate. Just honest to goodness neutral. Happens, I guess
                        execution_path.append( "STILL NEUTRAL" )
                        site = site_funct
                else:
                    execution_path.append( "WHAT THE FUCK OTHER COMBINATION COULD I BE! ZOMG" )
                    site = 0

        ## ok, now test -- our parent is degenerate, but we aren't.
        if is_degenerate( parent_lineage_map_site ) and not is_degenerate( site ): 

            ## right, so what is going on?
            if is_functional( site ):
               execution_path.append("") 
            elif is_mutation( mutation ): ## it might not be flagged in the site if we don't always show mutations.
               execution_path.append("") 
            elif is_lethal( site ):
                execution_path.append("") 
            else:
                print
                for line in execution_path:
                   print line

                print "Possible Error! Site went from Degen (%s) to Something Else (%s). genome %s, site %s" % (tostring(parent_lineage_map_site), tostring(site), map_index, site_index)

        lineage_maps[ map_index ][ site_index ] = site

## finally, take out the alignment marks so we can see it cleanly
unaligned_lineage_maps = []
for i in range(0, len(lineage_maps)):

    alignment = alignments[ ids[i] ]
    unaligned_map = lineage_maps[i][:]

    for j in range( len(alignment)-1, -1, -1):
        if alignment[j] == '_': ## move it to the end. :/
            unaligned_map.pop(j) 
            unaligned_map.append( KnockOuts.Empty )
    unaligned_lineage_maps.append( unaligned_map )


######### NOW OUTPUT ###############

def save_values( filename, organisms ):
    fp = open( filename + "__values_only.csv", "w" )
    #print organisms
    for organism in organisms:
        line = ",".join( [ str(val) for val in organism ] )
        print>>fp, line 
    fp.close()

def generate_output( prefix, maps ):

    ## save each organism's thing individually
    if not options.aggregate:
        count = 0
        for genome_id in ids:
            tasksite_file ="tasksites.org-%s.dat" % genome_id
            individual_filename = tasksite_file + ".png"
            filename = "%s__%s" % (prefix, individual_filename)

            save_values( filename, [maps[count]] )
            count += 1

    ## save them all in one fancy plot
    else:
        bits = options.aggregate.split("/")
        directory = "/".join(bits[:-1])
        filename = bits[-1]
        if len(directory) == 0:
            directory = "."
        filename = "%s/%s__%s" % (directory, prefix, filename)

        save_values(filename, maps )

if options.task_map:
    generate_output( "task_map", genome_task_maps )

if options.mutation_map:
    generate_output( "mutation_map", mutation_maps )

if options.aligned_task_map:
    generate_output( "aligned_task_map", aligned_genome_task_maps )    

if options.aligned_lineage_map:
    generate_output( "aligned_lineage_map", lineage_maps )    
 
if options.lineage_map:
    generate_output( "lineage_map", unaligned_lineage_maps )    
