#!/bin/sh

mageck count -l ../grna_to_locus_lib.txt -n Day4_CS \
             --sample-label PO1f_1,PO1f_2,PO1f_3,PO1f_Cas9_ku70_1,PO1f_Cas9_ku70_2,PO1f_Cas9_ku70_3 \
             --fastq PO1f_1_d4.fastq PO1f_2_d4.fastq PO1f_3_d4.fastq \
                     PO1f_Cas9_ku70_1_d4.fastq PO1f_Cas9_ku70_2_d4.fastq PO1f_Cas9_ku70_3_d4.fastq \
                     
mageck test -k Day4_CS.count.txt -t PO1f_Cas9_ku70_1,PO1f_Cas9_ku70_2,PO1f_Cas9_ku70_3 \
            -c PO1f_1,PO1f_2,PO1f_3 -n Day4_CS_test

