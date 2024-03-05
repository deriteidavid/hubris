import pandas as pd 


highlighted_pathways = ['KEGG_2021_Human: PI3K-Akt signaling pathway',
'KEGG_2021_Human: TGF-beta signaling pathway',
'KEGG_2021_Human: Focal adhesion',
'GO_Cellular_Component_2018: focal adhesion (GO:0005925)',
'KEGG_2021_Human: Adherens junction',
'KEGG_2021_Human: Tight junction',
'GO_Biological_Process_2021: actin cytoskeleton reorganization (GO:0031532)',
'KEGG_2021_Human: Regulation of actin cytoskeleton',
'GO_Cellular_Component_2018: stress fiber (GO:0001725)',
'KEGG_2021_Human: Hippo signaling pathway',
'GO_Biological_Process_2021: extracellular structure organization (GO:0043062)',
'GO_Biological_Process_2021: external encapsulating structure organization (GO:0045229)',
'GO_Biological_Process_2021: extracellular matrix organization (GO:0030198)',
'GO_Biological_Process_2021: collagen fibril organization (GO:0030199)',
'KEGG_2021_Human: ECM-receptor interaction',
'GO_Cellular_Component_2018: actin cytoskeleton (GO:0015629)']

df = pd.read_excel('CR_outputs/functional_enrichment/Supplementary_Table_S3_New_paths_node_set.xlsx')

df[df['pathway'].isin(highlighted_pathways)][["pathway","('16HBE', True, True)","('IMR90', True, True)","('union', True, False)"]].to_excel('highlighted_pathways.xlsx')




