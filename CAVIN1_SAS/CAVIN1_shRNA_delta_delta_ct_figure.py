import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df= pd.read_excel('CAVIN1_delta_delta_ct.xlsx')

plt.figure(figsize=(8,6))
plt.bar(range(len(df)),df['Delta delta Ct (estimate)'],yerr=df['Std Error'])
plt.xticks(range(len(df)),df['Gene'])
for i,p_value in enumerate(df['P-value']):
    if (float(p_value) <=0.05) and (float(p_value) >0.01):
        plt.text(x=i, y=df['Delta delta Ct (estimate)'][i]+df['Std Error'][i]+0.1, s="*", ha='center', va='center', fontsize=15)
    if (float(p_value) <=0.01):
        plt.text(x=i, y=df['Delta delta Ct (estimate)'][i]+df['Std Error'][i]+0.1, s="**", ha='center', va='center', fontsize=15)
plt.ylabel('Delta Delta Ct')
sns.despine()

plt.savefig('CAVIN1_delta_delta_ct.png',dpi=600)
plt.savefig('CAVIN1_delta_delta_ct.pdf')

