import sys
import os
import glob

import pandas as pd
import numpy as np


def test_excel(excel_table):
    df = pd.read_excel(excel_table)
    print(df.columns)
    print(df)


def merge_features_and_scores(f_df, s_df):
    d6fs_s_df = s_df.filter(['Gene ID', 'd6_FS'])
    f_df = f_df.drop(columns=['YALI0 locus ID', 'Annotation'])
    merged_df = pd.merge(f_df, d6fs_s_df, how='left', left_on='YALI1 Locus ID', right_on='Gene ID').dropna()
    return merged_df

def value_to_color(FS, min_FS, max_FS):
# fitness scores to color
# from red (230, 25, 75) to grey (128,128,128) for negative max to 0
# from grey (128, 128, 128) to green (60, 180, 75) for 0 to positive max
    if FS == 0:
        rgb = (128, 128, 128)
        return rgb
    if FS < 0:
        r1, g1, b1 = 230, 25, 75
        r2, g2, b2 = 128, 128, 128
    if FS > 0:
        r1, g1, b1 = 128, 128, 128
        r2, g2, b2 = 60, 180, 75
    r = int(round((FS - min_FS)/(max_FS - min_FS)*r1 + (1-(FS-min_FS)/(max_FS-min_FS))*r2))
    g = int(round((FS - min_FS)/(max_FS - min_FS)*g1 + (1-(FS-min_FS)/(max_FS-min_FS))*g2))
    b = int(round((FS - min_FS)/(max_FS - min_FS)*b1 + (1-(FS-min_FS)/(max_FS-min_FS))*b2))
    rgb = (r, g, b)
    return rgb

def add_color_to_df(merged_df):
    min_fs = merged_df['d6_FS'].min()
    max_fs = merged_df['d6_FS'].max()
    merged_df['fs_color'] = merged_df.apply(lambda x: value_to_color(x['d6_FS'], min_fs, max_fs), axis=1)
    return merged_df

def color_df_to_bed(color_df, Y_2_chr):

    with open('YALI1_fs_color.bed', 'w+') as outf:
        for ix, row in color_df.iterrows():
            data = [Y_2_chr[row['Chromosome']], row['Start Base'], row['End Base'],
                    row['YALI1 Locus ID'], 0, row['Strand'], row['Start Base'],
                    row['End Base'], ','.join(map(str, row['fs_color']))]
            line = '\t'.join(map(str, data)) + '\n'
            outf.write(line)

def value_to_bedgraph(merged_df, Y_2_chr):
    with open("YALI1_fs.bedgraph", 'w+') as outf:
        outf.write('track type=bedGraph name="Yarrowia gene fitness scores" ')
        outf.write('visibility=full color=60,180,75 altColor=230,25,75\n')
        for ix, row in merged_df.iterrows():
            data = [Y_2_chr[row['Chromosome']], row['Start Base'], row['End Base'],
                    row['d6_FS']]
            line = '\t'.join(map(str, data)) + '\n'
            outf.write(line)

def main():
    # YALI name to actual chromosome name in fastq
    Y_2_chr = {'YALI1A': 'CP0_17553',
               'YALI1B': 'CP0_17554',
               'YALI1C': 'CP0_17555',
               'YALI1D': 'CP0_17556',
               'YALI1E': 'CP0_17557',
               'YALI1F': 'CP0_17558'}
    feature_df = pd.read_excel('gene_data.xlsx')
    score_df = pd.read_excel('gene_summaries.xlsx')
    merged_df = merge_features_and_scores(feature_df, score_df)
    # Making the bedgraph
    value_to_bedgraph(merged_df, Y_2_chr)
    # Making the color gradient bed file
    '''
    color_df = add_color_to_df(merged_df)
    color_df.to_excel('gene_data_plus_colors.xlsx')
    color_df_to_bed(color_df, Y_2_chr)
    '''

if __name__ == '__main__':
    main()
