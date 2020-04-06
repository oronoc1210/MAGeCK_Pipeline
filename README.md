# Starting materials

To start with, I was shared:
1. "all_YL_gRNA_seq&locusID.xlsx" (here renamed to **gRNA_sequences.xlsx**)
2. "File 15 All Genes with GI and Accession.xlsx" (here renamed to **all_genes_with_GI_and_Accession.xlsx**)
3. "journal.pone.0162363.s004.XLSX" (here renamed to **gene_data.xlsx**)

The original files are contained in the google drive folder:
Shared with me > CRISPR screen analysis > Yarrowia_pilot_project_021920 > Yarrowia inputs

# Creating inputs

MAGeCK requires a table of gRNAs with three columns: gRNA ID, Locus ID, and gRNA sequence.
Since the gRNAs themselves didn't have IDs, I used the script **create_lib_file.py** to 
take the two column table **gRNA_sequences.xlsx** and add an ordinal gRNA ID column.
This new file is called **grna_to_locus_lib.txt**.

For my own purposes later down the line, I also wanted to combine all of the relevant data from the three given tables into one.
For this I used **create_reference_table.py** to create one master table called **gRNA_sequence_to_locus.xlsx**,
containing columns for gRNA sequence, Locus ID, Gene Type, Chromosome, Start base, End base, and Strand.

# MAGeCK command

In each of Days 2, 4, and 6 I wanted to calculate the FS (fitness score -- how harmful a CRISPR indel was to cell growth),
and the CS (cutting score -- how efficient a gRNA was at inducing a DNA double strand break).
FS is calculated with the log2 ratio of cas9 libraries over control,
and CS is calculated with the log2 ratio of cas9-ku70 libraries over control.

I used two sequential MAGeCK commands, both contained in *Day2/day2_fs_mageck_cmd.sh*. 
The first, mageck count, takes the grna_to_locus_lib and fastq files as input, and produces a count table 
of all the counts of each gRNA for each library -- *Day2/Day2.count.txt*.
The second, mageck test, takes the count table from the first command and performs statistical analysis 
to obtain a ranking by significance at the gene (**Day2/Day2_test.gene_summary.txt**)
and sgRNA (**Day2/Day2_test.sgrna_summary.txt**) level. These tables contain the log2 ratios between treatment and control 
for genes and sgRNAs respectively.

# post-MAGeCK 

Each of the barcode counts and log2 ratios for FS and CS for Days 2, 4, and 6 are contained in different tables, 
as each of the six combinations needed individual MAGeCK commands. So first I used
**combine_tables.py** to join all of the scores into two tables -- one for genes
(**gene_summaries.xlsx**) and one for sgRNAs (**sgrna_counts_and_lfc.xlsx**).

## visualization

Lastly, **fs_to_bed.py** was used to create bedfiles for viewing in IGV which highlight genes by fitness score.
The bedfile and preview images are available in the google drive above.
