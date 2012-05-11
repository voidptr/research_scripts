## only run me from the root of the data directory (which I assume is under raw_data)

for i in `ls -d noreward_and_or_??????`; do echo $i; cd $i/; pwd; 

../../../avida_executable_environments/mac/2.13.0/work__clean_template/avida -a -set ANALYZE_FILE ../../../../avida_python_scripts/avida_analyze_mode_scripts/output_lineages_and_map_tasks.analyze.cfg -set EVENT_FILE events_control.cfg -set ENVIRONMENT_FILE environment_AND_bb_OR_fluct.cfg

cd ../; done
