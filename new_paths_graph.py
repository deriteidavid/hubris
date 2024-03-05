import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np
import urllib
from biomart import BiomartServer
import pickle
import glob
import random
import tqdm
import gseapy as gp
from gseapy import Biomart
import glob
import hubris_functions as hf

with open('G_hubris.gpickle', 'rb') as f:
    G_hubris= pickle.load(f)
    
#taking the LCC
G_hubris=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
print(G_hubris.number_of_nodes(), G_hubris.number_of_edges())
G_hubris.number_of_nodes()

#For this graph we use the union of 16HBE and IMR90 interactions with CRAPome controls and no RNASeq filtering
experiment = 'union'



copd_gwas_genes=['FAM13A',
                 'IREB2',
                 'DSP',
                 'AGER',
                 'MFAP2',
                 'FBLN5',
                 'NPNT',
                 'FBXO38',
                 'SFTPD',
                 'TET2',
                 'TGFB2', 
                 'MMP12',
                 'MMP1']
                 
#we read in the experimental edges and add them to the network
df_all_HHIP_links=pd.read_excel('all_significant_links_HHIP.xlsx')
target_proteins=list(df_all_HHIP_links[(df_all_HHIP_links['crapome_16HBE_06']==1) | (df_all_HHIP_links['crapome_16HBE_11']==1) | (df_all_HHIP_links['crapome_IMR90_06']==1)]['bait_gene_symbol'])

new_targets_list=[]
new_edges=[]
new_edges+=list(zip(['HHIP' for i in range(len(target_proteins))], target_proteins))
print(new_edges)

G_hubris_extended=G_hubris.copy()
G_hubris_extended.add_edges_from(new_edges)

G_induced_hubris,hubris_sp_count_and_len=hf.induced_graph(G_hubris,'HHIP', copd_gwas_genes)
G_induced_hubris_extended,hubris_extended_sp_count_and_len=hf.induced_graph(G_hubris_extended,'HHIP', copd_gwas_genes)

G_new_paths=G_hubris_extended.subgraph(list(set(G_induced_hubris_extended.nodes())-set(G_induced_hubris.nodes()))+copd_gwas_genes+target_proteins).copy()
print(len(max(nx.connected_components(G_new_paths), key=len)))
print(G_new_paths.number_of_nodes())
G_new_paths.remove_edges_from(nx.selfloop_edges(G_new_paths))
colors = []
for node in G_new_paths.nodes():
    G_new_paths.nodes[node]['label']=node
    if node in copd_gwas_genes:
        colors.append('red')
        G_new_paths.nodes[node]['type']='gwas'
    elif node in target_proteins:
        colors.append('green')
        G_new_paths.nodes[node]['type']='new_link'
    else:
        colors.append('grey')
        G_new_paths.nodes[node]['type']='bridge'

for e in G_new_paths.edges():
    
    if 'db' in G_new_paths.edges[e].keys():
        db=G_new_paths.edges[e]['db']
        G_new_paths.edges[e]['db']=str(db)

nx.write_graphml(G_new_paths,'CR_outputs/G_new_paths.graphml') 
