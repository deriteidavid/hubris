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
import sys
import hubris_functions as hf
import itertools

#we read in the GPickle generated by create_HUBRIS.py 
with open('G_hubris.gpickle', 'rb') as f:
    G_hubris= pickle.load(f)
    
cell_lines=['IMR90','16HBE'] 

#we only keep the largest connected component: 
G_hubris=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
print('N=',G_hubris.number_of_nodes(), 'E=',G_hubris.number_of_edges())

non_translated_nodes=[]
for i in G_hubris.nodes():
    if '_' in i:
        non_translated_nodes.append(i)
print('Nr of nodes with no translation:',len(non_translated_nodes))

G_hubris_og = G_hubris.copy()

#If we already generated the different gene subsets for enrichment analysis then we can load the 
#dictionary and skip the lengthy calculations. If the network changed in any way it's worth recalcualting. 

save_HUBRIS_gmls = True

for cell_line, filter_crapome, filter_networks_based_on_expression in itertools.product(['16HBE','IMR90','union'], [True,False],[True,False]):
    key_tuple=(cell_line, filter_crapome, filter_networks_based_on_expression) 
    
    G_hubris = G_hubris_og.copy()
    
    print ('cell_line:',cell_line,
           ' filter_crapome:',filter_crapome, 
           ' filter_networks_based_on_expression:',filter_networks_based_on_expression)

    #filtering based on RNASeq
    if filter_networks_based_on_expression:

        G_hubris = hf.filter_hubris_based_on_cell_type_specific_gene_list(G_hubris,cell_line,cell_lines,keep_nodes=['HHIP'])  

        #taking the LCC
        G_hubris=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
        print('After filtering: N=%d, E=%d'%(G_hubris.number_of_nodes(), G_hubris.number_of_edges())) 

    #We load the experimental edges:
    df_all_HHIP_links=pd.read_excel('all_significant_links_HHIP.xlsx')
    target_proteins={} #the dictionary containing the new edges

    #We next determine the new experimental edges based on the input parameters (cell_line, crapome, expression)
    #NOTE: there are two 16HBE experiments (06 and 11). We use an OR rule between the links found to be singnificant in either
    #, i.e. if a link shows up in either of the two experiments we include it in our network. 
    if filter_crapome:
        if cell_line=='IMR90':
            experiment='IMR90_06'
            target_proteins[experiment]=list(df_all_HHIP_links[df_all_HHIP_links['crapome_IMR90_06']==1]['bait_gene_symbol'])
        elif cell_line=='16HBE':
            experiment='16HBE_06_11'
            target_proteins[experiment]=list(df_all_HHIP_links[(df_all_HHIP_links['crapome_16HBE_06']==1) | (df_all_HHIP_links['crapome_16HBE_11']==1)]['bait_gene_symbol'])
        elif cell_line=='union':  
            experiment='union'
            target_proteins[experiment]=list(df_all_HHIP_links[(df_all_HHIP_links['crapome_16HBE_06']==1) | (df_all_HHIP_links['crapome_16HBE_11']==1) | (df_all_HHIP_links['crapome_IMR90_06']==1)]['bait_gene_symbol'])
        elif cell_line=='intersection':
            experiment='intersection'
            target_proteins[experiment]=list(df_all_HHIP_links[((df_all_HHIP_links['crapome_16HBE_06']==1) | (df_all_HHIP_links['crapome_16HBE_11']==1)) & (df_all_HHIP_links['crapome_IMR90_06']==1)]['bait_gene_symbol'])
    else:
        if cell_line=='IMR90':
            experiment='IMR90_06'
            target_proteins[experiment]=list(df_all_HHIP_links[df_all_HHIP_links['sainte_IMR90_06']==1]['bait_gene_symbol'])
        elif cell_line=='16HBE':
            experiment='16HBE_06_11'
            target_proteins[experiment]=list(df_all_HHIP_links[(df_all_HHIP_links['sainte_16HBE_06']==1) | (df_all_HHIP_links['sainte_16HBE_11']==1)]['bait_gene_symbol'])
        elif cell_line=='union':  
            experiment='union'
            target_proteins[experiment]=list(df_all_HHIP_links[(df_all_HHIP_links['sainte_16HBE_06']==1) | (df_all_HHIP_links['sainte_16HBE_11']==1) | (df_all_HHIP_links['sainte_IMR90_06']==1)]['bait_gene_symbol'])
        elif cell_line=='intersection':
            experiment='intersection'
            target_proteins[experiment]=list(df_all_HHIP_links[((df_all_HHIP_links['sainte_16HBE_06']==1) | (df_all_HHIP_links['sainte_16HBE_11']==1)) & (df_all_HHIP_links['sainte_IMR90_06']==1)]['bait_gene_symbol'])

    #we create a copy of hubris and add the new edges
    new_edges=[]
    new_edges+=list(zip(['HHIP' for i in range(len(target_proteins[experiment]))], target_proteins[experiment]))
    G_hubris_extended=G_hubris.copy()
    G_hubris_extended.add_edges_from(new_edges)

    #We save the different HUBRIS variations
    if save_HUBRIS_gmls:
        nx.write_gml(G_hubris,'PPI_networks_for_analysis/G_hubris_new_edges_0_cellline_%s_filter_crapome_%d_filter_expression_%d.gml'%(cell_line,int(filter_crapome),int(filter_networks_based_on_expression)),stringizer=str)
        nx.write_gml(G_hubris_extended,'PPI_networks_for_analysis/G_hubris_new_edges_1_cellline_%s_filter_crapome_%d_filter_expression_%d.gml'%(cell_line,int(filter_crapome),int(filter_networks_based_on_expression)),stringizer=str)


 
