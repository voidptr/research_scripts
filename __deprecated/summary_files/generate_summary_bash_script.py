# Generate a summary file from a run_list 

# Written in Python 2.7
# RCK
# 8-21-11

#import sys
#sys.path.append('../common modules and helper scripts')

from optparse import OptionParser

# Set up options
usage = """usage: %prog [options] run_list_path output_directory scripts_directory
"""
#Permitted types for outfile are png, pdf, ps, eps, and svg"""
parser = OptionParser(usage)

## fetch the args
(options, args) = parser.parse_args()

## parameter error
if len(args) < 3:
    parser.error("incorrect number of arguments")

run_list_path = args[0]
output_directory = args[1]
scripts_directory = args[2]

fd = open(run_list_path)
data_dirs = []
for line in fd:
    line = line.strip()

    if (len(line) == 0 or line[0] == '#'): ## skip empty lines and comments
        continue

    line = line.split()

    if (line[0] == 'set'): ## skip these too
        continue

    data_dirs.append( line[1] )

fd.close()

## generate generate_graphs.bash

print "echo \"<h3>\" > " + output_directory + "/data.html"
print "cat README.txt >> " + output_directory + "/data.html"
print "echo \"</h3>\" >> " + output_directory + "/data.html"

## generate fitness graphs

print "# generate graphs"
fitness_template = "python \"" + scripts_directory + "\"/single_column_graph.py -l -m " + output_directory + "/fitness_$.png Fitness 4 \"x50 updates\" " + "$_??????/data/average.dat*"
tasks_template = "python \"" + scripts_directory + "\"/multi_column_graph.py " + output_directory + "/tasks_$.png Tasks \"x50 updates\" " + "$_??????/data/tasks.dat*"
coalescent_template = "python \"" + scripts_directory + "\"/single_column_graph.py -m " + output_directory + "/coalescentgenerations_$.png \"Coalescent Generations\" 10 \"x50 updates\" " + "$_??????/data/stats.dat*"

for data_dir in data_dirs:
    fitness_command = fitness_template.replace( "$", data_dir )
    tasks_command = tasks_template.replace( "$", data_dir )
    coalescent_command = coalescent_template.replace( "$", data_dir )

    print "#" + data_dir

    print fitness_command
    print tasks_command
    print coalescent_command

    print


print "# stack figures"
stack_figures_template = "python \"" + scripts_directory + "\"/stack_figures.py $ " + output_directory + "/*_$.png >> " + output_directory + "/data.html"
for data_dir in data_dirs:
    stack_figures_command = stack_figures_template.replace( "$", data_dir )

    print stack_figures_command
    print


