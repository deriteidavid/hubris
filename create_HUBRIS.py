import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import numpy as np
import urllib
from biomart import BiomartServer
import pickle
import glob
import random
import biorosetta as br
import tqdm
import urllib.request
import gzip
import shutil
import hubris_functions as hf
from collections import Counter
import itertools

np.random.seed(0)

#reading in the database config file
df_databases=pd.read_excel('databases.xlsx')

#the path for the biorosetta mapping files (offline use) 
biorosetta_data_path = 'biorosetta_data/data/'

#should the databases be re-downloaded? If False the ones specified in the database config excel will be used.
#NOTE that the configuration in the database config excel is subject to change and should be updated manually
#WARNING: whatever is in the paths specified in the df_databases will be OVERWRITTEN if not specified otherwise.  

re_download=False

#which databases should be downloaded

to_download=['HumanNet','HIPPIE','BioGrid','NCBI','StringDB','Interactome3D','HURI','Reactome']

if re_download:
    print('Downloading databases')
    hf.hubris_download_databases(to_download, df_databases)

#which databases should be merged into the HUBRIS network?    
to_merge=['HumanNet','HIPPIE','BioGrid','NCBI','StringDB','Interactome3D','HURI','Reactome']

#The consensus id type to which all dbs (which are not already in it) will be converted before merging 
consensus_id_type='entr'

#Other than Biorosetta (https://pypi.org/project/biorosetta/) we use the below hgnc mapping to convert between IDs
# to download a more recent version visit: https://www.genenames.org/download/statistics-and-files/
df_hgnc=pd.read_csv('hgnc_mapping.tsv',sep='\t',engine='python')
hgnc_column_dict={'entr':'entrez_id',
'ensg':'ensembl_gene_id',
'unipr':'uniprot_ids',
'symb':'symbol'}

#the below function iterates through the rows of the database configuration table (df_databases), converts the ids
#to the consensus_id_type using Biorosetta and a local file of the hgnc mapping and creates the undirected PPI graphs.
graphs = hf.create_graphs_with_consensus_ids(df_databases,to_merge,df_hgnc,hgnc_column_dict,consensus_id_type,biorosetta_data_path=biorosetta_data_path)

#We merge the constituent graphs into a single graph:
G_merged=nx.compose_all(graphs.values())

#Next we iterate through the edges of the merged graph and add as an edge-attribute the list of database names that included the edge
merged_edge_attr={}
for e in tqdm.tqdm(G_merged.edges()):
    merged_edge_attr[e]=set([])
    for db_name,g in graphs.items():
        if g.has_edge(e[0],e[1]):
            merged_edge_attr[e].add(db_name)
nx.set_edge_attributes(G_merged,merged_edge_attr,name='db')

with open('G_merged_raw.gpickle', 'wb') as f:
    pickle.dump(G_merged, f, pickle.HIGHEST_PROTOCOL)


#if the initial consensus_id_type wasn't gene symbol, we want a version of the network where it is gene symbol
#this way the interpretation is easier

if consensus_id_type!='symb':
    #idmap = br.IDMapper([br.EnsemblBiomartMapper(),br.HGNCBiomartMapper()]) # Multiple sources
    idmap = br.IDMapper([br.EnsemblBiomartMapper(data_path=biorosetta_data_path+'ensembl.tsv'), br.HGNCBiomartMapper(data_path=biorosetta_data_path+'hgnc.tsv')]) 
    translation_list=idmap.convert(list(G_merged.nodes()),consensus_id_type,'symb', multi_hits='all')
    translation_dict=dict(zip(list(G_merged.nodes()),translation_list))
    for k,v in translation_dict.items():
        if v=='N/A':
            translation_dict[k]=k+'_'+consensus_id_type
    G_merged_symb=hf.relabel_nodes_with_preserving_attributes(G_merged,translation_dict)       
else:
    G_merged_symb = G_merged
    

print('Raw network: N=',G_merged_symb.number_of_nodes(),'E=',G_merged_symb.number_of_edges())
  
#Filtering the edges of the merged network based on the database count
db_count_threshold=2

db_count=[]
single_source_edges=[]
for e in G_merged_symb.edges(data=True):
    if len(e[2]['db'])<db_count_threshold:  
        single_source_edges.append(e)
    db_count.append(len(e[2]['db']))
print('database support count:',Counter(db_count))
G_hubris=G_merged_symb.copy()
G_hubris.remove_edges_from(single_source_edges)

#we save the final network into a gpickle
with open('G_hubris.gpickle', 'wb') as f:
    pickle.dump(G_hubris, f, pickle.HIGHEST_PROTOCOL)
#we also save it into a gml and edgelist
nx.write_gml(G_hubris,'G_hubris.gml',stringizer=str)
nx.write_edgelist(G_hubris,'G_hubris.txt')

print('After filtering: N=',G_hubris.number_of_nodes(),'E=',G_hubris.number_of_edges())

G_hubris_LCC=G_hubris.subgraph(max(nx.connected_components(G_hubris), key=len))
print('LCC: N=',G_hubris_LCC.number_of_nodes(), 'E=',G_hubris_LCC.number_of_edges())

nx.write_gml(G_hubris_LCC,'G_hubris_lcc.gml',stringizer=str)
nx.write_edgelist(G_hubris_LCC,'G_hubris_lcc.txt')

# Plot HUBRIS stats as shown in the manuscript
edge_dbs=[]
for e in single_source_edges:
    edge_dbs.append(list(e[2]['db'])[0])
single_edge_dbs=dict(Counter(edge_dbs))
multi_source_edges_dbs=[]

for e in G_hubris.edges(data=True):
    multi_source_edges_dbs+=e[2]['db']
multi_edge_db_counts= Counter(multi_source_edges_dbs)
multi_edge_db_counts= dict(sorted(multi_edge_db_counts.items(), key=lambda item: item[1],reverse=True))

db_list=[  'NCBI','BioGrid',  'HIPPIE','HumanNet','StringDB', 'HURI', 'Reactome', 'Interactome3D']
db_e_count={}
for k in itertools.product(db_list,db_list):
    db_e_count[k]=0
for e in G_hubris.edges(data=True):
    dbs_e=e[2]['db']
    for pair in itertools.product(dbs_e,dbs_e):
        db_e_count[pair]+=1
 
 
db_e_count_array=np.zeros((len(db_list),len(db_list)))
for k,v in db_e_count.items():
    db_e_count_array[db_list.index(k[0]),db_list.index(k[1])]=v
    
db_e_count_ratios=db_e_count_array/G_hubris.number_of_edges()

fig, axs = plt.subplots(2,2,figsize=(20,20))

e=list(dict(sorted(Counter(db_count).items())).values())
total=sum(e)
axs[0,0].bar(range(1,9),np.array(e),log=True)
axs[0,0].set_title('Database suppport count distribution of all edges')
for i,ec in enumerate(e):
    axs[0,0].text(i+.5, ec+(ec*0.1), '%.3f'%(ec/total*100)+'%')
axs[0,0].set_xlabel('Database support count')
axs[0,0].set_ylabel('nr of edges')
axs[0,0].spines[['right', 'top']].set_visible(False)

single_edge_dbs= dict(sorted(single_edge_dbs.items(), key=lambda item: item[1],reverse=True))
e=list(single_edge_dbs.values())
total=sum(e)
axs[0,1].bar(range(1,9),np.array(e),log=True)
axs[0,1].set_title('Source distribution of edges found in a single database (db support count=1)')
for i,ec in enumerate(e): 
    axs[0,1].text(i+0.5, ec+(ec*0.1), '%.3f'%(ec/total*100)+'%')
axs[0,1].set_ylabel('nr of edges')
axs[0,1].set_xticks(range(1,9),single_edge_dbs.keys(), rotation=45)
axs[0,1].spines[['right', 'top']].set_visible(False)


e=list(multi_edge_db_counts.values())
total=G_hubris.number_of_edges()
axs[1,0].bar(range(1,9),np.array(e),log=True)
axs[1,0].set_title('Source distribution of edges found in multiple databases')
for i,ec in enumerate(e): 
    axs[1,0].text(i+0.5, ec+(ec*0.1), '%.2f'%(ec/total*100)+'%')
axs[1,0].set_ylabel('nr of edges')
axs[1,0].set_xticks(range(1,9),multi_edge_db_counts.keys(), rotation=45)
axs[1,0].spines[['right', 'top']].set_visible(False)


im=axs[1,1].imshow(np.log10(db_e_count_ratios))
axs[1,1].set_xticks(range(len(db_list)),db_list,rotation=45)
axs[1,1].set_yticks(range(len(db_list)),db_list)
cb=plt.colorbar(im,ax=axs[1, 1])
cb.set_label(label=r'$log_{10}(\frac{E_{shared}*100}{E_{total}})$',size=16)
axs[1,1].set_title('Percentage of multi source (db support count>2) edges \n shared by the PPI databases',fontsize=16)
plt.rc('font', size=14)
for (j,i),label in np.ndenumerate(db_e_count_ratios):
    axs[1,1].text(i,j,str(label*100)[:5],ha='center',va='center')
plt.savefig('HUBRIS_db_analytics.png')

