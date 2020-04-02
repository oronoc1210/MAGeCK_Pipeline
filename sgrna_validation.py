import sys
import os
import glob

import pandas as pd
import numpy as np


def cutting_validation(df, stats):
    # inactive: 2 or more
    # poor: -1 to 2
    # moderate: -5 to -1
    # good: -5 or less
    nt_df = df.loc[df['Gene'] == 'Nontargeting']
    nt_sgrnas = list(nt_df['sgRNA'].values)
    # Day 4
    # inactive
    d4_inactive_df = df.loc[df['d4_CS'] >= 2]
    d4_inactive_sgrnas = list(d4_inactive_df['sgRNA'].values)
    write_sgrnas(d4_inactive_sgrnas, 'd4_inactive_sgrnas.txt')
    # poor
    d4_poor_df = df.loc[(df['d4_CS'] < 2) & (df['d4_CS'] >= -1)]
    d4_poor_sgrnas = list(d4_poor_df['sgRNA'].values)
    write_sgrnas(d4_poor_sgrnas, 'd4_poor_sgrnas.txt')
    # moderate
    d4_moderate_df = df.loc[(df['d4_CS'] < -1) & (df['d4_CS'] >= -5)]
    d4_moderate_sgrnas = list(d4_moderate_df['sgRNA'].values)
    write_sgrnas(d4_moderate_sgrnas, 'd4_moderate_sgrnas.txt')
    # good
    d4_good_df = df.loc[df['d4_CS'] < -5]
    d4_good_sgrnas = list(d4_good_df['sgRNA'].values)
    write_sgrnas(d4_good_sgrnas, 'd4_good_sgrnas.txt')

    # Day5
    # inactive
    d6_inactive_df = df.loc[df['d6_CS'] >= 2]
    d6_inactive_sgrnas = list(d6_inactive_df['sgRNA'].values)
    write_sgrnas(d6_inactive_sgrnas, 'd6_inactive_sgrnas.txt')
    # poor
    d6_poor_df = df.loc[(df['d6_CS'] < 2) & (df['d6_CS'] >= -1)]
    d6_poor_sgrnas = list(d6_poor_df['sgRNA'].values)
    write_sgrnas(d6_poor_sgrnas, 'd6_poor_sgrnas.txt')
    # moderate
    d6_moderate_df = df.loc[(df['d6_CS'] < -1) & (df['d6_CS'] >= -5)]
    d6_moderate_sgrnas = list(d6_moderate_df['sgRNA'].values)
    write_sgrnas(d6_moderate_sgrnas, 'd6_moderate_sgrnas.txt')
    # good
    d6_good_df = df.loc[df['d6_CS'] < -5]
    d6_good_sgrnas = list(d6_good_df['sgRNA'].values)
    write_sgrnas(d6_good_sgrnas, 'd6_good_sgrnas.txt')

    compare_days('inactive', d4_inactive_sgrnas, d6_inactive_sgrnas, nt_sgrnas, stats)
    compare_days('poor', d4_poor_sgrnas, d6_poor_sgrnas, nt_sgrnas, stats)
    compare_days('moderate', d4_moderate_sgrnas, d6_moderate_sgrnas, nt_sgrnas, stats)
    compare_days('good', d4_good_sgrnas, d6_good_sgrnas, nt_sgrnas, stats)

    genes_with_no_sgrnas(df, 'd4', stats)
    genes_with_no_sgrnas(df, 'd6', stats)

def compare_days(quality, d4_sgrnas, d6_sgrnas, nt_sgrnas, stats):
    with open(stats, 'a') as outf:
        outf.write('{} sgRNA stats:\n'.format(quality))
        # Day 4 num & pct nt
        outf.write('Day 4 {} sgRNAs: {}\n'.format(quality, len(d4_sgrnas)))
        d4_nt = len(set(nt_sgrnas) & set(d4_sgrnas))
        outf.write('Number Day 4 {} sgRNAs nontargeting: {}\n'.format(quality, d4_nt))
        # Day 6 num & pct nt
        outf.write('Day 6 {} sgRNAs: {}\n'.format(quality, len(d6_sgrnas)))
        d6_nt = len(set(nt_sgrnas) & set(d6_sgrnas))
        outf.write('Number Day 6 {} sgRNAs nontargeting: {}\n'.format(quality, d6_nt))
        # overlapping between Day 4 and Day 6
        overlapping_sgrnas = len(set(d4_sgrnas) & set(d6_sgrnas))
        outf.write('Number {} sgRNAs in both Day 4 and 6: {}\n\n'.format(quality, overlapping_sgrnas))

def genes_with_no_sgrnas(df, day, stats):
    total_count = 0
    # all sgrna inactive for the gene
    inactive_count = 0
    # all sgrna poor OR inactive, i.e. poor or less
    poor_count = 0
    # At least one good sgRNA for the gene
    good_count = 0
    for gene in df['Gene'].values:
        if gene == 'Nontargeting':
            continue
        total_count += 1
        gene_df = df.loc[df['Gene'] == gene]
        if (gene_df['{}_CS'.format(day)] >= 2).all():
            inactive_count += 1
        if (gene_df['{}_CS'.format(day)] >= -1).all():
            poor_count += 1
        if (gene_df['{}_CS'.format(day)] <= -5).any():
            good_count += 1
    i_pct = float(inactive_count) * 100 / float(total_count)
    p_pct = float(poor_count) * 100 / float(total_count)
    g_pct = float(good_count) * 100 / float(total_count)
    with open(stats, 'a') as outf:
        day = day.replace('d', 'Day ')
        outf.write('Number of genes in {} where all sgRNAs inactive: {} ({:0.2f}% of genes)\n'.format(day, inactive_count, i_pct))
        outf.write('Number of genes in {} where all sgRNAs inactive or poor: {:0.2f} ({:0.2f}% of genes)\n'.format(day, poor_count, p_pct))
        outf.write('Number of genes in {} where at least one good sgRNA: {} ({:0.2f}% of genes)\n\n'.format(day, good_count, g_pct))


def write_sgrnas(sgrnas, outname):
    with open('Validation_out/{}'.format(outname), 'w+') as outf:
        for sgrna in sgrnas:
            outf.write(str(sgrna) + '\n')


def print_stats():
    with open('Validation_out/sgrna_stats.txt') as outf:
        print(outf.read())

def main():
    df = pd.read_excel('sgrna_counts_and_lfc.xlsx')
    if not os.path.isdir('Validation_out'):
        os.mkdir('Validation_out')
    stats = 'Validation_out/sgrna_stats.txt'
    with open(stats, 'w+') as outf:
        outf.write("Total sgRNA: {}\n\n".format(len(df.index)))
    cutting_validation(df, stats)
    print_stats()



if __name__ == '__main__':
    main()
