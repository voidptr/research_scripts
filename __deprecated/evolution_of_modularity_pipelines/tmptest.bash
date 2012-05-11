## test for the presence of the parameter
if [ -z $2 ]
then
    echo "usage: $0 raw_data_directory analysis_output_directory"
    exit
fi

#${RAWDATA}=$1
#${ANALYSIS}=$2

## run the commands

#cat ${ANALYSIS}/__dynamic_runlist.txt | bash { "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_stats_by_sample_and_task.py 30000 100000 1000 ${RAWDATA}/\$1_??????/data/tasks.dat.gz* > ${ANALYSIS}/median_amplitudes/\$1.txt" }

python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_stats_by_sample_and_task.py 30000 100000 1000 $1/\$1_??????/data/tasks.dat.gz* > $2/median_amplitudes/\$1.txt" $2/*__dynamic_runlist.txt

