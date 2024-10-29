This repository contains code and data for the manuscript entitled: 
# HHIP protein interactions in lung cells provide insight into COPD pathogenesis

Available on BioRxiv: 
https://www.biorxiv.org/content/10.1101/2024.04.01.586839v1  

## Abstract 
Chronic obstructive pulmonary disease (COPD) is the third leading cause of death worldwide. The primary causes of COPD are environmental, including cigarette smoking; however, genetic susceptibility also contributes to COPD risk. Genome-Wide Association Studies (GWASes) have revealed more than 80 genetic loci associated with COPD, leading to the identification of multiple COPD GWAS genes. However, the biological relationships between the identified COPD susceptibility genes are largely unknown. Genes associated with a complex disease are often in close network proximity, i.e. their protein products often interact directly with each other and/or similar proteins. In this study, we use affinity purification mass spectrometry (AP-MS) to identify protein interactions with HHIP, a well-established COPD GWAS gene which is part of the sonic hedgehog pathway, in two disease-relevant lung cell lines (IMR90 and 16HBE). To better understand the network neighborhood of HHIP, its proximity to the protein products of other COPD GWAS genes, and its functional role in COPD pathogenesis, we create HUBRIS, a protein-protein interaction network compiled from 8 publicly available databases. We identified both common and cell type-specific protein-protein interactors of HHIP. We find that our newly identified interactions shorten the network distance between HHIP and the protein products of several COPD GWAS genes, including DSP, MFAP2, TET2, and FBLN5. These new shorter paths include proteins that are encoded by genes involved in extracellular matrix and tissue organization. We found and validated interactions to proteins that provide new insights into COPD pathobiology, including CAVIN1 (IMR90) and TP53 (16HBE). The newly discovered HHIP interactions with CAVIN1 and TP53 implicate HHIP in response to oxidative stress.

# Running all scripts

To run the Python scripts reproducing the network analysis results published in the paper run the bash script: 

__run_all_scirpts_in_sequence.sh__

# Running scripts individually 
The documentation of the code is in progress, please contact the authors if you have any questions at david.deritei@channing.harvard.edu

This section documents the individual scripts needed to create the HUBRIS networks, the different cell-type-specific versions, and the related analyses. 

1. __process\_SAINTExpress\_output\_excels.py__ <br>
    * __Aim__: Process the output files of the SAINTExpress analysis (HHIP\_SAINTexpress\_consolidated.xlsx), which consolidates the raw AP-MS interaction data into statistically significant interactions. The goal is to have a simplified list of interactions for the different cases (celly type, CRAPome etc.), which also constitutes the input for later network analysis scripts.
    * __Input files__: HHIP\_SAINTexpress\_consolidated.xlsx <br>
    * __Std output__: list of statistically significant interactions on the standard output for all cases (cell type, CRAPome (yes/no)) <br>
    * __Output Files__: all_significant_links_HHIP.xlsx; Supplementary_Table_S1_all_significant_links_HHIP.xlsx <br> 

2. __RNASeq\_based\_filtering.py__ 
    * __Aim__: Determine which genes are expressed in the two cell lines (IMR90, 16HBE) based on RNA-Seq data.
    * __Input files__: rnaseq\_PPI\_GWAS/imr90/gene\_count.xlsx;  rnaseq\_PPI\_GWAS/imr90/gene\_fpkm\_group.xlsx;  rnaseq\_PPI\_GWAS/16hbe/gene\_count.xlsx; rnaseq\_PPI\_GWAS/16hbe/gene\_fpkm\_group.xlsx
    * __Key parameter(s)__: expression_threshold (default = 0.25)
    * __Std output__: -
    * __Output Files__:IMR90_RNASeq_genes_expressed.csv; 16HBE_RNASeq_genes_expressed.csv; <br>
    Figures: CR_outputs/RNASeq_IMR90.png; CR_outputs/RNASeq_16HBE.png (__Figure S12__)


3. __create\_HUBRIS.py__
    * __Aim__: Generate the HUBRIS network by either re-downloading the constituent databases or using existing downloads. This script also does the conversion between ID-s (using biorosetta and a mapping table referenced below) and the merging of the networks
    * __Input files__: - databases.xlsx (config file of the databases, it may require an update if the databases a re-downloaded); <br>
                       - hgnc_mapping.tsv (id mapping from  https://www.genenames.org/download/statistics-and-files/). <br>
                       -(optional) db_local_files/* - database local files, file names configured in databases.xlsx
    * __Key parameter(s)__: - re_download (default = False): should the databases be re-downloaded? If False the ones specified in the database config excel will be used. <br> 
                      - to_download (default = ['HumanNet','HIPPIE','BioGrid','NCBI','StringDB','Interactome3D','HURI','Reactome']): which databases should be downloaded (if re_download == True)<br>
                      - to_merge (default = to_download): which databases should be merged into the HUBRIS network? <br>
                      - consensus_id_type (default = 'entr'): he consensus id type to which all dbs (which are not already in it) will be converted before merging <br>
                      - db_count_threshold (default=2) minimum number of databases containing an edge for the edge to be kept in the final HUBRIS network
    * __Std output__: progress report; network statistics
    * __Output Files__: G_merged_raw.gpickle; G_hubris.gpickle <br>
                        Figures: CR_outputs/HUBRIS_db_analytics.png (__Figure S11__ )



4. __generate\_HHIP\_ego\_networks.py__
    * __Aim__: Generate different variations of the "ego" network of HHIP based on HUBRIS and our newly identified edges. The script also determines whether the newly identified edges create new shorter paths between HHIP and the other GWAS genes. <br>
    * __Input files__: - G_hubris.gpickle <br>
                       - all_significant_links_HHIP.xlsx <br>
                       - (optional) RNASeq_lists/*cell_line*_RNASeq_genes_expressed.csv
    * __Key parameter(s)__: - cell_line (str, options:'intersection', 'union', 'IMR90', '16HBE'): which cell line's data to use (interactions and RNA-Seq)<br>
                            - filter_crapome (bool, options: True= SAINTExpress interactions with CRAPome priors; False= without CRAPOME priors) <br>
                            - filter_networks_based_on_expression (bool, options: True = filter the network based on RNA-Seq expression; False = no filtering)
    * __Std output__: progress report; network statistics
    * __Output Files__: CR_outputs/G_ego_HUBRIS_only_cell_type_%s_expression_%s.graphml %(cell_line,str(int(filter_networks_based_on_expression)))) (the figure for the HUBRIS-only ego network of HHIP) <br>
                        CR_outputs/G_ego_plot_cell_type_%s_crapome_%s_expression_%s.graphml'%(cell_line,str(int(filter_crapome)),str(int(filter_networks_based_on_expression)))) (HUBRIS + new interactions) <br>  
    * __Specific use-cases:__ The parameters __cell_line__, __filter_crapome__ and __filter_networks_based_on_expression__ and be specified as command line arguments (in this order), this way it's easier to generate the different use cases we disscus below: <br>
                   - __python generate_HHIP_ego_networks.py union 1 1__ --> G_ego_HUBRIS_only_cell_type_union_expression_1.graphml (__Figure 1__) <br>
                                                                        --> G_ego_HUBRIS_only_cell_type_union_expression_1.graphml (__Figure 3__) <br>
                   - __python generate_HHIP_ego_networks.py union 0 1__ --> G_ego_plot_cell_type_union_crapome_0_expression_1.graphml (__Figure S2__) <br>
   
5. __shorthest\_path\_analysis.py__
    * __Aim__: Find shortest paths in the different variations of the HUBRIS networks (cell type-specific, with and without new experimental edges) between HHIP and a set of other COPD GWAS gene products.
    * __Input files__: - G_hubris.gpickle <br>
                       - all_significant_links_HHIP.xlsx <br>
                       - (optional) RNASeq_lists/*cell_line*_RNASeq_genes_expressed.csv
    * __Key parameter(s)__: - cell_line (str, options:'intersection', 'union', 'IMR90', '16HBE'): which cell line's data to use (interactions and RNA-Seq)<br>
                            - filter_crapome (bool, options: True= SAINTExpress interactions with CRAPome priors; False= without CRAPOME priors) <br>
                            - filter_networks_based_on_expression (bool, options: True = filter the network based on RNA-Seq expression; False = no filtering)<br>
                            - copd_gwas_genes (list, default = ['FAM13A','IREB2','DSP','AGER','MFAP2','FBLN5','NPNT','FBXO38','SFTPD','TET2','TGFB2','MMP12','MMP1']<br>
    * __Std output__: progress report; network statistics
    * __Output Files__:'CR_outputs/hubris_sps_cell_type_%s_crapome_%s_expression_%s.pdf'%(cell_line,str(int(filter_crapome)),str(int(filter_networks_based_on_expression)))  (shortest path comparisons with and without the new edges)<br>
                       'CR_outputs/G_hubris_seleted_sp_cell_type_%s_crapome_%s_expression_%s.graphml'%(cell_line,str(int(filter_crapome)),str(int(filter_networks_based_on_expression))) (graph of specific shortest paths) <br>
    * __Specific use-cases:__ The parameters __cell_line__, __filter_crapome__ and __filter_networks_based_on_expression__ and be specified as command line arguments (in this order), this way it's easier to generate the different use cases we disscus below: <br>
                   - __python shorthest_path_analysis.py IMR90 1 1__ --> hubris_sps_cell_type_IMR90_crapome_1_expression_1.png (.pdf) (__Figure S3 top__) <br>
                   - __python shorthest\_path\_analysis.py 16HBE 1 1__ --> hubris_sps_cell_type_16HBE_crapome_1_expression_1.png (.pdf) (__Figure S3 bottom__) <br>
                   - __python shorthest_path_analysis.py IMR90 0 1__ --> G_hubris_seleted_sp_cell_type_IMR90_crapome_0_expression_1.graphml (__Figure S4__) <br>
                   - __python shorthest_path_analysis.py 16HBE 0 1__ --> G_hubris_seleted_sp_cell_type_16HBE_crapome_0_expression_1.graphml (__Figure S5__) <br>


6. __merged\_shorthest\_path\_graph.py__
    * __Aim__: Merge the shortest path graphs from the two cell lines (generated by shorthest\_path\_analysis.py) for the representation shown on __Figure 4__.
    * __Input files__: - CR_outputs/G_hubris_seleted_sp_cell_type_16HBE_crapome_1_expression_1.graphml <br>
                       - CR_outputs/G_hubris_seleted_sp_cell_type_IMR90_crapome_1_expression_1.graphml <br>
    * __Output Files__:CR_outputs/G_hubris_seleted_sp_merged_crapome_1_expression_1.graphml (__Figure 4__)<br>


7. __generate\_enrichment\_gene\_sets.py__
    * __Aim__: Generate the specific gene sets (as a preparation step for functional enrichment analysis) from all the network variations. Specifically, we determine sets for:<br>
                -the nodes of the induced graph between HHIP and the other GWAS genes (with and without the newly identified experimental edges) <br>
                -the set of genes constituting the new paths (created by the new edges) between HHIP and the other GWAS genes <br>
                -set of the new, experimentally identified interactors <br>
                -set of genes constituting shortened paths and 2-step paths <br>
                
      We generate these new sets for all 2x2x3 = 12 network variants generated by the parameters __cell_line__ (16HBE, IMR90, union); __filter_crapome__ (True, False); __filter_networks_based_on_expression__ (True, False) <br>
      The script (optionally) also saves the different HUBRIS variations into __.gml__ files 
    * __Input files__: - G_hubris.gpickle <br>
                       - all_significant_links_HHIP.xlsx <br>
                       - RNASeq_lists/*cell_line*_RNASeq_genes_expressed.csv
    * __Key parameter(s)__: - regenerate_gene_subsets (bool, default = False)
                            - save_HUBRIS_gmls (bool, default = False)
                            - copd_gwas_genes (list, default = ['FAM13A','IREB2','DSP','AGER','MFAP2','FBLN5','NPNT','FBXO38','SFTPD','TET2','TGFB2','MMP12','MMP1']<br>
    * __Std output__: progress report; network statistics
    * __Output Files__:-gene_subset_variations_dict_for_functional_enrichment.pickle (pickled python dictionary of the 5 different gene sets generated for the 12 network variations) <br>
                       -_all the HUBRIS network variations_ in HUBRIS_variations/*.gml


python functional\_enrichment\_new\_paths.py

python new\_paths\_graph.py

python functional\_enrichment\_new\_interactors.py

python functional\_enrichment\_induced\_graph.py

python highlighted\_pathway\_stats.py

# Visualization

For the visualization of the networks the yED (Version 3.21.1)  software was used in Ubuntu 22.04.3 LTS

All network visualizations in the manuscript are finalized by manual editing. However the majority of the graph properties are generated by the python scripts.

To reproduce a figure follow these steps:

1. Load a .graphml into yED via File → Open or by dragging and dropping it through the screen. If the software gives warnings about the conversion of properties data just OK them. 

2. Open the Properties Mapper, by clicking Edit → Properties Mapper 

3. If the configuration is not loaded yet import the configuration (node colors, node size etc.) by clicking import (green arrow in the top left corner of the Properties Mapper) and load _HHIP\_network\_config\_for\_yED.cnfx_ 

4. Select the HHIP\_ego\_network (Node) configuration on the left and click Apply then OK

5. Click Layout → Organic (here the settings can be changed) and OK

6. To remove directional arrows (all the networks are undirected) click on an edge and press Ctrl+A to select all edges. Then in the Properties View (bottom right) set the Target Arrow option to a line (just like the Source Arrow above it)

From this point every other change is manual fine-tuning to the author’s taste. One can move nodes around by first selecting them then moving them around (or by adjusting the layout parameters) and most properties (node size, label font, colors, etc) can be changed in the Properties View. For more systematic changes one can adjust the configuration in the Properties Mapper. You’re smart, you’ll figure it out. 

Bonus tip: add the color legend boxes as big nodes next to the network (or Copy-Paste them from the existing graphmls). To add a new node drag and drop the desired shape from the Palette panel on the top right. 

# Biorosetta 

The data files for Biorosetta are stored locally and no remote option is used in the current configuration. The last download of the data files are from February 2023. 

# HGNC tsv file (hgnc\_mapping.tsv)

This TSV is used alongside biorosetta to convert from uniprot ids. To download a more recent version visit: <https://www.genenames.org/download/statistics-and-files/>.

The version used to produce the results is from 05 Oct 2022. 

# Python package versions: 

Python V=3.9.16
biomart==0.9.2
biorosetta==0.3.2
gseapy==1.0.6
matplotlib==3.8.0
networkx==3.2
numpy==1.24.3
pandas==2.0.1
scipy==1.11.3
tqdm==4.65.0
xlrd==2.0.1

