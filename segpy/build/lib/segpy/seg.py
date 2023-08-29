"""
# Copyright belong MNI BIOINFO CORE (https://github.com/neurobioinfo)
# The pipeline is written by Saeid Amiri (saeid.amiri@mcgill.ca)
"""

import os 
import pandas as pd
import numpy as np 

# from pyspark.sql import SparkSession
# import pyspark as spark
# import pyspark
# from pyspark.sql.functions import udf
# from pyspark.sql.types import StructType
# from pyspark.sql.types import ArrayType
# from pyspark.sql.types import IntegerType

# import pyspark.sql.functions as F
# import pyspark.sql.types as T

# from segpy.segrun.segrun_family_wise_CSQ_genotype_sole  import segrun_family_wise_CSQ_genotype_sole
# from segpy.segrun.segrun_family_wise_CSQ_genotype_more  import segrun_family_wise_CSQ_genotype_more
# from segpy.segrun.segrun_family_wise_genotype_sole  import segrun_family_wise_genotype_sole
# from segpy.segrun.segrun_family_wise_genotype_more  import segrun_family_wise_genotype_more


from segpy.segrun.segrun_family_wise_withoutCSQ_genotype_sole import segrun_family_wise_withoutCSQ_genotype_sole
from segpy.segrun.segrun_family_wise_withoutCSQ_genotype_more import segrun_family_wise_withoutCSQ_genotype_more
from segpy.segrun.segrun_family_wise_withCSQ_genotype_sole    import segrun_family_wise_withCSQ_genotype_sole
from segpy.segrun.segrun_family_wise_withCSQ_genotype_more    import segrun_family_wise_withCSQ_genotype_more



# def run(mt, ped, outfolder,hl,ncol=7, *vcffile):
#     """
#     mt: the matrix table generated by Hail 
#     ped: a pedigree file, this should file includes six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex` 
#     outfolder: the folder that you want to save your output 
#     hl: the breif of Hail
#     vcffile: The annotated vcf file with VEP.  
#     """
#     if (vcffile is not None) and (len(vcffile) >= 1) :
#         vcffile1=vcffile[0]
#         cmd0=f'grep "##INFO=<ID=CSQ"  {vcffile1}'
#         csqlabel=os.popen(cmd0).read().split("Format: ")[1].split('">')[0].split('|')
#         csqlabel=[el+'_csq' for el in csqlabel]
#         print("Segpy is using VCF with CSQ")   
#         cmd_temp=f'cd {outfolder} ; mkdir -p temp'
#         os.system(cmd_temp)     
#         if len(pd.unique(ped.loc[:,'phenotype']))==1:
#             print("Segpy is running on data with sole phenotype ")
#             segrun_family_wise_CSQ_genotype_sole(mt, ped, outfolder,hl, ncol,csqlabel)
#         else:    
#             print("Segpy is running on data with different phenotypes")
#             segrun_family_wise_CSQ_genotype_more(mt, ped, outfolder,hl, ncol,csqlabel)
#     else:
#         print("Segpy is running on data withOUT CSQ")
#         if len(pd.unique(ped.loc[:,'phenotype']))==1:
#             print("Segpy is running on data with sole phenotype ")
#             segrun_family_wise_genotype_sole(mt, ped, outfolder,hl)
#         else:    
#             print("Segpy is running on data with different phenotypes")
#             segrun_family_wise_genotype_more(mt, ped, outfolder,hl) 



def run(mt,ped,outfolder,hl,vcffile,ncol=7,CSQ=True):
    """
    mt: the matrix table generated by Hail 
    ped: a pedigree file, this should file includes six columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex` 
    outfolder: the folder that you want to save your output 
    hl: the breif of Hail
    vcffile: The annotated vcf file with VEP.  
    """

    if eval(str(str(CSQ)))==True: 
        try:
            # parse CSQ from vcf/gvcf header, hard-coded to first 10k lines of file
            ext = vcffile.split('.')[-1]
            prog = 'zcat' if ext == 'gz' or ext == 'bgz' else 'cat'
            cmd0 = f'{prog} {vcffile}|head -10000|grep "##INFO=<ID=CSQ"'
            csqlabel=os.popen(cmd0).read().split("Format: ")[1].split('">')[0].split('|')
            csqlabel=[el+'_csq' for el in csqlabel]
            print("Segpy is using VCF with CSQ")  
            run_with_CSQ(mt, ped, outfolder,hl, ncol,csqlabel)
        except IndexError as e:
            print("Segpy is using VCF withOUT CSQ") 
            run_without_CSQ(mt, ped, outfolder,hl) 
    else:
            print("Segpy is using VCF withOUT CSQ") 
            run_without_CSQ(mt, ped, outfolder,hl) 



def run_with_CSQ(mt, ped, outfolder,hl, ncol,csqlabel):
        cmd_temp=f'cd {outfolder} ; mkdir -p temp'
        os.system(cmd_temp)     
        if len(pd.unique(ped.loc[:,'phenotype']))==1:
            print("Segpy is running on data with sole phenotype ")
            segrun_family_wise_withCSQ_genotype_sole(mt, ped, outfolder,hl, ncol,csqlabel)
        else:    
            print("Segpy is running on data with different phenotypes")
            segrun_family_wise_withCSQ_genotype_more(mt, ped, outfolder,hl, ncol,csqlabel) 

def run_without_CSQ(mt, ped, outfolder,hl):
        cmd_temp=f'cd {outfolder} ; mkdir -p temp'
        os.system(cmd_temp)     
        if len(pd.unique(ped.loc[:,'phenotype']))==1:
            print("Segpy is running on data with sole phenotype ")
            segrun_family_wise_withoutCSQ_genotype_sole(mt, ped, outfolder,hl)
        else:    
            print("Segpy is running on data with different phenotypes")
            segrun_family_wise_withoutCSQ_genotype_more(mt, ped, outfolder,hl) 


if __name__ == "__main__":
    run()