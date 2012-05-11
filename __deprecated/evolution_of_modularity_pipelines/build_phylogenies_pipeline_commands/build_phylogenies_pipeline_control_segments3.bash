## only run me from the root of the data directory (which I assume is under raw_data)

for i in `ls -d *control_*3?`; do echo $i; cd $i/data/; pwd; python2.6 ../../../../../scripts/evolution_of_modularity_pipelines/build_phylogeny.py ../../phylogeny_$i.png ../../../../../scripts/evolution_of_modularity_pipelines/draw_map_task.py analyze/lineage-???.dat* analyze/lineage-????.dat* analyze/lineage-?????.dat* analyze/lineage-??????.dat* ;cd ../../; done
