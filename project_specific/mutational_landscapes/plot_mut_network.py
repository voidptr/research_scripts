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


parser.add_option("--filter_dead", action = "store_true", dest = "filter_dead",
                  default = False, help = "hide dead organisms")
parser.add_option("--logfit", action = "store_true", dest = "logfit",
                  default = True, help = "colors are log fitness not raw")


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

    live = g.new_vertex_property("bool")
    g.vertex_properties["live"] = live


    size = g.new_vertex_property("int")
    g.vertex_properties["size"] = size

    shape = g.new_vertex_property("int")
    g.vertex_properties["shape"] = shape

    fits_txt = g.new_vertex_property("string")
    g.vertex_properties["fits_txt"] = fits_txt

    deg = g.degree_property_map("in")

    logfit = g.new_vertex_property("float")
    #deg.a = 2 * (math.sqrt(deg.a) * 0.5 + 0.4)


    for idx in range(g.num_vertices()):
        v = g.vertex(idx)
        if fitnesses[v] == 0.0:
            logfit[v] = 0
            live[v] = False ## inverse, for filtering purposes, sorry
            size[v] = 0
            fits_txt[v] = "0"
            shape[v] = 1
        else:
            logfit[v] = math.log(fitnesses[v] + 1)
            live[v] = True ## inverse, for filtering purposes, sorry
            size[v] = 5
            fits_txt[v] = "1"
            shape[v] = 0

    if options.filter_dead:
        g.set_vertex_filter(live)

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

    fitcol = fitnesses
    if options.logfit:
        fitcol = logfit

    graph_draw(g, pos,
               output_size=(1000, 1000),
               vertex_color=[0,0,0,1],
               vertex_shape=shape,
               vertex_fill_color=fitcol,
               #vertex_text=fits_txt,
               #vertex_fill_color=deg,
               bg_color=[1,1,1,1],
               #vertex_pen_width=2,
               vertex_size=size,
               edge_pen_width=0.1,
               #edge_color=[1,1,1,0.5],
               vcmap=matplotlib.cm.hot,
    output=outfile)
    print "DONE"

generate_figure()
