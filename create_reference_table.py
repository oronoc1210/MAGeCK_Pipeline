import sys
import os

import pandas as pd

def check_excel():
    for filename in os.listdir(os.getcwd()):
        if '.xlsx' in filename:
            df = pd.read_excel(filename)
            print(filename)
            print(df.head())
            print('\n\n')

def main():
    gene_df = pd.read_excel('gene_data.XLSX')
    sequence_df = pd.read_excel('gRNA_sequences.xlsx')
    data_matrix = []
    column_names = ['gRNA Sequence', 'Locus ID', 'Gene type', 'Chromosome', 'Start base', 'End base', 'Strand']
    count = 0
    for ix, row in sequence_df.iterrows():
        count += 1
        if count % 1000 == 0:
            print('Processed {} lines'.format(count))
        sequence = row['gRNA sequence']
        locus_id = row['Locus ID']
        if locus_id == 'Nontargeting':
            data_entry = [sequence, locus_id, 'n/a', 'n/a', 'n/a', 'n/a', 'n/a']
            data_matrix.append(data_entry)
            continue
        gene_info = gene_df.loc[gene_df['YALI1 Locus ID'] == locus_id].squeeze()
        gene_type = gene_info['Gene Type']
        chromosome = gene_info['Chromosome']
        start = gene_info['Start Base']
        end = gene_info['End Base']
        strand = gene_info['Strand']
        data_entry = [sequence, locus_id, gene_type, chromosome, start, end, strand]
        data_matrix.append(data_entry)
    output_df = pd.DataFrame(data_matrix, columns=column_names)
    output_df = output_df.sort_values(by='Locus ID')
    output_df.to_excel('gRNA_sequence_to_locus.xlsx', index=False)
	    
if __name__ == '__main__':
    main()
