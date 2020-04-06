#!/bin/sh

mageck count -l ../grna_to_locus_lib.txt -n Day2_CS \
             --sample-label PO1f_1,PO1f_2,PO1f_3,PO1f_Cas9_ku70_1,PO1f_Cas9_ku70_2,PO1f_Cas9_ku70_3 \
             --fastq PO1f_1_d2.fastq PO1f_2_d2.fastq PO1f_3_d2.fastq \
                     PO1f_Cas9_ku70_1_d2.fastq PO1f_Cas9_ku70_2_d2.fastq PO1f_Cas9_ku70_3_d2.fastq \
                     
mageck test -k Day2_CS.count.txt -t PO1f_Cas9_ku70_1,PO1f_Cas9_ku70_2,PO1f_Cas9_ku70_3 \
            -c PO1f_1,PO1f_2,PO1f_3 -n Day2_CS_test

