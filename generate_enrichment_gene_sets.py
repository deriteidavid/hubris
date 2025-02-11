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

regenerate_gene_subsets = False

if len(sys.argv)>1:
    
    regenerate_gene_subsets = sys.argv[1]


if not regenerate_gene_subsets:
    with open('gene_subset_variations_dict_for_functional_enrichment.pickle', 'rb') as f:
        gene_subset_variations = pickle.load(f)

else:

    gene_subset_variations = {}
    gene_subset_variations['Induced_graph_nodes_in_HUBRIS_extended'] = {}
    gene_subset_variations['Induced_graph_nodes_in_HUBRIS_default'] = {}
    gene_subset_variations['New_paths_node_set'] = {}
    gene_subset_variations['New_interactors_only'] = {}
    gene_subset_variations['Shortened_paths_and_two_step_paths'] = {}


    for cell_line, filter_crapome, filter_networks_based_on_expression in itertools.product(['16HBE','IMR90','union'], [True,False],[True,False]):
        key_tuple=(cell_line, filter_crapome, filter_networks_based_on_expression) 
        
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


        if filter_networks_based_on_expression:
            copd_gwas_genes=list(set(copd_gwas_genes).intersection(set(G_hubris.nodes())))

        #we create a copy of hubris and add the new edges
        new_edges=[]
        new_edges+=list(zip(['HHIP' for i in range(len(target_proteins[experiment]))], target_proteins[experiment]))
        G_hubris_extended=G_hubris.copy()
        G_hubris_extended.add_edges_from(new_edges)

        #Next we generate the induced graph in each network between HHIP and the other COPD GWAS genes. 
        G_induced_hubris,hubris_sp_count_and_len=hf.induced_graph(G_hubris,'HHIP', copd_gwas_genes)
        G_induced_hubris_extended,hubris_extended_sp_count_and_len=hf.induced_graph(G_hubris_extended,'HHIP', copd_gwas_genes)

        #next we generate the graph that shows the highlighted shortest paths between HHIP and the other GWAS genes

        selected_path_targets=np.array(copd_gwas_genes)[(hubris_extended_sp_count_and_len[1,:]<hubris_sp_count_and_len[1,:]) | (hubris_extended_sp_count_and_len[1,:]<=2)]

        #print('Shortened or <=2 step paths in extened HUBRIS to:',selected_path_targets)

        sp_list=[]
        for i in selected_path_targets:
            sp_list.append(['HHIP',str(i)])

        cell_line_column_mapping={'IMR90': set(['sainte_IMR90_06','crapome_IMR90_06',]),
                                   '16HBE': set(['sainte_16HBE_06','sainte_16HBE_11','crapome_16HBE_06','crapome_16HBE_11'])}

        node_to_cell_line_mapping={}

        if filter_crapome:
            relevant_columns = ['bait_gene_symbol', 'crapome_IMR90_06', 'crapome_16HBE_06','crapome_16HBE_11']
        else: 
            relevant_columns = ['bait_gene_symbol', 'sainte_IMR90_06', 'sainte_16HBE_06', 'sainte_16HBE_11']

        for i,row in df_all_HHIP_links[relevant_columns].iterrows():

            if row['bait_gene_symbol'] in target_proteins[experiment]:

                columns_where_the_row_is_1=set(row.keys()[(row==1)])
                node_cell_lines=[]

                for cl in cell_lines:
                    if cell_line_column_mapping[cl].intersection(columns_where_the_row_is_1):
                        node_cell_lines.append(cl)

                node_label = ' and '.join(node_cell_lines)

                node_to_cell_line_mapping[row['bait_gene_symbol']] = node_label

        G_hubris_seleted_sp=nx.Graph()
        for e in sp_list:
            #print(e[1])
            #print('hubris',list(nx.shortest_paths.all_shortest_paths(G_hubris_extended, e[0],e[1])))

            for sp in list(nx.shortest_paths.all_shortest_paths(G_hubris_extended, e[0],e[1])):
                G_hubris_seleted_sp.add_edges_from(list(zip(sp[:-1],sp[1:])))

        gene_subset_variations['Induced_graph_nodes_in_HUBRIS_extended'][key_tuple]=list(G_induced_hubris_extended.nodes())
        gene_subset_variations['Induced_graph_nodes_in_HUBRIS_default'][key_tuple]=list(G_induced_hubris.nodes())
        gene_subset_variations['New_paths_node_set'][key_tuple]=list(set(G_induced_hubris_extended.nodes())-set(G_induced_hubris.nodes())-set(target_proteins[experiment])-set(copd_gwas_genes))
        gene_subset_variations['New_interactors_only'][key_tuple]=target_proteins[experiment]
        gene_subset_variations['Shortened_paths_and_two_step_paths'][key_tuple]=list(G_hubris_seleted_sp.nodes())
    
    with open('gene_subset_variations_dict_for_functional_enrichment.pickle', 'wb') as fp:
        pickle.dump(gene_subset_variations, fp)
