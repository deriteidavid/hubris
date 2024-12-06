#!/bin/bash

python process_SAINTExpress_output_excels.py 
python RNASeq_based_filtering_hg38.py
python create_HUBRIS.py
python generate_HHIP_ego_networks.py union 1 1
python generate_HHIP_ego_networks.py union 0 1
python shorthest_path_analysis.py 16HBE 1 1 
python shorthest_path_analysis.py IMR90 1 1 
python merged_shorthest_path_graph.py
python shorthest_path_analysis.py IMR90 0 1 
python shorthest_path_analysis.py 16HBE 0 1
python generate_HHIP_ego_networks.py union 0 1
python generate_enrichment_gene_sets.py 1
python functional_enrichment_new_paths.py
python new_paths_graph.py
python functional_enrichment_new_interactors.py
python functional_enrichment_induced_graph.py
python highlighted_pathway_stats.py

