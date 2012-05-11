#!/bin/bash

####### ANALYZE Data 
####### Evolution of Modularity

####### I should be run from the root of the data directory.

PATH_TO_SCRIPTS="../../../../scripts/"

do_work()
{
    echo "Processing $SUBGRP"
    echo "=========================================="

    echo "Graphs"
    echo "------------------------------------------"

#    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" tasks_timeseries
#    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" fitness_timeseries

    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" genome_change_timeseries
    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" genotypic_entropy_timeseries
    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" genotype_count_timeseries


#    $PATH_TO_SCRIPTS/graph_generation/makegraphs.py -s "$SUBGRP" fitness_max

    echo "DONE"
    echo ""
}


cd SEPARATED
SUBGRP="separated"
do_work
cd ../

cd INTERTWINED
SUBGRP="intertwined"
do_work
cd ../
