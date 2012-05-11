## extract only the raw amplitudes
## $1 is the directory name

## test for the presence of the parameter
if [ -z $2 ]
then
    echo "usage: $0 raw_data_directory analysis_output_directory"
    exit
fi

## run the commands

mkdir $2/raw_amplitudes
python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_raw_amplitudes_by_sample_and_task.py 30000 100000 1000 $1/\$1_??????/data/tasks.dat.gz* > $2/raw_amplitudes/\$1.txt" $2/*__dynamic_runlist.txt


