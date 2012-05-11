## run analyze mode
## $1 is the directory name

## test for the presence of the parameter
if [ -z $2 ]
then
    echo "usage: $0 raw_data_directory analysis_output_directory"
    exit
fi

## run the commands

python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "cd $1/\$1\$2; gunzip *; gunzip data/*; ../config/avida.macosx -a -set ENVIRONMENT_FILE environment_andn.cfg -set EVENTS_FILE events_\$1.cfg -set ANALYZE_FILE ../../../../avida_python_scripts/avida_analyze_mode_scripts/map_task_switching_env.analyze.cfg; python ../python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_raw_amplitudes_by_sample_and_task.py 100000 110000 200 $1/\$1_??????/data/tasks.dat.gz* > $2//\$1.txt" $2/*__dynamic_runlist.txt

mkdir $2/
python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_raw_amplitudes_by_sample_and_task.py 100000 110000 200 $1/\$1_??????/data/tasks.dat.gz* > $2/raw_long_tail/\$1.txt" $2/*__dynamic_runlist.txt

python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../evolution_of_modularity_pipelines/longtail.py $2/summary/longtail_\$1_\$2.png $2/raw_long_tail/\$1.txt $2/raw_long_tail/\$2.txt " $2/*_comparisons_dynamic_runlist.txt

#mkdir $2/long_tail
#python ../common\ modules\ and\ helper\ scripts/run_combinatoric_scripts.py "python ../analyze\ task\ oscillations\ pipeline/task_oscillation__output_stats_by_sample_and_task.py 100000 105000 5000 $1/\$1_??????/data/tasks.dat.gz* > $2/long_tail/\$1.txt" $2/*__dynamic_runlist.txt 
