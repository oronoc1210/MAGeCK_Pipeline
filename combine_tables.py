import sys
import os
import glob

import pandas as pd
import numpy as np

def merge_count_tables():
    final_df = None
    for filename in glob.glob('Day*/*.count.txt'):
        print("Processing {}...".format(filename))
        df = pd.read_table(filename)
        day = filename[:5].replace('Day','d')
        no_append = ['sgRNA', 'Gene']
        df.columns = [day + str(col) if col not in no_append else str(col) for col in df.columns]
        if not isinstance(final_df, pd.DataFrame):
            final_df = df
            continue
        common_columns = list(set(final_df.columns) & set(df.columns))
        final_df = pd.merge(final_df, df, how='left', on=common_columns)
    print(final_df)
    print(final_df.columns)
    sorted_columns = ['sgRNA', 'Gene'] + sorted([x for x in final_df.columns if x.startswith('d')])
    print(sorted_columns)
    final_df = final_df[sorted_columns]
    final_df.to_excel("barcode_counts.xlsx")


def merge_sgrna_summaries(final_df):
    starting_column_names = list(final_df.columns)
    new_column_names = []
    for filename in glob.glob('Day*/*.sgrna_summary.txt'):
        print("Processing {}...".format(filename))
        day = filename[:5].replace('Day','d')
        if 'CS' in filename:
            score_type = 'CS'
        else:
            score_type = 'FS'
        score_column_name = day + score_type
        df = pd.read_table(filename)
        df = df.filter(['sgrna', 'LFC'])
        df = df.rename({'LFC': score_column_name,
                        'sgrna': 'sgRNA'}, axis=1)
        new_column_names.append(score_column_name)
        final_df = pd.merge(final_df, df, how='left', on=['sgRNA'])
    print(final_df.columns)
    sorted_columns = starting_column_names + sorted(new_column_names)
    final_df = final_df[sorted_columns]
    print(final_df.columns)
    return(final_df)


def merge_gene_summaries():
    final_df = None
    for filename in glob.glob('Day*/*.gene_summary.txt'):
        print("Processing {}...".format(filename))
        day = filename[:5].replace('Day','d')
        if 'CS' in filename:
            score_type='CS'
        else:
            score_type='FS'
        score_column_name = day + score_type
        df = pd.read_table(filename)
        df = df.filter(['id', 'neg|lfc'])
        df = df.rename({'neg|lfc': score_column_name,
                        'id': 'Gene ID'}, axis=1)
        if not isinstance(final_df, pd.DataFrame):
            final_df = df
            continue
        final_df = pd.merge(final_df, df, how='left', on='Gene ID')
    sorted_columns = ['Gene ID'] + sorted([x for x in final_df.columns if x.startswith('d')])
    final_df = final_df[sorted_columns]
    print(final_df)
    final_df.to_excel("Gene_summaries.xlsx")


def make_sgrna_table():
    final_df = merge_count_tables()
    final_df = pd.read_excel('barcode_counts.xlsx')
    final_df = merge_sgrna_summaries(final_df)
    final_df = final_df.sort_values('sgRNA')
    print(final_df)
    print("Writing to excel...")
    final_df.to_excel("sgrna_counts_and_lfc.xlsx")


def main():
    #make_sgrna_table()
    merge_gene_summaries()

if __name__ == '__main__':
    main()
