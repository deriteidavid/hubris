import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

#RNASeq data originally retrieved from: /proj/regeps/regep00/pilots/rerpc/Pilot_rna_mrna_repjc_H202SC21081019/data/rna/mrna/H202SC21081019/data/raw/novogene_transfer_batches/Result_X202SC21081019-Z01-F003/Result_X202SC21081019-Z01-F003/3.Quant/1.Count

paths={'IMR90':'rnaseq_PPI_GWAS/imr90/', '16HBE':'rnaseq_PPI_GWAS/16hbe/'}

expression_threshold = 0.25
 
cell_line = 'IMR90'
path = paths[cell_line]

df=pd.read_excel(path+'gene_count.xlsx')
df_group=pd.read_excel(path+'gene_fpkm_group.xlsx')

zero_count_genes=df[(df['IMR90hTERT_1']==0) & (df['IMR90hTERT_2']==0) & (df['IMR90hTERT_2']==0)]['gene_id']

plt.figure(figsize=(8,4))
plt.title('IMR90 RNASeq FPKM distribution', fontsize=16)
plt.xlabel('$Log_2(FPKM)$',fontsize=16)
plt.ylabel('count',fontsize=16)
plt.vlines(x=expression_threshold, ymin=0,ymax=5000,color='red', label='expression threshold=%f'%expression_threshold)
plt.hist(np.log2(df_group[~df_group.geneID.isin(zero_count_genes)]['IMR90hTERT']+1),bins=100,log=True)
plt.legend(fontsize=14)
plt.savefig('CR_outputs/RNASeq_IMR90.png')

df_group[(~df_group.geneID.isin(zero_count_genes)) & (df_group['IMR90hTERT']>=expression_threshold  )]['geneID'].to_csv('IMR90_RNASeq_genes_expressed.csv')

cell_line = '16HBE'
path = paths[cell_line]

df=pd.read_excel(path+'gene_count.xlsx')
df_group=pd.read_excel(path+'gene_fpkm_group.xlsx')

zero_count_genes=df[(df['Sigma16HBE_1']==0) & (df['Sigma16HBE_2']==0) & (df['Sigma16HBE_2']==0)]['gene_id']

plt.figure(figsize=(8,4))
plt.title('16HBE RNASeq FPKM distribution', fontsize=16)
plt.xlabel('$Log_2(FPKM)$',fontsize=16)
plt.ylabel('count',fontsize=16)
plt.vlines(x=expression_threshold, ymin=0,ymax=5000,color='red', label='expression threshold=%f'%expression_threshold)
plt.hist(np.log2(df_group[~df_group.geneID.isin(zero_count_genes)]['Sigma16HBE']+1),bins=100,log=True)
plt.legend(fontsize=14)

plt.savefig('CR_outputs/RNASeq_16HBE.png')

df_group[(~df_group.geneID.isin(zero_count_genes)) & (df_group['Sigma16HBE']>=expression_threshold  )]['geneID'].to_csv('16HBE_RNASeq_genes_expressed.csv')
