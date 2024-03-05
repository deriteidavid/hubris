import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_excel('HHIP_SAINTexpress_consolidated.xlsx')
df_crapome=pd.read_excel('HHIP_CRAPome_SAINTexpress_consolidated.xlsx')

df=df.fillna(0)

df_crapome=df_crapome.fillna(0)

np.all(df['Alternate ID']==df_crapome['Alternate ID'])

df_cons=pd.DataFrame()

df_cons['bait_gene_symbol']=df['Alternate ID']

df_cons['sainte_IMR90_06']=df['SignifCall_IMR90_06']
df_cons['sainte_16HBE_06']=df['SignifCall_16HBE_06']
df_cons['sainte_16HBE_11']=df['SignifCall_16HBE_11']

df_cons['crapome_IMR90_06']=df_crapome['SignifCall_IMR90_06']
df_cons['crapome_16HBE_06']=df_crapome['SignifCall_16HBE_06']
df_cons['crapome_16HBE_11']=df_crapome['SignifCall_16HBE_11']


df_cons['link_sum']=df_cons[['sainte_IMR90_06', 'sainte_16HBE_06','sainte_16HBE_11', 'crapome_IMR90_06', 'crapome_16HBE_06',
       'crapome_16HBE_11']].sum(axis=1)

df_cons=df_cons[df_cons['link_sum']>0]

df_cons=df_cons.sort_values('link_sum',ascending=False)

df_cons.reset_index(drop=True).to_excel('all_significant_links_HHIP.xlsx')
df_cons.reset_index(drop=True).to_excel('Supplementary_Table_S1_all_significant_links_HHIP.xlsx') 

#counting the edges:
print('cell line: IMR90, CRAPome controls: False')
interactors = list(df_cons[df_cons['sainte_IMR90_06']==1]['bait_gene_symbol'])
print('Number of interactors (Including HHIP) :%d \n Interactors: '%len(interactors), interactors)

print('cell line: 16HBE, CRAPome controls: False')
interactors = list(df_cons[(df_cons['sainte_16HBE_06']==1) | (df_cons['sainte_16HBE_11']==1)]['bait_gene_symbol'])
print('Number of interactors (Including HHIP) :%d \n Interactors: '%len(interactors), interactors)

print('cell line: IMR90, CRAPome controls: True')
interactors = list(df_cons[df_cons['crapome_IMR90_06']==1]['bait_gene_symbol'])
print('Number of interactors (Including HHIP) :%d \n Interactors: '%len(interactors), interactors)

print('cell line: 16HBE, CRAPome controls: True')
interactors = list(df_cons[(df_cons['crapome_16HBE_06']==1) | (df_cons['crapome_16HBE_11']==1)]['bait_gene_symbol'])
print('Number of interactors (Including HHIP) :%d \n Interactors: '%len(interactors), interactors)


