import networkx as nx
import glob

if ('CR_outputs/G_hubris_seleted_sp_cell_type_16HBE_crapome_1_expression_1.graphml' in glob.glob('CR_outputs/*')) and ('CR_outputs/G_hubris_seleted_sp_cell_type_IMR90_crapome_1_expression_1.graphml' in glob.glob('CR_outputs/*')):
    print('Generating merged sp figure from the individual cell line data')    
    g16hbe = nx.read_graphml('CR_outputs/G_hubris_seleted_sp_cell_type_16HBE_crapome_1_expression_1.graphml')
    gimr90 = nx.read_graphml('CR_outputs/G_hubris_seleted_sp_cell_type_IMR90_crapome_1_expression_1.graphml')
    G_hubris_seleted_sp = nx.compose_all([g16hbe,gimr90])
    nx.write_graphml(G_hubris_seleted_sp, 'CR_outputs/G_hubris_seleted_sp_merged_crapome_1_expression_1.graphml')
else:
    print('Necessary files not found. Please run "shorthest_path_analysis.py IMR90 1 1" and "shorthest_path_analysis.py 16HBE 1 1" first so the necessary input graphs are generated.')

