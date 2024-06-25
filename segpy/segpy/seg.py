"""
# Copyright belong MNI BIOINFO CORE (https://github.com/neurobioinfo)
# The pipeline is developed by Saeid Amiri (saeid.amiri@mcgill.ca)
"""

import os
import pandas as pd

from segpy.segrun.segrun_family_wise_whole import segrun_family_wise_whole

def run(mt, ped, outfolder, hl, vcffile, CSQ=True, affecteds_only=True):
    """
    mt: a hail MatrixTable object, passed to this function by step2.py
    ped: a pedigree file, this should file includes six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`, `phenotype`, plus a header with those exact column names
    outfolder: the folder that you want to save your output.
    hl: the hail module, passed to this script by step2.py and passed on to segrun_family_wise_whole to save loading time
    vcffile: the annotated vcf file
    affecteds_only: if a family has >0 samples with phenotype=2 (affected), then we want to process only variants found in those samples in that family [default behaviour]
    """
    if eval(str(str(CSQ)))==True: 
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
            
    segrun_family_wise_whole(mt, ped, outfolder, hl, csqlabel, affecteds_only)

if __name__ == "__main__":
    run()
