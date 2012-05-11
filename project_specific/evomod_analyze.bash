#!/bin/bash

####### ANALYZE Data 
####### Evolution of Modularity

####### I should be run from the root of the data directory.

PATH_TO_SCRIPTS="../../../../scripts/"

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

    ### Collect Mutation Information (within the individual runs)
    echo "Collect Mutations"
    echo "------------------------------------------"

    for i in *_??????; 
        do echo $i ; 
        if [ -e $i/data/ ] ; 
        then 
            cd $i/data ; 
            #rm mutation_metrics.csv ; 
            #python ../../$PATH_TO_SCRIPTS/analysis/mutations/calculate_mutation_metrics.py 5 6 8 lineage.dat ./phenotype/ > mutation_metrics.csv ; 
            cd ../../ ; 
        else 
            echo "Data Directory Not Found" ; 
        fi ; 
    done

    ### Aggregate Fitness Timeseries
    echo "Aggregate Fitness"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" fitness_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" fitness_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" fitness_timeseries p*_??????/data/

    ### Aggregate Functional Modularity
    echo "Aggregate Funct Mod"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" -e 4001 functional_modularity_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" -e 4001 functional_modularity_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" -e 4001 functional_modularity_timeseries p*_??????/data/

    ### Aggregate Mutation Timeseries
    echo "Aggregate Mutations"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" coding_mutations_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" coding_mutations_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" coding_mutations_timeseries p*_??????/data/

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" noncoding_mutations_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" noncoding_mutations_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" noncoding_mutations_timeseries p*_??????/data/

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" degenerate_mutations_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" degenerate_mutations_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" degenerate_mutations_timeseries p*_??????/data/

    ### Aggregate Genome Ct Change Timeseries
    echo "Aggregate Genome Ct Change"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" genome_change_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" genome_change_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" genome_change_timeseries p*_??????/data/

    ### Aggregate Genome Count Timeseries
    echo "Aggregate Genome Count"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" genotype_count_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" genotype_count_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" genotype_count_timeseries p*_??????/data/

    ### Aggregate Genotypic Entropy Timeseries
    echo "Aggregate Genotypic Entropy<D-c>"
    echo "------------------------------------------"

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" genotypic_entropy_timeseries c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" genotypic_entropy_timeseries n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" genotypic_entropy_timeseries p*_??????/data/



    ### Collapse Fitness
    echo "Collapse Fitness"
    echo "------------------------------------------"
    
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" fitness_max c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" fitness_max n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" fitness_max p*_??????/data/

    ### Collapse Mutations
    echo "Collapse Mutations"
    echo "------------------------------------------"
    
    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" coding_mutations_average c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" coding_mutations_average n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" coding_mutations_average p*_??????/data/

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" noncoding_mutations_average c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" noncoding_mutations_average n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" noncoding_mutations_average p*_??????/data/

    $PATH_TO_SCRIPTS/analysis/analyze.py -g control -s "$SUBGRP" degenerate_mutations_average c*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g noreward -s "$SUBGRP" degenerate_mutations_average n*_??????/data/
    $PATH_TO_SCRIPTS/analysis/analyze.py -g punish -s "$SUBGRP" degenerate_mutations_average p*_??????/data/


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
