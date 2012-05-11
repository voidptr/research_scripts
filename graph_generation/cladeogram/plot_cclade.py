########
## Originally created by Matt Rupp... sometime in the past
##
## Updated by Rosangela Canino-Koning 2/23/12
########

## create a cladeogram

from pylab import *
import pdb
import matplotlib as mpl
import numpy as np
import sys
import gzip
from AvidaData import *
from DataTable import *
from cladeogram import *

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] outfile.png cclade_counts.dat detail-30000.spop.gz population_size

Permitted types for outfile are png, pdf, ps, eps, and svg
"""

parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
                  
parser.add_option("-p", "--forpaper", action = "store_true", dest = "forpaper",
                  default = False, help = "larger output")

parser.add_option("-a", "--byancestor", action = "store_true", dest = "byancestor",
                  default = False, help = "relative fitness by ancestor")

## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 4:
    parser.error("incorrect number of arguments")

outfile = args[0]
population_history_path = args[2]
clade_count_path = args[1]
#stats_path = args[2]

population_size = int(args[3])

if options.forpaper:
   fig_width_pt = 469.77502 # Get this from LaTeX using \showthe\columnwidth
   sbX = 80000
   sbY = 0.10
   lwt = 3  #Line with for EQU over time (fimpma)
   lwa = 3  #Line width for EQU at end  (fimpma)
else:
   fig_width_pt = 290.742
   sbX = 60000 # Position of symbol box X
   sbY = 0.10  #Position of symbol box Y
   lwt = 2  #Line with for EQU over time (fimpma)
   lwa = 2  #Line width for EQU at end  (fimpma)

inches_per_pt = 1.0/72.27               # Convert pt to inches
golden_mean = (sqrt(5)-1.0)/2.0         # Aesthetic ratio
fig_width = fig_width_pt*inches_per_pt  # width in inches
fig_height =fig_width*golden_mean       # height in inches
fig_size = [fig_width,fig_height]
params = {'backend': 'ps',
             'figure.facecolor':'white',
             'axes.labelsize': 7,
             'axes.titlesize':10,
             'text.fontsize': 10,
             'legend.fontsize': 6,
             'xtick.labelsize': 7,
             'ytick.labelsize': 7,
             #'text.usetex': True,
             'font.family':'sans-serif',
             #'text.dvipnghack':True,
             'figure.figsize': fig_size,
             'xtick.major.pad':6}
rcParams.update(params)
   
if not options.forpaper:
   axes([0.15, 0.55, 0.80, 0.40])   

if options.byancestor:
    print "Relative Fitness by Ancestor."
else:
    print "Relative Fitness by Parent."

stats_format = ['update%d', 'energy%f', 'avgmut%f',' avgmut_dom%f', 'avgfid%f', 'avgfid_dom%f',\
             'deltag%f', 'gen_h%f', 'sp_h%f',\
             'depth_clsc%d', 'resamp%d', 'resamp_fail%d']

## init the cladeograms
MyCladeogram = cladeogram(clade_count_path, population_size)
Clades = MyCladeogram.GetClades()

## extract the genotype history
if population_history_path[-3:] == ".gz":
    fd = gzip.open(population_history_path)
else:
    fd = open(population_history_path)

if options.verbose:
    print "Processing: '" + population_history_path + "'"

file_format = {}
org_id_index = -1
parent_id_index = -1
fitness_index = -1
genotypes = {}
for line in fd:
    line = line.strip() ## strip off the end of line crap

    if len(line) == 0 or line[0] == '#': ## if the line is blank or a comment
        if "#format" in line:
            columns = line.split()[1:] ## grab the format lines
            for index in range(0, len(columns)):
                file_format[ columns[index] ] = index

            #print file_format
            parent_field_name = "parents"
            if ( parent_field_name not in file_format ):
                parent_field_name = "parent_id"

            org_id_index = file_format[ 'id' ]
            parent_id_index = file_format[ parent_field_name ]
            fitness_index = file_format[ 'fitness' ]

        continue

    whole_line = line

    line = line.split() ## break the line up on spaces

    org_id = int(line[ org_id_index ])
    parent_id_str = line[ parent_id_index ]
    parent_id = -1
    if parent_id_str != '(none)':
        parent_id = int(parent_id_str)
    fitness = float(line[ fitness_index ] )

    genotypes[ org_id ] = ( parent_id, fitness )
fd.close()

## assign clade membership (for convenience)
genotype_clades = {}
for clade in Clades.keys():
    genotype_clades[ clade ] = clade

def find_clade( genotype_id ):
    if genotype_id == -1:
        return 0

    if genotype_id in genotype_clades: ## I'm a clade founder!
        return genotype_clades[ genotype_id ] 
    else: 
        if genotype_id not in genotypes: ## unknown! :(
            return 0
        parent_id = genotypes[ genotype_id ][ 0 ]
        clade = find_clade( parent_id )
        genotype_clades[ genotype_id ] = clade
        return clade

sorted_genotypes = genotypes.keys()
sorted_genotypes.sort()
for org_id in sorted_genotypes:
    genotype_clades[ org_id ] = find_clade( org_id )

## make lists of the genotypes in a clade
clade_genotypes = {}
for (genotype, clade) in genotype_clades.items():
    if clade not in clade_genotypes:
        clade_genotypes[ clade ] = []

    clade_genotypes[ clade ].append( genotype )

def get_ancestral_line_fitnesses( clade_id ):
    genotype = clade_id
    fitnesses = []
    while genotype in genotypes:        
        fitnesses.append( genotypes[ genotype ][ 1 ] )
        genotype = genotypes[ genotype ][ 0 ]

    return fitnesses

polys   = []
fitvals = []
ordering = np.sort(Clades.keys())
for clade_id in ordering:
    clade = Clades[clade_id]
    polys.append( np.c_[clade.polyX, clade.polyY] )
  
    if options.byancestor: ## calculate the relative fitness of this clade against that of the max fitness of its ancestral line
        ancestral_line_fitnesses = get_ancestral_line_fitnesses( clade_id )
        if len(ancestral_line_fitnesses) == 1:
            fitvals.append( 1.0 )
        else:
            max_fitness = np.max( ancestral_line_fitnesses[:-1] )
            fitvals.append( genotypes[ clade_id ][ 1 ] / max_fitness if max_fitness > 0 else 1.0 )
    else:
        if genotypes[ clade_id ][ 0 ] not in genotypes:
            fitvals.append( 1.0 )
        else:                
            parental_fitness = genotypes[ genotypes[ clade_id ][ 0 ] ][ 1 ]
            fitvals.append( genotypes[ clade_id ][ 1 ] / parental_fitness if parental_fitness > 0 else 1.0 )

#for val in fitvals:
#    print val

#print fitvals
   
pc = mpl.collections.PolyCollection(polys)
norm = mpl.colors.Normalize(vmin=0.0, vmax=2.0, clip=True)
ax = axes()

ax.add_collection(pc)

#print
#normvals = norm(fitvals)
#for val in normvals:
#    print val



#print norm(fitvals)

pc.set_array(norm(fitvals))

pc.set_cmap(cm.jet)

pc.set_linewidth(0.05)

ax.autoscale_view()

xlabel('Update')

nultick = mpl.ticker.NullFormatter()

ax.yaxis.set_major_formatter(nultick)

ylabel('Abundance')

#title('Example Cladeogram')

ylim(0,population_size)

cax,kw = mpl.colorbar.make_axes(ax, orientation='horizontal')

lbl = 'Parent Relative Fitness' 
if options.byancestor: 
    lbl = 'Ancestor Relative Fitness'

mpl.colorbar.ColorbarBase(cax, cmap=cm.jet, norm=norm, orientation='horizontal').set_label(lbl)

savefig(outfile)

