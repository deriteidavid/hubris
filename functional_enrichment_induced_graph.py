from generate_enrichment_gene_sets import *

from gseapy import barplot, dotplot
gene_sets=['KEGG_2021_Human','GO_Cellular_Component_2018','GO_Biological_Process_2021']

G_hubris = G_hubris_og.copy()
background=list(G_hubris.nodes())

nodes_subset = 'Induced_graph_nodes_in_HUBRIS_extended'
enrichment_results = {}
enrichment_results[nodes_subset]={}

for key_tuple in gene_subset_variations[nodes_subset].keys():
    print(key_tuple)
    gene_list = gene_subset_variations[nodes_subset][key_tuple]
    enr = gp.enrichr(gene_list=gene_list, # or "./tests/data/gene_list.txt",
                             gene_sets=gene_sets,
                             organism='human', # don't forget to set organism to the one you desired! e.g. Yeast
                             background=background,
                             outdir=None)
    
    enrichment_results[nodes_subset][key_tuple] = enr
    
key_tuples=[('16HBE', True, True),
('16HBE', False, True),
('IMR90', True, True),
('IMR90', False, True),
('union', True, True),
('union', False, True),
('union', True, False)]

key_tuple=key_tuples[0]

df=enrichment_results[nodes_subset][key_tuple].results[['Gene_set','Term','Adjusted P-value']].copy()
df['pathway'] = df[['Gene_set', 'Term']].agg(': '.join, axis=1)
df=df[['pathway','Adjusted P-value']]
df=df[df['Adjusted P-value']<=0.05]
df.columns = ['pathway', str(key_tuple)]
df=df.set_index('pathway')

for key_tuple in key_tuples[1:]:
    print(key_tuple)
    #df_ = df.copy()
    
    df_=enrichment_results[nodes_subset][key_tuple].results[['Gene_set','Term','Adjusted P-value']].copy()
    df_['pathway'] = df_[['Gene_set', 'Term']].agg(': '.join, axis=1)
    df_=df_[['pathway','Adjusted P-value']]
    df_=df_[df_['Adjusted P-value']<=0.05]
    df_.columns = ['pathway', str(key_tuple)]
    df_=df_.set_index('pathway')
    
    df = pd.concat([df,df_],axis=1)
    
df['nr_of_significant_columns']=len(df.columns)-df.isnull().sum(axis=1)
df=df.sort_values('nr_of_significant_columns',ascending=False).fillna('ns')
df.to_excel('CR_outputs/functional_enrichment/Supplementary_Table_S4_%s.xlsx'%nodes_subset)
