#!/usr/bin/python

# Load a saved network with position information in an interactive window

# Written in Python 2.7
# RCK
# 3-24-11


from graph_tool.all import *
from optparse import OptionParser
import matplotlib
import random
import math

# Set up options
usage = """usage: %prog [options] <network.xml> <outfile.png>

script must be run from the same directory as Avida."""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")
                  
parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

parser.add_option("--save", dest = "save", type="string",
                  default = None, help = "Output the graph, including the position.")

## fetch the args
(options, args) = parser.parse_args()
## parameter errors
if len(args) < 1:
    parser.error("incorrect number of arguments")

networkfile = args[0]


 
def interactive_figure():
    g = load_graph(networkfile, "gt")
    print "LOADED"
    print g
 
    num_cpus = g.vertex_properties["num_cpus"]
    fitnesses = g.vertex_properties["fitnesses"]
    steps = g.vertex_properties["steps"]
    pos = None
    if "pos" in g.vertex_properties.keys():
        pos = g.vertex_properties["pos"]        
    
    alleles_cluster = g.vertex_properties['alleles_cluster']
    
    filtered = g.new_vertex_property("bool")
    g.vertex_properties['filtered'] = filtered

    live = g.new_vertex_property("bool")
    g.vertex_properties["live"] = live


    size = g.new_vertex_property("int")
    g.vertex_properties["size"] = size

    shape = g.new_vertex_property("int")
    g.vertex_properties["shape"] = shape

    fits_txt = g.new_vertex_property("string")
    g.vertex_properties["fits_txt"] = fits_txt
    
    deg = g.degree_property_map("in")     
    
#==============================================================================
#     for idx in range(g.num_vertices()):
#         v = g.vertex(idx)
#         if fitnesses[v] == 0.0:
#             live[v] = False ## inverse, for filtering purposes, sorry
#             size[v] = 0
#             fits_txt[v] = "0"
#             shape[v] = 1
#         else:
#             live[v] = True ## inverse, for filtering purposes, sorry
#             size[v] = 5
#             fits_txt[v] = "1"
#             shape[v] = 0        
#==============================================================================


    print "DRAWING"
    newpos = interactive_window(g, pos, 
               output_size=(1000, 1000), 
               vertex_color=[0,0,0,1],
               vertex_shape=shape,
               vertex_fill_color=fitnesses,
               #vertex_text=fits_txt,
               #vertex_fill_color=deg,
               bg_color=[1,1,1,1], 
               #vertex_pen_width=2,
               vertex_size=size, 
               edge_pen_width=0.1,
               #edge_color=[1,1,1,0.5],
               vcmap=matplotlib.cm.hot)
    print "DONE"
    
    if options.save:        
        g.vertex_properties["pos"] = newpos
        g.save(options.save, "gt")
    
interactive_figure()

