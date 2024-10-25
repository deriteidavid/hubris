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

#we read in the GPickle generated by create_HUBRIS.py 
with open('G_hubris.gpickle', 'rb') as f:
    G_hubris= pickle.load(f)

#we only keep the largest connected component: 
G_hubris=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
print('N=',G_hubris.number_of_nodes(), 'E=',G_hubris.number_of_edges())

non_translated_nodes=[]
for i in G_hubris.nodes():
    if '_' in i:
        non_translated_nodes.append(i)
print('Nr of nodes with no translation:',len(non_translated_nodes))

#PARAMETERS:

cell_line='union' #options: intersection, union, IMR90, 16HBE
cell_lines=['IMR90','16HBE'] 
filter_crapome=True
filter_networks_based_on_expression=True


#The parameters are always overriden by system arguments, otherwise the above params are used.
#The system parameter order is: cell_line (str), filter_crapome (bool), filter_networks_based_on_expression (bool)
if len(sys.argv)>1:
    
    cell_line = sys.argv[1]
    filter_crapome = hf.str_to_bool(sys.argv[2])
    filter_networks_based_on_expression = hf.str_to_bool(sys.argv[3])
    
    
print ('cell_line:',cell_line,
       ' filter_crapome:',filter_crapome, 
       ' filter_networks_based_on_expression:',filter_networks_based_on_expression)
       
       
#HUBRIS-only (no experimental egdes from our study) ego network of HHIP before filtering
G_ego_HHIP = G_hubris.subgraph(list(G_hubris.neighbors('HHIP'))+['HHIP']).copy()

#filtering based on RNASeq
if filter_networks_based_on_expression:
    
    G_hubris = hf.filter_hubris_based_on_cell_type_specific_gene_list(G_hubris,cell_line,cell_lines,keep_nodes=['HHIP'])  
  
    #taking the LCC
    G_hubris=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
    print('After filtering: N=%d, E=%d'%(G_hubris.number_of_nodes(), G_hubris.number_of_edges())) 
    
#Generating the figure for the HUBRIS-only ego network of HHIP
expressed_neighbors=list(G_hubris.neighbors('HHIP'))  
for n in G_ego_HHIP.nodes():
    print(n)
    if n in expressed_neighbors:
        colors = ('#5ad45a','#000000')
    elif n == 'HHIP':
        colors = ('#b30000','#ffffff')
    else:
        colors = ('#ffffff','#000000')
    
    G_ego_HHIP.nodes[n]['name']=n
    G_ego_HHIP.nodes[n]['color']=colors[0]
    G_ego_HHIP.nodes[n]['font_color']=colors[1]
    G_ego_HHIP.nodes[n]['width']=60
    G_ego_HHIP.nodes[n]['height']=30
    G_ego_HHIP.nodes[n]['font_size']=12
for e in G_ego_HHIP.edges():
    G_ego_HHIP.edges[e]['db'] = ', '.join(list(G_ego_HHIP.edges[e]['db']))
G_ego_HHIP.remove_edges_from(nx.selfloop_edges(G_ego_HHIP))
nx.write_graphml(G_ego_HHIP,'CR_outputs/G_ego_HUBRIS_only_cell_type_%s_expression_%s.graphml'%(cell_line,str(int(filter_networks_based_on_expression))))

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

# Create an ego network for a figure just using the new edges
G_ego_plot=nx.Graph()

cell_line_column_mapping={'IMR90': set(['sainte_IMR90_06','crapome_IMR90_06',]),
                          '16HBE': set(['sainte_16HBE_06','sainte_16HBE_11','crapome_16HBE_06','crapome_16HBE_11'])}

color_scheme={'16HBE':('#1a53ff','#ffffff'), #(node color, font color)
              'IMR90':('#ffcc00','#000000'),
              'IMR90 and 16HBE':('#5ad45a','#000000'),
              'GWAS':('#b30000','#ffffff')}

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
        if row['bait_gene_symbol'] == 'HHIP':
            node_label = 'GWAS'
            
        print(row['bait_gene_symbol'],node_label)
        
        G_ego_plot.add_edge('HHIP',row['bait_gene_symbol'])
        G_ego_plot.nodes[row['bait_gene_symbol']]['label']=node_label
        G_ego_plot.nodes[row['bait_gene_symbol']]['name']=row['bait_gene_symbol']
        G_ego_plot.nodes[row['bait_gene_symbol']]['color']=color_scheme[node_label][0]
        G_ego_plot.nodes[row['bait_gene_symbol']]['font_color']=color_scheme[node_label][1]
        G_ego_plot.nodes[row['bait_gene_symbol']]['width']=60
        G_ego_plot.nodes[row['bait_gene_symbol']]['height']=30
        G_ego_plot.nodes[row['bait_gene_symbol']]['font_size']=12
        G_ego_plot.nodes[row['bait_gene_symbol']]['font_style']='Bold'
        
inter_edges=list(G_hubris.subgraph(G_ego_plot.nodes).edges())
G_ego_plot.add_edges_from(inter_edges)
G_ego_plot.remove_edges_from(nx.selfloop_edges(G_ego_plot))
nx.write_graphml(G_ego_plot,'CR_outputs/G_ego_plot_cell_type_%s_crapome_%s_expression_%s.graphml'%(cell_line,str(int(filter_crapome)),str(int(filter_networks_based_on_expression))))


