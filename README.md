# Running all scripts

To run the Python scripts reproducing the network analysis results published in the paper run the bash script: 

run_all_scirpts_in_sequence.sh

# Running scripts individually 
In this section we document the individual scripts needed to create the HUBRIS networks, the different cell-type specific versions, and the related analyses. 

1. __python process\_SAINTExpress\_output\_excels.py__ <br>
    * __Aim__: Process the output files of the SAINTExpress analysis (HHIP\_SAINTexpress\_consolidated.xlsx), which consolidates the raw AP-MS interaction data into statistically significant interactions. The goal is to have a simplified list of interactions for the different cases (celly type, CRAPome etc.), which also constitutes the input for later network analysis scripts.
    * __Input files__: HHIP\_SAINTexpress\_consolidated.xlsx <br>
    * __Std output__: list of statistically significant interactions on the standard output for all cases (cell type, CRAPome (yes/no)) <br>
    * __Output Files__: all_significant_links_HHIP.xlsx; Supplementary_Table_S1_all_significant_links_HHIP.xlsx <br> 

2. __python RNASeq\_based\_filtering.py__ 
    * __Aim__: Determine which genes are expressed in the two cell lines (IMR90, 16HBE) based on RNA-Seq data.
    * __Input files__: rnaseq\_PPI\_GWAS/imr90/gene\_count.xlsx;  rnaseq\_PPI\_GWAS/imr90/gene\_fpkm\_group.xlsx;  rnaseq\_PPI\_GWAS/16hbe/gene\_count.xlsx; rnaseq\_PPI\_GWAS/16hbe/gene\_fpkm\_group.xlsx
    * __Key parameter(s)__: expression_threshold (default = 0.25)
    * __Std output__: -
    * __Output Files__:IMR90_RNASeq_genes_expressed.csv; 16HBE_RNASeq_genes_expressed.csv; <br>
    Figures: CR_outputs/RNASeq_IMR90.png; CR_outputs/RNASeq_16HBE.png (__Supplementary Figure S12__)


3. __python create\_HUBRIS.py__
    * __Aim__: Generate the HUBRIS network by either re-downloading the constituent databases or using existing downloads. This script also does the conversion between ID-s (using biorosetta) and the merging of the networks
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
                        Figures: CR_outputs/HUBRIS_db_analytics.png (__Supplementary Figure S11__)



4. __python generate\_HHIP\_ego\_networks.py *cell_line filter_crapome filter_networks_based_on_expression*__
    * __Aim__: Generate the "ego" network of HHIP based on HUBRIS and our newly identified edges. 
    * __Input files__: - G_hubris.gpickle <br>
                       - all_significant_links_HHIP.xlsx <br>
                       - (optional) RNASeq_lists/*cell_line*_RNASeq_genes_expressed.csv
    * __Key parameter(s)__: - cell_line (str, options:'intersection', 'union', 'IMR90', '16HBE'): which cell line's data to use (interactions and RNA-Seq)<br>
                            - filter_crapome (bool), filter_networks_based_on_expression (bool, options: True= SAINTExpress interactions with CRAPome priors; False= without CRAPOME priors) <br>
                            - filter_networks_based_on_expression (bool, options: True = filter the network based on RNA-Seq expression; False = no filtering)
    * __Std output__: progress report; network statistics
    * __Output Files__: 




6. __python shorthest\_path\_analysis.py IMR90 1 1__

python shorthest\_path\_analysis.py 16HBE 1 1 

python merged\_shorthest\_path\_graph.py

python shorthest\_path\_analysis.py IMR90 0 1 

python shorthest\_path\_analysis.py 16HBE 0 1

python generate\_HHIP\_ego\_networks.py union 0 1

python generate\_enrichment\_gene\_sets.py 1

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

aiohttp==3.8.4

aiosignal==1.3.1

async-timeout==4.0.2

biomart==0.9.2

biorosetta==0.3.2

biothings-client==0.3.1

brotlipy==0.7.0

contourpy==1.1.1

cycler==0.12.1

dataclasses-json==0.5.7

docx2txt==0.8

et-xmlfile==1.1.0

faiss-cpu==1.7.4

fastrlock==0.8.2

fonttools==4.43.1

frozenlist==1.3.3

greenlet==2.0.2

gseapy==1.0.6

kiwisolver==1.4.5

langchain==0.0.164

llama-index==0.6.4

marshmallow-enum==1.5.1

matplotlib==3.8.0

multidict==6.0.4

mypy-extensions==1.0.0

networkx==3.2

numexpr==2.8.4

numpy==1.24.3

openai==0.27.6

openapi-schema-pydantic==1.2.4

openpyxl==3.1.2

pandas==2.0.1

Pillow==10.0.1

ply==3.11

pydantic==1.10.7

pyparsing==3.1.1

PyPDF2==3.0.1

PyQt5-sip==12.11.0

PyYAML==6.0

pyzmq==19.0.2

regex==2023.5.5

scipy==1.11.3

seaborn==0.13.0

SQLAlchemy==2.0.12

tenacity==8.2.2

tiktoken==0.4.0

tqdm==4.65.0

typing-inspect==0.8.0

tzdata==2023.3

webencodings==0.5.1

xlrd==2.0.1

yarl==1.9.2

