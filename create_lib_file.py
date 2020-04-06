import sys
import os

import pandas as pd

def main():
    sequence_df = pd.read_excel('gRNA_sequences.xlsx')
    count=0
    with open('grna_to_locus_lib.txt', 'w+') as outf:
        for ix, row in sequence_df.iterrows():
            count += 1
            if count % 1000 == 0:
                print('Processed {} lines'.format(count))
            sequence = row['gRNA sequence']
            locus_id = row['Locus ID']
            outf.write('{}\t{}\t{}\n'.format(count, sequence, locus_id))
	    
if __name__ == '__main__':
    main()
