#!/usr/bin/python

# Split a graph into disconnected graphs

# Written in Python 2.7
# RCK
# 3-24-11


from graph_tool.all import *
from optparse import OptionParser
import matplotlib
import random
import math

# Set up options
usage = """usage: %prog [options] <network.xml> <out_prefix>

script must be run from the same directory as Avida."""
parser = OptionParser(usage)
parser.add_option("-v", "--verbose", action = "store_true", dest = "verbose",
                  default = False, help = "print extra messages to stdout")

parser.add_option("--debug_messages", action = "store_true", dest = "debug_messages",
                  default = False, help = "print debug messages to stdout")

## fetch the args
(options, args) = parser.parse_args()

networkfile = args[0]
outfile_prefix = args[1]

## parameter errors
if len(args) < 2:
    parser.error("incorrect number of arguments")

g = load_graph(networkfile, "gt")
print "LOADED"
print g




class VisitorExample(BFSVisitor):

    def __init__(self, filt, hit, filt_ct, hit_ct):
        self.filt_ct = filt_ct
        self.filt = filt
        self.hit_ct = hit_ct
        self.hit = hit
        return None
        #self.filt = filt

    def discover_vertex(self, u):
        #print("-->", self.filt[u], "has been discovered!")
        self.filt[u] = True
        self.hit[u] = True
        self.hit_ct += 1
        self.filt_ct += 1
        #print u

#     def examine_vertex(self, u):
#         return None
# #        print(self.name[u], "has been examined...")
#
#     def tree_edge(self, e):
#         return None
# #        self.pred[e.target()] = int(e.source())
# #        self.dist[e.target()] = self.dist[e.source()] + 1

def split_graph():

    idx = 0
    graph_ct = 0
    vct = g.num_vertices()

    hit = g.new_vertex_property("bool", val=False)
    hit_ct = 0
    filt = g.new_vertex_property("bool", val=False)
    filt_ct = 0

    while (idx < vct):

        start = idx
        print
        print "starting at ", idx
        for idx in range(start, vct):

            if hit[g.vertex(idx)] == False:
                print " ...found ", idx
                break

        if hit[g.vertex(idx)] == True:
            ## if we hit the end of the for loop and seen it all
            break

        filt = g.new_vertex_property("bool", val=False)
        filt_ct = 0
        bleh = VisitorExample(filt, hit, filt_ct, hit_ct)
        bfs_search(g, g.vertex(idx), bleh)

        filt_ct = bleh.filt_ct
        hit_ct = bleh.hit_ct
        filt = bleh.filt
        hit = bleh.hit

        print "Partition ", graph_ct, " started at ", idx
        print "Hit So Far: ", hit_ct, " out of ", vct
        print "Current Filter Ct: ", filt_ct
        #g.set_vertex_filter(filt)
        sub = GraphView(g, filt)
        sub = Graph(sub, prune=True)
        print sub
        #print g
        sub.save(outfile_prefix+".partition_"+str(graph_ct)+".xml", "gt")

        idx += 1
        graph_ct += 1


split_graph()
