## this builds the phylogenies - only the phylogenies, not the individual map tasks
## run this from the root of the data directory.

for i in `ls -d *_??????`; do echo $i; cd $i/data/; pwd; python2.6 ../../../../../scripts/evolution_of_modularity_pipelines/build_phylogeny.py -p ../../phylogeny_$i.png ../../../../../scripts/evolution_of_modularity_pipelines/draw_map_task.py lineage_???.dat lineage_????.dat lineage_?????.dat ;cd ../../; done;


