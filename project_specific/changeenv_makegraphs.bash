#!/bin/bash

####### ANALYZE Data 
####### Evolution of Modularity

####### I should be run from the root of the data directory.

PATH_TO_SCRIPTS="../../../scripts/"

do_work()
{
    echo "Graphs"
    echo "------------------------------------------"

#    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py tasks_timeseries
#    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py fitness_timeseries
    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py fitness_max

    echo "DONE"
    echo ""
}


do_work
