#!/usr/bin/python

import glob
import os
from optparse import OptionParser
import sys

# Set up options
usage = """usage: %prog [options] graph1 [graph2 ...]

Permitted types for graph are mod_all, mod_summary, 
phys_mod_by_treatment, phys_mod_unity_scatter, phys_mod_gaps, 
phys_mod_unity, phys_mod_scatter, phys_mod_gapmean,
phys_mod_gapmedian, phys_mod_gapvar, phys_mod_gapstd

phys_mod_gapstd_organisms, phys_mod_gapmean_organisms

funct_mod, funct_mod_organisms, tasks, fitness, or all

map_task_all, lineage_mutation_profile

"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

parser.add_option("-t","--treatment", dest = "treatment", help = "What's the experiment name")

parser.add_option("--title", dest = "title", help = "Add a supplemental title")

parser.add_option("-l","--script_location", dest = "location", help = "script directory location")

parser.add_option("-e", "--error_bars", action = "store_true", dest = "error_bars",
                  default = False, help = "Draw Error Bars")

parser.add_option("-p", "--pattern", dest = "pattern", help = "Pattern")

## fetch the args
(options, args) = parser.parse_args()


## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

if not options.location:
    parser.error("script directory path is required")


## actions
graphs = args[0:]

plot_from_csv_path="%s/generate_graphs_from_raw_data/plot_from_csv.py" % options.location
draw_map_task_path="../../%s/evolution_of_modularity_pipelines/draw_map_task__using_lineage_and_alignment.py" % options.location
plot_barchart_from_csv_path="%s/generate_graphs_from_raw_data/bar_chart_from_csv.py" % options.location

pattern = "*_??????"
if options.pattern:
    pattern = options.pattern

treatment = ""
if options.treatment:
    treatment = options.treatment

title = ""
if options.title:
    title = " - %s" % options.title

error_bars_name = ""
error_bars_opt = ""
if options.error_bars:
    error_bars_name = "__with_error_bars"
    error_bars_opt = " --calculate_error"

show_opt = ""

if "map_task_all" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#;
# "Plot all the map tasks";
for i in %s; do echo $i ; if [ -e $i/data ] ; then cd $i/data/;  python %s --show_phase --aligned_lineage_map --lineage_map --task_map --mutation_map --aligned_task_map --show_mutations --title "$i%s" -v -a ../$TREATMENT.png 5 6 8 lineage.dat ./phenotype/; cd ../../ ; else echo "Data dir not found." ; fi ; done ;
""" % (treatment, pattern, draw_map_task_path, title)

    print command
#    os.popen(command)



if "mod_all" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#;
# "Plot all Modularity";
python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 13 -t "$TREATMENT%s" -x "Updates" -y "Modularity" \
modularity_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__functional_modularity.csv" \
control_$TREATMENT"__backbone_task_unity.csv" \
control_$TREATMENT"__backbone_task_scatter.csv" \
control_$TREATMENT"__backbone_task_gapmean.csv" \
control_$TREATMENT"__backbone_task_gapmedian.csv" \
control_$TREATMENT"__backbone_task_gapvar.csv" \
control_$TREATMENT"__backbone_task_gapstd.csv" \
control_$TREATMENT"__fluct_task_unity.csv" \
control_$TREATMENT"__fluct_task_scatter.csv" \
control_$TREATMENT"__fluct_task_gapmean.csv" \
control_$TREATMENT"__fluct_task_gapmedian.csv" \
control_$TREATMENT"__fluct_task_gapvar.csv" \
control_$TREATMENT"__fluct_task_gapstd.csv" \
noreward_$TREATMENT"__functional_modularity.csv" \
noreward_$TREATMENT"__backbone_task_unity.csv" \
noreward_$TREATMENT"__backbone_task_scatter.csv" \
noreward_$TREATMENT"__backbone_task_gapmean.csv" \
noreward_$TREATMENT"__backbone_task_gapmedian.csv" \
noreward_$TREATMENT"__backbone_task_gapvar.csv" \
noreward_$TREATMENT"__backbone_task_gapstd.csv" \
noreward_$TREATMENT"__fluct_task_unity.csv" \
noreward_$TREATMENT"__fluct_task_scatter.csv" \
noreward_$TREATMENT"__fluct_task_gapmean.csv" \
noreward_$TREATMENT"__fluct_task_gapmedian.csv" \
noreward_$TREATMENT"__fluct_task_gapvar.csv" \
noreward_$TREATMENT"__fluct_task_gapstd.csv" \
punish_$TREATMENT"__functional_modularity.csv" \
punish_$TREATMENT"__backbone_task_unity.csv" \
punish_$TREATMENT"__backbone_task_scatter.csv" \
punish_$TREATMENT"__backbone_task_gapmean.csv" \
punish_$TREATMENT"__backbone_task_gapmedian.csv" \
punish_$TREATMENT"__backbone_task_gapvar.csv" \
punish_$TREATMENT"__backbone_task_gapstd.csv" \
punish_$TREATMENT"__fluct_task_unity.csv" \
punish_$TREATMENT"__fluct_task_scatter.csv" \
punish_$TREATMENT"__fluct_task_gapmean.csv" \
punish_$TREATMENT"__fluct_task_gapmedian.csv" \
punish_$TREATMENT"__fluct_task_gapvar.csv" \
punish_$TREATMENT"__fluct_task_gapstd.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)

    os.popen(command)

    print command


if "mod_summary" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Modularity Summary"
python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 5 -t "$TREATMENT%s" -x "Updates" -y "Modularity" \
modularity_summary_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__functional_modularity.csv" \
control_$TREATMENT"__backbone_task_unity.csv" \
control_$TREATMENT"__backbone_task_scatter.csv" \
control_$TREATMENT"__fluct_task_unity.csv" \
control_$TREATMENT"__fluct_task_scatter.csv" \
noreward_$TREATMENT"__functional_modularity.csv" \
noreward_$TREATMENT"__backbone_task_unity.csv" \
noreward_$TREATMENT"__backbone_task_scatter.csv" \
noreward_$TREATMENT"__fluct_task_unity.csv" \
noreward_$TREATMENT"__fluct_task_scatter.csv" \
punish_$TREATMENT"__functional_modularity.csv" \
punish_$TREATMENT"__backbone_task_unity.csv" \
punish_$TREATMENT"__backbone_task_scatter.csv" \
punish_$TREATMENT"__fluct_task_unity.csv" \
punish_$TREATMENT"__fluct_task_scatter.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command

if "funct_mod_organisms" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Functional Modularity - By Organisms"


python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 1 -t "Functional Modularity - $TREATMENT%s - By Organisms" -x "Updates" -y "Modularity" \
functional_modularity_by_task__$TREATMENT"%s__two_task__organisms.png" \
control_$TREATMENT"__functional_modularity__organisms.csv" \
noreward_$TREATMENT"__functional_modularity__organisms.csv" \
punish_$TREATMENT"__functional_modularity__organisms.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command

if "funct_mod" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Functional Modularity"


python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 1 -t "Functional Modularity - $TREATMENT%s" -x "Updates" -y "Modularity" \
functional_modularity_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__functional_modularity.csv" \
noreward_$TREATMENT"__functional_modularity.csv" \
punish_$TREATMENT"__functional_modularity.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


###### ALL MEASURES PHYSICAL MODULARITY $TREATMENT
if "phys_mod_by_treatment" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity"
python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 6 -t "Control - $TREATMENT%s" -x "Updates" -y "Modularity" \
control_physical_modularity_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_unity.csv" \
control_$TREATMENT"__backbone_task_scatter.csv" \
control_$TREATMENT"__backbone_task_gapmean.csv" \
control_$TREATMENT"__backbone_task_gapmedian.csv" \
control_$TREATMENT"__backbone_task_gapvar.csv" \
control_$TREATMENT"__backbone_task_gapstd.csv" \
control_$TREATMENT"__fluct_task_unity.csv" \
control_$TREATMENT"__fluct_task_scatter.csv" \
control_$TREATMENT"__fluct_task_gapmean.csv" \
control_$TREATMENT"__fluct_task_gapmedian.csv" \
control_$TREATMENT"__fluct_task_gapvar.csv" \
control_$TREATMENT"__fluct_task_gapstd.csv" \

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 6 -t "No Reward - $TREATMENT%s" -x "Updates" -y "Modularity" \
noreward_physical_modularity_by_task__$TREATMENT"%s__two_task.png" \
noreward_$TREATMENT"__backbone_task_unity.csv" \
noreward_$TREATMENT"__backbone_task_scatter.csv" \
noreward_$TREATMENT"__backbone_task_gapmean.csv" \
noreward_$TREATMENT"__backbone_task_gapmedian.csv" \
noreward_$TREATMENT"__backbone_task_gapvar.csv" \
noreward_$TREATMENT"__backbone_task_gapstd.csv" \
noreward_$TREATMENT"__fluct_task_unity.csv" \
noreward_$TREATMENT"__fluct_task_scatter.csv" \
noreward_$TREATMENT"__fluct_task_gapmean.csv" \
noreward_$TREATMENT"__fluct_task_gapmedian.csv" \
noreward_$TREATMENT"__fluct_task_gapvar.csv" \
noreward_$TREATMENT"__fluct_task_gapstd.csv" \

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 6 -t "Punish - $TREATMENT%s" -x "Updates" -y "Modularity" \
punish_physical_modularity_by_task__$TREATMENT"%s__two_task.png" \
punish_$TREATMENT"__backbone_task_unity.csv" \
punish_$TREATMENT"__backbone_task_scatter.csv" \
punish_$TREATMENT"__backbone_task_gapmean.csv" \
punish_$TREATMENT"__backbone_task_gapmedian.csv" \
punish_$TREATMENT"__backbone_task_gapvar.csv" \
punish_$TREATMENT"__backbone_task_gapstd.csv" \
punish_$TREATMENT"__fluct_task_unity.csv" \
punish_$TREATMENT"__fluct_task_scatter.csv" \
punish_$TREATMENT"__fluct_task_gapmean.csv" \
punish_$TREATMENT"__fluct_task_gapmedian.csv" \
punish_$TREATMENT"__fluct_task_gapvar.csv" \
punish_$TREATMENT"__fluct_task_gapstd.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command




###### PHYSICAL MODULARITY UNITY/SCATTER
if "phys_mod_unity_scatter" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Unity/Scatter"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 1 --data_sources 4 -t "Physical Modularity - Unity/Scatter - $TREATMENT%s" -x "Updates" -y "Modularity" \
physical_modularity_by_task__unity_scatter__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_unity.csv" \
control_$TREATMENT"__backbone_task_scatter.csv" \
control_$TREATMENT"__fluct_task_unity.csv" \
control_$TREATMENT"__fluct_task_scatter.csv" \
noreward_$TREATMENT"__backbone_task_unity.csv" \
noreward_$TREATMENT"__backbone_task_scatter.csv" \
noreward_$TREATMENT"__fluct_task_unity.csv" \
noreward_$TREATMENT"__fluct_task_scatter.csv" \
punish_$TREATMENT"__backbone_task_unity.csv" \
punish_$TREATMENT"__backbone_task_scatter.csv" \
punish_$TREATMENT"__fluct_task_unity.csv" \
punish_$TREATMENT"__fluct_task_scatter.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command



###### PHYSICAL MODULARITY Gap Measures
if "phys_mod_gaps" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Gap Measures"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 8 -t "Physical Modularity - Gap Measures - $TREATMENT%s" -x "Updates" -y "Modularity" \
physical_modularity_by_task__gapmeasures__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_gapmean.csv" \
control_$TREATMENT"__backbone_task_gapmedian.csv" \
control_$TREATMENT"__backbone_task_gapvar.csv" \
control_$TREATMENT"__backbone_task_gapstd.csv" \
control_$TREATMENT"__fluct_task_gapmean.csv" \
control_$TREATMENT"__fluct_task_gapmedian.csv" \
control_$TREATMENT"__fluct_task_gapvar.csv" \
control_$TREATMENT"__fluct_task_gapstd.csv" \
noreward_$TREATMENT"__backbone_task_gapmean.csv" \
noreward_$TREATMENT"__backbone_task_gapmedian.csv" \
noreward_$TREATMENT"__backbone_task_gapvar.csv" \
noreward_$TREATMENT"__backbone_task_gapstd.csv" \
noreward_$TREATMENT"__fluct_task_gapmean.csv" \
noreward_$TREATMENT"__fluct_task_gapmedian.csv" \
noreward_$TREATMENT"__fluct_task_gapvar.csv" \
noreward_$TREATMENT"__fluct_task_gapstd.csv" \
punish_$TREATMENT"__backbone_task_gapmean.csv" \
punish_$TREATMENT"__backbone_task_gapmedian.csv" \
punish_$TREATMENT"__backbone_task_gapvar.csv" \
punish_$TREATMENT"__backbone_task_gapstd.csv" \
punish_$TREATMENT"__fluct_task_gapmean.csv" \
punish_$TREATMENT"__fluct_task_gapmedian.csv" \
punish_$TREATMENT"__fluct_task_gapvar.csv" \
punish_$TREATMENT"__fluct_task_gapstd.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command



#### UNITY
if "phys_mod_unity" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Unity"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 1 --data_sources 2 -t "Unity - $TREATMENT%s" -x "Updates" -y "Modularity" \
unity_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_unity.csv" \
control_$TREATMENT"__fluct_task_unity.csv" \
noreward_$TREATMENT"__backbone_task_unity.csv" \
noreward_$TREATMENT"__fluct_task_unity.csv" \
punish_$TREATMENT"__backbone_task_unity.csv" \
punish_$TREATMENT"__fluct_task_unity.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### SCATTER
if "phys_mod_scatter" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Scatter"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 1 --data_sources 2 -t "Scatter - $TREATMENT%s" -x "Updates" -y "Modularity" \
scatter_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_scatter.csv" \
control_$TREATMENT"__fluct_task_scatter.csv" \
noreward_$TREATMENT"__backbone_task_scatter.csv" \
noreward_$TREATMENT"__fluct_task_scatter.csv" \
punish_$TREATMENT"__backbone_task_scatter.csv" \
punish_$TREATMENT"__fluct_task_scatter.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command

#### Gap Mean - By Organisms
if "phys_mod_gapmean_organisms" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - GapMean - By Organisms"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 3 --data_sources 2 -t "Gap Mean - $TREATMENT%s - By Organisms" -x "Updates" -y "Modularity" \
gapmean_by_task__$TREATMENT"%s__two_task__organisms.png" \
control_$TREATMENT"__backbone_task_gapmean__organisms.csv" \
control_$TREATMENT"__fluct_task_gapmean__organisms.csv" \
noreward_$TREATMENT"__backbone_task_gapmean__organisms.csv" \
noreward_$TREATMENT"__fluct_task_gapmean__organisms.csv" \
punish_$TREATMENT"__backbone_task_gapmean__organisms.csv" \
punish_$TREATMENT"__fluct_task_gapmean__organisms.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### Gap Mean
if "phys_mod_gapmean" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - GapMean"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 3 --data_sources 2 -t "Gap Mean - $TREATMENT%s" -x "Updates" -y "Modularity" \
gapmean_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_gapmean.csv" \
control_$TREATMENT"__fluct_task_gapmean.csv" \
noreward_$TREATMENT"__backbone_task_gapmean.csv" \
noreward_$TREATMENT"__fluct_task_gapmean.csv" \
punish_$TREATMENT"__backbone_task_gapmean.csv" \
punish_$TREATMENT"__fluct_task_gapmean.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### Gap Median
if "phys_mod_gapmedian" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#"Plot Physical Modularity - GapMedian"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 2 -t "Gap Median - $TREATMENT%s" -x "Updates" -y "Modularity" \
gapmedian_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_gapmedian.csv" \
control_$TREATMENT"__fluct_task_gapmedian.csv" \
noreward_$TREATMENT"__backbone_task_gapmedian.csv" \
noreward_$TREATMENT"__fluct_task_gapmedian.csv" \
punish_$TREATMENT"__backbone_task_gapmedian.csv" \
punish_$TREATMENT"__fluct_task_gapmedian.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### Gap Var
if "phys_mod_gapvar" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - GapVar"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 60 --data_sources 2 -t "Gap Var - $TREATMENT%s" -x "Updates" -y "Modularity" \
gapvar_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_gapvar.csv" \
control_$TREATMENT"__fluct_task_gapvar.csv" \
noreward_$TREATMENT"__backbone_task_gapvar.csv" \
noreward_$TREATMENT"__fluct_task_gapvar.csv" \
punish_$TREATMENT"__backbone_task_gapvar.csv" \
punish_$TREATMENT"__fluct_task_gapvar.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### Gap STD - By Organisms
if "phys_mod_gapstd_organisms" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Gap STD - By Organism"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 2 -t "Gap STD - $TREATMENT%s - By Organism" -x "Updates" -y "Modularity" \
gapstd_by_task__$TREATMENT"%s__two_task__organisms.png" \
control_$TREATMENT"__backbone_task_gapstd__organisms.csv" \
control_$TREATMENT"__fluct_task_gapstd__organisms.csv" \
noreward_$TREATMENT"__backbone_task_gapstd__organisms.csv" \
noreward_$TREATMENT"__fluct_task_gapstd__organisms.csv" \
punish_$TREATMENT"__backbone_task_gapstd__organisms.csv" \
punish_$TREATMENT"__fluct_task_gapstd__organisms.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command

#### Gap STD
if "phys_mod_gapstd" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot Physical Modularity - Gap STD"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 6 --data_sources 2 -t "Gap STD - $TREATMENT%s" -x "Updates" -y "Modularity" \
gapstd_by_task__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__backbone_task_gapstd.csv" \
control_$TREATMENT"__fluct_task_gapstd.csv" \
noreward_$TREATMENT"__backbone_task_gapstd.csv" \
noreward_$TREATMENT"__fluct_task_gapstd.csv" \
punish_$TREATMENT"__backbone_task_gapstd.csv" \
punish_$TREATMENT"__fluct_task_gapstd.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command



#### Two-Task organisms
if "tasks" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot # of Organisms doing both tasks"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 4000 --data_sources 1 -t "Organisms Doing Both Tasks - $TREATMENT%s" -x "Updates" -y "Organisms" \
organisms_doing_both_tasks__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__fluct_task_count.csv" \
noreward_$TREATMENT"__fluct_task_count.csv" \
punish_$TREATMENT"__fluct_task_count.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command


#### Two-Task fitness
if "fitness" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot fitness of Organisms doing both tasks"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --ylim_max 140 --data_sources 1 -t "Fitness - $TREATMENT%s" -x "Updates" -y "Fitness" \
fitness_both_tasks__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__fitness.csv" \
noreward_$TREATMENT"__fitness.csv" \
punish_$TREATMENT"__fitness.csv" \
""" % (treatment,plot_from_csv_path, show_opt, error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command



#### Two-Task coalescent generations
if "coalescent" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot coalescent generations"

python %s -o %s --x_tick_intervals 50 --show_phase 1000 --legend%s --data_sources 1 -t "Coalescent Generations - $TREATMENT%s" -x "Updates" -y "Coalescent Generations" \
coalescent_generations__$TREATMENT"%s__two_task.png" \
control_$TREATMENT"__coalescent.csv" \
noreward_$TREATMENT"__coalescent.csv" \
punish_$TREATMENT"__coalescent.csv" \
""" % (treatment,plot_from_csv_path, show_opt ,error_bars_opt, title, error_bars_name)
    os.popen(command)

    print command

#### Dominant Lineage Profile
if "lineage_mutation_profile" in graphs or "all" in graphs:

    command="""
TREATMENT=%s;
#
# "Plot dominant lineage's mutation profile"

python %s --legend --title "Dominant Lineage Mutation Profile - $TREATMENT%s" -y "Mean Mutations per Generation" -x "Treatment" --column_labels "Degenerate Mutations, Coding Mutations" "3,1" \
mean_mutations_per_generation__$TREATMENT".png" \
control_$TREATMENT"__mean_dominant_lineage_mutation_metrics.csv" \
noreward_$TREATMENT"__mean_dominant_lineage_mutation_metrics.csv" \
punish_$TREATMENT"__mean_dominant_lineage_mutation_metrics.csv" \
""" % (treatment, plot_barchart_from_csv_path, title)
    os.popen(command)

    print command




