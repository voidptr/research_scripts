#!/bin/bash

####### ANALYZE Data 
####### Evolution of Modularity

####### I should be run from the root of the data directory.

PATH_TO_SCRIPTS="../../../scripts/"

do_work()
{
    echo "Processing $SUBGRP"
    echo "=========================================="


    ### Sanitize (gunzip everything)
    echo "Sanitize"
    echo "------------------------------------------"
    mkdir empty_data_directories

    for i in *_??????; 
        do echo $i ; 
        if [ -e $i/data/ ] ; 
        then 
            gunzip -r $i
        else 
            mv $i empty_data_directories
            echo "Data Directory Not Found - Moving to empty_data_directories" ; 
        fi ; 
    done

    ### Aggregate Fitness Timeseries
    echo "Aggregate Fitness"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_both fitness_timeseries c*_b*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glucose fitness_timeseries c*_glu*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glactose fitness_timeseries c*_gla*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward fitness_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish fitness_timeseries p*_??????/data/

    ### Aggregate Tasks Timeseries
    echo "Aggregate Tasks"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_both tasks_timeseries c*_b*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glucose tasks_timeseries c*_glu*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glactose tasks_timeseries c*_gla*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward tasks_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish tasks_timeseries p*_??????/data/


    ### Aggregate Functional Modularity
    echo "Aggregate Funct Mod"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_both -e 1001 functional_modularity_timeseries c*_b*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glucose -e 1001 functional_modularity_timeseries c*_glu*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glactose -e 1001 functional_modularity_timeseries c*_gla*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -e 1001 functional_modularity_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -e 1001 functional_modularity_timeseries p*_??????/data/

    ### Collapse Fitness
    echo "Collapse Fitness"
    echo "------------------------------------------"
    
    ## don't count the fitness value in the start of the treatment, or you will be sad.
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_both fitness_max --passoptions "--start_at 21" c*_b*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glucose fitness_max --passoptions "--start_at 21" c*_glu*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control_glactose fitness_max --passoptions "--start_at 21" c*_gla*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward fitness_max --passoptions "--start_at 21" n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish fitness_max --passoptions "--start_at 21" p*_??????/data/


    echo "DONE"
    echo ""
}


do_work
