## this builds the phylogenies
## run this from the root of the data directory.

## screens!!
screen -d -m -S c_0_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_control_segments0.bash
screen -d -m -S c_1_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_control_segments1.bash
screen -d -m -S c_2_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_control_segments2.bash
screen -d -m -S c_3_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_control_segments3.bash

screen -d -m -S n_0_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_noreward_segments0.bash
screen -d -m -S n_1_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_noreward_segments1.bash
screen -d -m -S n_2_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_noreward_segments2.bash
screen -d -m -S n_3_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_noreward_segments3.bash

screen -d -m -S p_0_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_punish_segments0.bash
screen -d -m -S p_1_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_punish_segments1.bash
screen -d -m -S p_2_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_punish_segments2.bash
screen -d -m -S p_3_phylogeny -s ../../../scripts/evolution_of_modularity_pipelines/build_phylogenies_pipeline_commands/build_phylogenies_pipeline_punish_segments3.bash
