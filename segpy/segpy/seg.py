"""
# Copyright belong MNI BIOINFO CORE (https://github.com/neurobioinfo)
# The pipeline is scripted\developed by Saeid Amiri (saeid.amiri@mcgill.ca)
"""

import os
import pandas as pd
import sys 

from segpy.segrun.segrun_family_wise_whole import segrun_family_wise_whole
from segpy.segrun.segrun_family_wise_whole_multiple import segrun_family_wise_whole_multiple
def run(mt, ped, outfolder, hl, vcffile, CSQ, affecteds_only, filter_variant, retrieve_sample_id, ncol, ana_mode):
    """
    mt: a hail MatrixTable object, passed to this function by step2.py
    ped: a pedigree file, this should file includes six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`, `phenotype`, plus a header with those exact column names
    outfolder: the folder that you want to save your output.
    hl: the hail module, passed to this script by step2.py and passed on to segrun_family_wise_whole to save loading time
    vcffile: the annotated vcf file
    affecteds_only: if a family has >0 samples with phenotype=2 (affected), then we want to process only variants found in those samples in that family [default behaviour]
    """
    # os.chdir(outfolder)
    # CSQ=eval(str(str(CSQ)))
    if CSQ == "TRUE":
        try:
            ext = vcffile.split('.')[-1]
            prog = 'zcat' if ext == 'gz' or ext == 'bgz' else 'cat'
            cmd0 = f'{prog} {vcffile}|head -10000|grep "##INFO=<ID=CSQ"'
            csqlabel=os.popen(cmd0).read().split("Format: ")[1].split('">')[0].split('|')
            csqlabel=[el+'_csq' for el in csqlabel]
            print("Segpy is processing on VCF with a CSQ annotation.")  
        except IndexError as e:
            print("Error: Segpy can not exctract CSQ annotation from VCF")
    else:
        print("Segpy is processing on VCF without a CSQ annotation.")
        csqlabel=False
    if ana_mode != "multiple":
        segrun_family_wise_whole(mt, ped, outfolder, hl, csqlabel, affecteds_only, filter_variant, retrieve_sample_id, ncol)
    else:
        segrun_family_wise_whole_multiple(mt, ped, outfolder, hl, csqlabel, affecteds_only, filter_variant, retrieve_sample_id, ncol)
if __name__ == "__main__":
    run()
