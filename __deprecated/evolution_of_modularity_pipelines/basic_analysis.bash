## perform the basic analysis
## $1 is the directory name

## test for the presence of the parameter
if [ -z $2 ]
then
    echo "usage: $0 raw_data_directory analysis_output_directory"
    exit
fi

## run the commands


## 1. Perform the rest of the analysis

mkdir $2/median_amplitudes
python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_stats_by_sample_and_task.py 30000 100000 1000 $1/\$1_??????/data/tasks.dat.gz* > $2/median_amplitudes/\$1.txt" $2/*__dynamic_runlist.txt

mkdir $2/means_and_mann_whitney_u
python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_differences_in_mean_and_mann_whitney_u_test.py $2/median_amplitudes/\$1.txt $2/median_amplitudes/\$2.txt > $2/means_and_mann_whitney_u/\$1_\$2.txt" $2/*_comparisons_dynamic_runlist.txt 

python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__plot_differences_in_means.py $2/summary/differences_in_means_\$1_\$2.png $2/means_and_mann_whitney_u/\$1_\$2.txt" $2/*_comparisons_dynamic_runlist.txt 

#mkdir $2/long_tail
#python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_stats_by_sample_and_task.py 100000 105000 5000 $1/\$1_??????/data/tasks.dat.gz* > $2/long_tail/\$1.txt" $2/*__dynamic_runlist.txt 

mkdir $2/raw_long_tail
python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_raw_amplitudes_by_sample_and_task.py 100000 110000 200 $1/\$1_??????/data/tasks.dat.gz* > $2/raw_long_tail/\$1.txt" $2/*__dynamic_runlist.txt

python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../evolution_of_modularity_pipelines/longtail.py $2/summary/longtail_\$1_\$2.png $2/raw_long_tail/\$1.txt $2/raw_long_tail/\$2.txt " $2/*_comparisons_dynamic_runlist.txt


#python ../analyze\ task\ oscillations\ pipeline/task_oscillation__collect_all_data_and_plot_3d_chart__bar3d.py $2/graphs/collective_bar $2/*__task_name_translation_file.txt $2/means_and_mann_whitney_u/*.txt

## 2. Generate and run the summary generation script
mkdir $2/summary
python ../generate\ summary\ files/generate_summary_bash_script.py $1 $2/summary/ "../generate graphs from raw data/" > ./summary.bash
cat ./summary.bash
bash ./summary.bash 
rm ./summary.bash

