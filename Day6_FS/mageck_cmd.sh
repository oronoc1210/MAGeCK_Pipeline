#!/bin/sh

mageck count -l ../grna_to_locus_lib.txt -n Day6 \
             --sample-label PO1f_1,PO1f_2,PO1f_3,PO1f_Cas9_1,PO1f_Cas9_2,PO1f_Cas9_3 \
             --fastq PO1f_1_d6.fastq PO1f_2_d6.fastq PO1f_3_d6.fastq \
                     PO1f_Cas9_1_d6.fastq PO1f_Cas9_2_d6.fastq PO1f_Cas9_3_d6.fastq \
                     
mageck test -k Day6.count.txt -t PO1f_Cas9_1,PO1f_Cas9_2,PO1f_Cas9_3 \
            -c PO1f_1,PO1f_2,PO1f_3 -n Day6_test

