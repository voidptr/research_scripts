#!/usr/bin/python

# Extract single column to csv, and possibly perform some operations to it.

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

parser.add_option("--sample", dest = "sample", type="float",
                  default = None, help = "sample down the loaded network graph to a fraction.")

parser.add_option("--save", dest = "save", type="string",
                  default = None, help = "Output the graph, including the position.")
parser.add_option("--redopos", action = "store_true", dest = "redopos",
                  default = False, help = "re-generate positions.")


## fetch the args
(options, args) = parser.parse_args()

networkfile = args[0]
outfile = args[1]

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

 
def generate_figure():
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
    
    deg = g.degree_property_map("in")
    #deg.a = 2 * (math.sqrt(deg.a) * 0.5 + 0.4)
    
        
    if options.sample:
        for idx in range(g.num_vertices()):
            filtered[g.vertex(idx)] = True
        
        sample = random.sample(range(g.num_vertices()), int(g.num_vertices() * (1-options.sample)))
        for idx in sample:
            filtered[g.vertex(idx)] = False  
        
        sub = GraphView(g, filtered)

        for v in sub.vertices():            
            ct = 0
            for edge in v.all_edges():
                ct += 1
                break;
                
            if ct == 0:            
                filtered[v] = False

        g.set_vertex_filter(filtered)         
        print g
        
        
    #fitnesses_down = [ fitnesses[v][0] for v in g.vertices() ]  
    #steps_down = [ steps[v][0] for v in g.vertices() ] 
#    for v in g.vertices():
#        print fitnesses[v]
        
    print "BEGINNING"
    if options.redopos or not pos:
        pos = sfdp_layout(g, 
                          #groups=alleles_cluster, 
                          epsilon=0.001, max_level=50, 
                          verbose=True)
        
    if pos and options.redopos:
        pos = sfdp_layout(g, pos=pos, epsilon=0.001, max_level=10, verbose=True)
        #pos = fruchterman_reingold_layout(g, pos=pos, verbose=True)

    if options.save:        
        g.vertex_properties["pos"] = pos
        g.save(options.save, "gt")

    print "DRAWING"
    graph_draw(g, pos, 
               output_size=(1000, 1000), 
               vertex_color=[0,0,0,1],
               vertex_fill_color=fitnesses,
               #vertex_fill_color=deg,
               bg_color=[1,1,1,1],
               vertex_size=2, edge_pen_width=0.1,
               #edge_color=[1,1,1,0.5],
               vcmap=matplotlib.cm.hot, 
    output=outfile)
    print "DONE"
    
generate_figure()

