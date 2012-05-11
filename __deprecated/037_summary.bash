echo "<h3>" > ../../evolution_of_modularity/analysis/037/summary//data.html
cat ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/README.txt >> ../../evolution_of_modularity/analysis/037/summary//data.html
echo "</h3>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
# generate graphs
#nopunish_orn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_nopunish_orn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_orn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_nopunish_orn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_orn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_nopunish_orn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_orn_??????/data/stats.dat.gz*

#punish_orn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_punish_orn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_orn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_punish_orn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_orn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_punish_orn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_orn_??????/data/stats.dat.gz*

#control_orn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_control_orn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_orn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_control_orn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_orn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_control_orn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_orn_??????/data/stats.dat.gz*

#nopunish_or
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_nopunish_or.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_or_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_nopunish_or.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_or_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_nopunish_or.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_or_??????/data/stats.dat.gz*

#punish_or
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_punish_or.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_or_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_punish_or.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_or_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_punish_or.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_or_??????/data/stats.dat.gz*

#control_or
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_control_or.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_or_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_control_or.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_or_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_control_or.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_or_??????/data/stats.dat.gz*

#nopunish_andn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_nopunish_andn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_andn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_nopunish_andn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_andn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_nopunish_andn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/nopunish_andn_??????/data/stats.dat.gz*

#punish_andn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_punish_andn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_andn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_punish_andn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_andn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_punish_andn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/punish_andn_??????/data/stats.dat.gz*

#control_andn
python "../generate graphs from raw data/"/single_column_graph.py -l -m ../../evolution_of_modularity/analysis/037/summary//fitness_control_andn.png Fitness 4 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_andn_??????/data/average.dat.gz*
python "../generate graphs from raw data/"/multi_column_graph.py ../../evolution_of_modularity/analysis/037/summary//tasks_control_andn.png Tasks "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_andn_??????/data/tasks.dat.gz*
python "../generate graphs from raw data/"/single_column_graph.py -m ../../evolution_of_modularity/analysis/037/summary//coalescentgenerations_control_andn.png "Coalescent Generations" 10 "x50 updates" ../../evolution_of_modularity/raw_data/037_Andn_Orn_Or__Opinion_Backbone/control_andn_??????/data/stats.dat.gz*

# stack figures
echo "<p>nopunish_orn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py nopunish_orn ../../evolution_of_modularity/analysis/037/summary//*_nopunish_orn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>punish_orn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py punish_orn ../../evolution_of_modularity/analysis/037/summary//*_punish_orn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>control_orn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py control_orn ../../evolution_of_modularity/analysis/037/summary//*_control_orn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>nopunish_or</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py nopunish_or ../../evolution_of_modularity/analysis/037/summary//*_nopunish_or.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>punish_or</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py punish_or ../../evolution_of_modularity/analysis/037/summary//*_punish_or.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>control_or</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py control_or ../../evolution_of_modularity/analysis/037/summary//*_control_or.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>nopunish_andn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py nopunish_andn ../../evolution_of_modularity/analysis/037/summary//*_nopunish_andn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>punish_andn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py punish_andn ../../evolution_of_modularity/analysis/037/summary//*_punish_andn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

echo "<p>control_andn</p>" >> ../../evolution_of_modularity/analysis/037/summary//data.html
python ./stack_figures.py control_andn ../../evolution_of_modularity/analysis/037/summary//*_control_andn.png >> ../../evolution_of_modularity/analysis/037/summary//data.html

