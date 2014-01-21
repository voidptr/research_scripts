#!/bin/bash

EXTRACT_LINE_ON_CONDITION="../scripts/extract_line_on_condition.py"
CALCULATE_PHYSICAL_MODULARITY="../scripts/calculate_physical_modularity.py"
EXTRACT_SINGLE_COLUMN_TO_CSV="../scripts/extract_single_column_to_csv.py"
CONVERT_TO_ORGANISMS__SINGLE_FILE="../../scripts/convert_to_organisms__single_file.py"
#############
## There are a series of stages and actions. The levels go as follows:
## START (STAGE 0)
## A.1 -> individual genotypes in a single file in a single time point; updates/50 files per run, unknown number of lines per file (one line per genotype)
## T.1 -> single task count file per run.
## STAGE 1 -- SEPARATE TWO-TASK ONLY
## A.1b -> two-task genotypes only from A.1 -- same format as A.1; updates/50 files per run, ?? lines per file (one line per two-task-performing genotype)
## STAGE 1.5 -- CONVERT TO ORGANISM COUNT FROM GENOTYPE COUNT
## A.1c -> two-task ORGANISMS from A.1b -- same format as A.1b; updates/50 files per run, ?? lines per file (one organism per line)
## STAGE 2 -- PHYSICAL MODULARITY
## A.2 -> calculate physical modularity measures from A.1b (extends A.1b) ; updates/50 files per run, ?? lines per file (should be the same # of lines as A1.c)
## STAGE 3 -- PHYSICAL MODULARITY
## B.1 -> took entire column 2 (fluctuating task unity) of every A.2, calculated mean, median, std, etc. FILES A.2 (col 2) -> FILE B.1  (FILE A.2 (col 2) -> line (of stats) in FILE B.1); One file per run, updates/50 lines per file
## B.2 -> took entire column 1 (backbone task unity) of every A.2, calculated mean, median, std, etc. FILES A.2 (col 1) -> FILE B.2  (FILE A.2 (col 1) -> line (of stats) in FILE B.2); One file per run, updates/50 lines per file
## B.3 -> took entire column 5 (fluctuating task scatter) of every A.2, calculated mean, median, std, etc. FILES A.2 (col 5) -> FILE B.3  (FILE A.2 (col 5) -> line (of stats) in FILE B.3); One file per run, updates/50 lines per file
## B.4 -> took entire column 4 (backbone task scatter) of every A.2, calculated mean, median, std, etc. FILES A.2 (col 4) -> FILE B.4  (FILE A.2 (col 4) -> line (of stats) in FILE B.4); One file per run, updates/50 lines per file
## etc...

if [ ! -e "data" ]
then
    echo "Data directory is missing"
    exit 1
fi

cd data/;

######## STAGE 1 #########
##Pull out only the genomes that do both tasks from the individual modularity files 
echo "Stage 1 -- pull out twotask genomes"
mkdir two_task_only_individual_modularity
python $EXTRACT_LINE_ON_CONDITION 2 '>1' two_task_only_individual_modularity/two_task_only__ individual_modularity-*.dat*

######## STAGE 1.5 ########
## convert to organisms
echo "Stage 1.5 -- convert those genomes into organisms"
mkdir two_task_only_individual_modularity__organisms
cd two_task_only_individual_modularity
for i in two_task_only__*
do
    echo $i
    python $CONVERT_TO_ORGANISMS__SINGLE_FILE 18 $i > ../two_task_only_individual_modularity__organisms/organisms__$i 
done
cd ../

######## STAGE 2 #########
## Generate the Physical Modularity Measure File (one for each sample in a run, a jillion files)
## Generates stats for both scatter (Ratio of Optimal STD) and unity (Ct/Length)

echo "Stage 2 - generate the physical modularity stats"
#pwd
mkdir physical_modularity_stats__organisms
cd two_task_only_individual_modularity__organisms/
#pwd
for j in organisms__two_task_only__*.dat*
do     
#    pwd
    echo $j
    cd ../
#    pwd
    python $CALCULATE_PHYSICAL_MODULARITY 11 12 16 17 9 10 19 20 two_task_only_individual_modularity__organisms/$j > physical_modularity_stats__organisms/task_physical_modularity__$j
    cd two_task_only_individual_modularity__organisms/ 
#    pwd
done
cd ../

########### STAGE 3 #########
##generate the stats for the physical modularity measures, and aggregate into a single file for a run
echo "Stage 3 -- collect the physical modularity averages"
#pwd
############# BACKBONE TASK #############
## unity - backbone task
echo "Backbone - unity"
rm backbone_task_unity__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 1 >> backbone_task_unity__two_task_physical_modularity__stats__organisms.csv; 

## scatter - backbone task
echo "Backbone - scatter"
rm backbone_task_scatter__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 4  >> backbone_task_scatter__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - mean - backbone task
echo "Backbone - gapmean"
rm backbone_task_gapmean__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 7  >> backbone_task_gapmean__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - median - backbone task
echo "Backbone - gapmedian"
rm backbone_task_gapmedian__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 8  >> backbone_task_gapmedian__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - variance - backbone task
echo "Backbone - gapvar"
rm backbone_task_gapvar__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 9  >> backbone_task_gapvar__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - std - backbone task
echo "Backbone - gapstd"
rm backbone_task_gapstd__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 10  >> backbone_task_gapstd__two_task_physical_modularity__stats__organisms.csv; 

########## FLUCTUATING TASK ##########
## unity - fluctuating task
echo "Fluct - unity"
rm fluct_task_unity__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 2  >> fluct_task_unity__two_task_physical_modularity__stats__organisms.csv; 

## scatter - fluctuating task
echo "Fluct - scatter"
rm fluct_task_scatter__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 5  >> fluct_task_scatter__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - mean - fluctuating task
echo "Fluct - gapmean"
rm fluct_task_gapmean__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 11  >> fluct_task_gapmean__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - median - fluctuating task
echo "Fluct - gapmedian"
rm fluct_task_gapmedian__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 12  >> fluct_task_gapmedian__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - variance - fluctuating task
echo "Fluct - gapvar"
rm fluct_task_gapvar__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 13  >> fluct_task_gapvar__two_task_physical_modularity__stats__organisms.csv; 

## gap stats - std - fluctuating task
echo "Fluct - gapstd"
rm fluct_task_gapstd__two_task_physical_modularity__stats__organisms.csv ; ls physical_modularity_stats__organisms/task_physical*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s "," -c 14  >> fluct_task_gapstd__two_task_physical_modularity__stats__organisms.csv; 


################### STAGE 4
# Collect the functional modularity stats into averages
echo "Stage 4 - collect the funct mod stats into averages"
echo "Functional Modularity"
rm two_task_functional_modularity__stats__organisms.csv ; ls two_task_only_individual_modularity__organisms/*two_task*-*.dat* | sort -n -t "-" -k 2 | xargs python "$EXTRACT_SINGLE_COLUMN_TO_CSV" -s " " -c 8 >> two_task_functional_modularity__stats__organisms.csv; 

