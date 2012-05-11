## this extracts the lineages and maps the tasks using avida analyze mode.
## run this from the root of the data directory.

## screens!
#screen -d -m -S c_0_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_control_segments0.bash
#screen -d -m -S c_1_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_control_segments1.bash
#screen -d -m -S c_2_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_control_segments2.bash
#screen -d -m -S c_3_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_control_segments3.bash

screen -d -m -S n_0_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_noreward_segments0.bash
screen -d -m -S n_1_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_noreward_segments1.bash
screen -d -m -S n_2_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_noreward_segments2.bash
screen -d -m -S n_3_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_noreward_segments3.bash

screen -d -m -S p_0_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_punish_segments0.bash
screen -d -m -S p_1_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_punish_segments1.bash
screen -d -m -S p_2_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_punish_segments2.bash
screen -d -m -S p_3_analyze -s ../../../avida_python_scripts/evolution_of_modularity_pipelines/extract_lineages_and_map_tasks_pipeline_commands/analyze_pipeline_punish_segments3.bash

