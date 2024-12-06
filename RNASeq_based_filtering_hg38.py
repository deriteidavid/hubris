import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 

df_tpm_hg38=pd.read_csv('RNA_Seq_hg38/salmon.merged.gene_tpm.tsv',sep='\t')
df_tpm_hg38['IMR90hTERT'] = df_tpm_hg38[['IMR90hTERT_1','IMR90hTERT_2','IMR90hTERT_3']].mean(axis=1)
df_tpm_hg38['Sigma16HBE'] = df_tpm_hg38[['Sigma16HBE_2', 'Sigma16HBE_1', 'Sigma16HBE_3']].mean(axis=1)
#ENSG00000000003.16 --> ENSG00000000003
df_tpm_hg38['geneID']= df_tpm_hg38.apply(lambda row: row['gene_id'].split('.')[0],axis=1)

expression_threshold = 0.5

df_tpm_hg38[df_tpm_hg38['IMR90hTERT']>=expression_threshold]['geneID'].to_csv('RNASeq_lists/IMR90_RNASeq_genes_expressed.csv')
df_tpm_hg38[df_tpm_hg38['Sigma16HBE']>=expression_threshold]['geneID'].to_csv('RNASeq_lists/16HBE_RNASeq_genes_expressed.csv')

import seaborn as sns
fig, axs = plt.subplots(2,1, sharex=True,constrained_layout=True)
axs[0].set_title('Cell line: IMR90')
axs[0].hist(np.log2(df_tpm_hg38['IMR90hTERT']+1), bins=100,log=True)
axs[0].set_xlabel('$Log_2(TPM + 1)$',fontsize=12)
axs[0].set_ylabel('count',fontsize=12)
axs[0].vlines(x=expression_threshold,ymin=0, ymax = np.histogram(np.log2(df_tpm_hg38['IMR90hTERT']+1),bins=100)[0][0],color='red', label = f'expression threshold = {expression_threshold:.2f}')
axs[0].legend()

axs[1].set_title('Cell line: 16HBE')
axs[1].hist(np.log2(df_tpm_hg38['Sigma16HBE']+1), bins=100,log=True)
axs[1].set_xlabel('$Log_2(TPM + 1)$',fontsize=12)
axs[1].set_ylabel('count',fontsize=12)
axs[1].vlines(x=expression_threshold,ymin=0, ymax = np.histogram(np.log2(df_tpm_hg38['Sigma16HBE']+1),bins=100)[0][0],color='red', label = f'expression threshold = {expression_threshold:.2f}')
axs[1].legend()

plt.legend()
sns.despine()

plt.savefig('CR_outputs/RNASeq_distribution.png')

