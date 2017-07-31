#!/usr/bin/python

###################
# Analyze
###################

# system includes
import glob
import os
from optparse import OptionParser
import sys

sys.path.append( os.path.abspath( os.path.join( sys.path[0], "common/" ) ) ) ## to common/
import config as cf

# note the paths to the utilities
analyzepath = os.path.abspath( os.path.join( sys.path[0], "analysis/analyze.py" ) )
plotpath = os.path.abspath( os.path.join( sys.path[0], "graph_generation/plot_from_csv.py" ) )
#plotpath = os.path.abspath( os.path.join( sys.path[0], "graph_generation/plot_from_csv__twinx.py" ) )
#plotpath = os.path.abspath( os.path.join( sys.path[0], "graph_generation/plot_from_csv__stripped.py" ) )


# Set up options
usage = """usage: %prog [options] outfile [input_file1 column1 \"directory_glob1\" name1 .. input_fileN columnN \"directory_globN\" nameN] 
          
"""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
parser.add_option("-d", "--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")
parser.add_option("--plotonly", action = "store_true", dest = "plotonly",
                  default = False, help = "Skip the aggregation step, and plot only, using existing data files.")
parser.add_option("--noplot", action = "store_true", dest = "noplot",
                  default = False, help = "Skip the plotting step, only aggregate the data files.")
parser.add_option("-t", "--title", dest = "title",
                  help = "set a different title than outfile (default)")
parser.add_option("-x", "--xlabel", dest="xlabel", 
                  help="X-axis Label")
parser.add_option("-y", "--ylabel", dest="ylabel", 
                  help="Y-axis Label")
parser.add_option("--include_chevrons", dest="include_chevrons", 
                  action="store_true", default = False, 
                  help="Include line marker glyphs in addition to color") 
parser.add_option("--chevrons_by_members", dest="member_chevrons", 
                  action="store_true", default = False, 
                  help="Make the chevrons track by members, along with line style")                  
parser.add_option("--data_members", dest="member_count",
                  help="Number of Components from a given data source (treatment)")
parser.add_option("--alt_axis", dest="alt_axis", type="int",
                  help="Use an alternative axis for the Nth data source")  
parser.add_option("-w", "--ylabel_alt_axis", dest="y_label_alt_axis", type="string", 
                  help="Alternative Y-axis Label")                  
parser.add_option("--xtick_multiplier", dest="xtick_multiplier", 
                  help="X-axis Tick Multipliers")
parser.add_option("--ylog", action="store_true", dest="ylog",
                  help="Y-axis logarithmic scale")
parser.add_option("--ylim_max", dest="ylim_max", type="float",
                  help="Set the ylim max")        
parser.add_option("--ylim_min", dest="ylim_min", type="float",
                  help="Set the ylim min")                         
parser.add_option("--error", dest="calculate_error", action="store_true", default = False,
                  help="include error bars - error values will be calculated from data using bootstrap")
parser.add_option("--samples", dest="samples",
                  help="how many samples to draw for bootstrap?")
parser.add_option("--end_at", dest="end_at",
                  help="Stop plotting at datapoint <end_at>")
## fetch the args
(options, args) = parser.parse_args()

## parameter errors
if len(args) < 5: #outfile, plus a singular input set
    parser.error("incorrect number of arguments")

if (len(args[1:]) % 4) != 0:
    parser.error("incorrectly formatted input sets. (infile, column, directory glob, and name)")

outfile = args[0]

input_set_count = len(args[1:]) / 4

#input_set_count = 1
#if options.input_set_count:
#    input_set_count = int(options.input_set_count)

title = outfile
if options.title:
    title = options.title

error_opt = ""
if options.calculate_error:
    error_opt = " --error"

samples_opt = ""
if options.samples:
    samples_opt = " --samples " + options.samples


xlabel_opt = ""
if options.xlabel:
    xlabel_opt = " --xlabel \"" + options.xlabel + "\"" 

ylimmax_opt = ""
if options.ylim_max:
    ylimmax_opt = " --ylim_max \"" + str(options.ylim_max) + "\"" 

ylimmin_opt = ""
#print "HHHHIIII"
if options.ylim_min != None:
#    print "WHWHWHHWHW"
    ylimmin_opt = " --ylim_min \"" + str(options.ylim_min) + "\"" 

ylabel_opt = ""
if options.ylabel:
    ylabel_opt = " --ylabel \"" + options.ylabel + "\"" 

datamembers_opt = ""
if options.member_count:
    datamembers_opt = " --data_members " + options.member_count  

altax_opt = ""
if options.alt_axis:
    altax_opt = " --alt_axis " + str(options.alt_axis)   
    
ylabel_altax_opt = ""
if options.y_label_alt_axis:
    ylabel_altax_opt = " --ylabel_alt_axis \"" + str(options.y_label_alt_axis) + "\""

    

xtickmult_opt = ""
if options.xtick_multiplier:
    xtickmult_opt = " --xtick_multiplier " + options.xtick_multiplier

endat_opt = ""
if options.end_at:
    endat_opt = " --end_at " + options.end_at 

ylog_opt = ""
if options.ylog:
    ylog_opt = " --ylog"
    
chev_opt = ""
if options.include_chevrons:
    chev_opt = " --include_chevrons"
    
    
memchev_opt = ""
if options.member_chevrons:
    memchev_opt = " --chevrons_by_members"


## extract the list of input files and columns
input_files = []
columns = []
globs = []
names = []

for i in range(1, (input_set_count*4) + 1, 4):
    input_files.append( args[i] )
    columns.append( args[i + 1] )
    globs.append( args[i + 2] )
    names.append( args[i + 3] )

#print input_files
#print columns
#print globs
#print names

if input_set_count != len(input_files) != len(columns) != len(globs) != len(names):
    parser.error("input_set_count must equal the number of input files, columns, and directory globs")

expanded_globs = []
for thing in globs:
    thing = thing.strip('\"')
    output = glob.glob(thing)
    if len(output) > 0:
        expanded_globs.append( output )

if len(expanded_globs) < 1 :
    parser.error("directory glob: "+str(globs) +"  does not interpret into anything.")
    
aggregated_names = []
for i in range(0, input_set_count):
    ####### FIRST, DO THE AGGREGATIONS
    
    ag_name = outfile + "." + names[i]
    aggregated_names.append( ag_name )

    command = "python2 " + analyzepath + " -i \"" + input_files[i] + "*\" -c " + columns[i] + " -o " + ag_name + " timeseries " + " ".join(expanded_globs[i])

    print "Aggregating " + names[i] + " to " + ag_name  
    if options.plotonly:
        print "~~SKIPPING, PLOTTING ONLY~~"
    else:
        if options.verbose:
            print command
            print os.popen( command ).read()
        else:
            os.popen( command ).read()
            
####### THEN, PLOT IT.

agnames_csv = [ name + ".timeseries.csv" for name in aggregated_names ]

command = "python2 " + plotpath + " -o --title \"" + title + "\"" + error_opt + samples_opt + ylog_opt + endat_opt + xlabel_opt + ylabel_opt + ylimmax_opt + ylimmin_opt + datamembers_opt + altax_opt + ylabel_altax_opt + chev_opt + memchev_opt + xtickmult_opt + " --legend \"" + ",".join(names) + "\" " + outfile + ".png " + " ".join(agnames_csv)

#print command
print "Plotting " + outfile
if options.noplot:
    print "~~SKIPPING, AGGREGATING ONLY~~"
else:
    if (options.verbose):
        print command
        print os.popen( command ).read()
    else:    
        os.popen(command)