# Draw the placements of where the tasks are

# Written in Python 2.7
# RCK
# 10-19-11

from optparse import OptionParser
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import os
import gzip


# Set up options
usage = """usage: %prog [options] output_filename tasksites.org-1.dat [tasksites.org-2.dat ...]

"""
parser = OptionParser(usage)
parser.add_option("-i", "--individual", action = "store_true", dest = "store_individual",
                  default = False, help = "save images individually")
parser.add_option("-t", "--trim", action = "store_true", dest = "trim_whitespace",
                  default = False, help = "trim the whitespace")
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "verbose mode")
parser.add_option("-p", "--phase", dest = "phase", metavar = "START_UPDATE",
                  default = -1, type="int", help = "show the phase (reward vs noreward/punish)")
parser.add_option("-P", "--phase_only", dest = "phase_only", metavar = "PHASE_1_or_2",
                  default = -1, type="int", help = "only show the phase we want 1/2")




## fetch the args
(options, args) = parser.parse_args()
if options.store_individual:
    options.trim_whitespace = True

if options.phase_only > -1 and options.phase == -1:
    parser.error("-P or --phase_only requires passing of phase START_UPDATE using -p or --phase")

## parameter error
if len(args) < 2:
    parser.error("incorrect number of arguments")

outfile_name = args[0]
tasksites_files = args[1:]

## the stack of organisms to display
organisms = []

## site colors
sc_default = 0
sc_black = 0
sc_purple = 10
sc_blue = 25
sc_green = 50
sc_yellow = 75
sc_orange = 80
sc_red = 85
sc_darkpink = 99.6
sc_gray = 100

## assignment of meaning to color
pm_gainbb_gainfl = sc_gray ## these three are weird, but I guess I only care about gains when there are losses of function.
pm_gainbb_neutfl = sc_gray
pm_gainbb_losefl = sc_green ## this is a fluctuating only site, but interesting because losing it gains you the backbone task, so mark it green instead of blue

pm_neutbb_gainfl = sc_gray
pm_neutbb_neutfl = sc_gray
pm_neutbb_losefl = sc_blue ## this is a fluctuating only site

pm_losebb_gainfl = sc_orange ## this is a backbone only site, but interesting because losing it gains you the fluctuating task, so mark it orange instead of red
pm_losebb_neutfl = sc_red ## this is a backbone only site
pm_losebb_losefl = sc_purple ## this is both backbone and fluctuating

## set up the probability matrix
color_matrix = [[pm_gainbb_gainfl,   pm_gainbb_neutfl,   pm_gainbb_losefl], ## visually inverted (X coordinates go down)
                [pm_neutbb_gainfl,   pm_neutbb_neutfl,   pm_neutbb_losefl],
                [pm_losebb_gainfl,   pm_losebb_neutfl,   pm_losebb_losefl]]

## site task_status (as index into color_matrix)
stat_gained = 0
stat_neutral = 1
stat_lost = 2

####### TEST CODE display all the colors
#test_organism = [
#    sc_default, sc_default, sc_default, sc_default, sc_default,
#    sc_black,sc_black,sc_black,sc_black,sc_black,
#    sc_purple,sc_purple,sc_purple,sc_purple,sc_purple,
#    sc_blue,sc_blue,sc_blue,sc_blue,sc_blue,
#    sc_green,sc_green,sc_green,sc_green,sc_green,
#    sc_yellow,sc_yellow,sc_yellow,sc_yellow,sc_yellow,
#    sc_orange,sc_orange,sc_orange,sc_orange,sc_orange,
#    sc_red,sc_red,sc_red,sc_red,sc_red,
#    sc_gray,sc_gray,sc_gray,sc_gray,sc_gray]
#organisms.append( test_organism )
#organisms.append( test_organism )
#organisms.append( test_organism )
#organisms.append( test_organism )
#organisms.append( test_organism )
####### END TEST


for tasksite_file in tasksites_files:

    ## pull out the update (assumes the map tasks file is in a map_tasks-nnnnnn/ directory
    update_str = tasksite_file.split('-')[1].split('/')[0]


    if (options.phase_only > -1):
        if (int(update_str) <= options.phase):
            continue # ignore any files that aren't part of the cycles        

        if ((int(update_str) % 1000) > 0 and options.phase_only != 1): ## we are at the end of a no-reward phase (nnn500), which we don't want to display
            continue

        if ((int(update_str) % 1000) == 0 and options.phase_only != 2): ## we are at the end of a reward phase (nnn000), which we don't want to display
            continue


    if (options.phase > -1):
        if (int(update_str) > options.phase and (int(update_str) % 1000) > 0): ## we at the end of a no-reward phase (nnn500)
            color_matrix[1][1] = sc_darkpink ## DO IT HERE (half assed)
        else:
            color_matrix[1][1] = sc_gray ## DO IT HERE (half assed)



    if (options.verbose):
        print tasksite_file

    #fp = open( tasksite_file )

    if tasksite_file[-3:] == ".gz":
        fp = gzip.open(tasksite_file)
    else:
        fp = open(tasksite_file)

    organisms.append( [] ) ## to hold the per-site data of the organism

    organism_task_execution = -1
    for line in fp:

        line = line.strip()
        if len(line) == 0 or line[0] == '#': ## skip it
            continue

        line = line.replace(' ',',') ## doing this because the split method concatenates spaces all in a row
        line = line.split(',') 

        # the first line contains the base organism stuff
        if (organism_task_execution == -1): ## fill in the first line
            organism_task_execution = line[-2] + line[-1] ## the last two tasks
            continue

        site_task_execution = line[-2] + line[-1] ## the last two tasks
        site_fitness = float( line[3] )

        site_color = sc_black
        if (site_fitness == 0): ## killed it
            site_color = sc_black
        else: ## check the status
           

            # deal with the backbone first
            if (int(site_task_execution[0]) < int(organism_task_execution[0])): ## lost the backbone
                backbone_status = stat_lost 
            elif (int(site_task_execution[0]) == int(organism_task_execution[0])): ## neutral effect
                backbone_status = stat_neutral
            else:
                backbone_status = stat_gained

            # deal with the fluctuating task
            if (int(site_task_execution[1]) < int(organism_task_execution[1])): ## lost the backbone
                fluct_status = stat_lost
            elif (int(site_task_execution[1]) == int(organism_task_execution[1])): ## neutral effect
                fluct_status = stat_neutral
            else:
                fluct_status = stat_gained

            site_color = color_matrix[backbone_status][fluct_status] ## set the color based on the probability matrix and the task status
    
            if (options.verbose):
                print tasksite_file + " WT vs Mut: "+ organism_task_execution  + " " + site_task_execution + " color: " + str(site_color) + " status: " + str(backbone_status) + str(fluct_status)

        organisms[-1].append( site_color ) ## add the site color to the organism site array        

    organisms[-1].append(sc_black) ## making sure the damned thing displays the right colors, for fucks sake. :(
    organisms[-1].append(sc_gray)

    fp.close()

### go through the organism genotypes we collected, and normalize
max_length = max( [ len(organism) for organism in organisms ] )
for organism in organisms: ## set each array to be the max length
    for i in range(0, max_length - len(organism)):
        organism.append(sc_default)


######### NOW GENERATE THE PLOT(S) ###############

def generate_plot( filename, organisms ):
    plottable_organisms = np.array( organisms )

    fig = plt.figure()

    if options.trim_whitespace:
        ax = fig.add_axes((0,0,1,1))
        ax.set_axis_off()
        ax.imshow(organisms, cmap=cm.spectral, interpolation='nearest')
        plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0)
        plt.savefig(filename, pad_inches=0)

        ## trim the fat
        os.system('convert '+filename+' -bordercolor white -border 1x1 -trim +repage -alpha off +dither -colors 32 PNG8:'+filename)
    else:
        ax = fig.add_subplot(111) ## 1 row, 1 column, first plot
        ax.imshow(organisms, cmap=cm.spectral, interpolation='nearest')

        plt.title("Task knockouts by site in dominant organisms") 
        plt.ylabel("updates")
        plt.xlabel("site")

        ylocs, ylabels = plt.yticks()
        ymodlabels = []
        ymodlocs = []
        for i in range(0, len(ylocs)):
            if ( ylocs[i] * 500 ) >= 0 and (ylocs[i]* 500) < 110000:
                ymodlabels.append(ylocs[i] * 500 )
                ymodlocs.append(ylocs[i] )
        plt.yticks( ymodlocs, ymodlabels )

        plt.savefig(filename)


## save each organism's thing individually
if options.store_individual:
    count = 0
    for tasksite_file in tasksites_files:
        update = tasksite_file.split('/')[-2].replace('_','')

        individual_filename = outfile_name.replace('.','_'+update+".")
        generate_plot( individual_filename, [organisms[count]] )

        count += 1 ## increment the count
## save them all in one fancy plot
else:     
    generate_plot( outfile_name, organisms )


