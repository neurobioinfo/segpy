import os 
import pandas as pd
import numpy as np 

from pyspark.sql import SparkSession
import pyspark as spark
import pyspark
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType
from pyspark.sql.types import ArrayType
from pyspark.sql.types import IntegerType

import pyspark.sql.functions as F
import pyspark.sql.types as T


#### Just segregation
def segrun_family_wise(mt, ped, outfolder,hl):
    glb_aff=[ x for x in ped.loc[ped.loc[:,'phenotype']==2,'individualid']]
    glb_naf=[ x for x in ped.loc[ped.loc[:,'phenotype']==1,'individualid']]
    fam_list=ped.loc[:,'familyid'].unique()
    fam1=fam11=fam12={}
    for i in fam_list:
        fam1[i]=[ x for x in ped.loc[ped.loc[:,'familyid']==i,'individualid']]
    # wildtype 
    mt = mt.annotate_entries(wild = mt.GT.is_hom_ref())
    # no call
    mt = mt.annotate_entries(ncl = hl.is_missing(mt.GT))
    # variant 
    mt = mt.annotate_entries(vrt = mt.GT.is_het())
    # hom_var: contains identical alternate alleles
    mt = mt.annotate_entries(homv = mt.GT.is_hom_var())
    # altaf: contains  ALT allele frequency   
    mt = mt.annotate_rows(altaf = (hl.agg.call_stats(mt.GT, mt.alleles).AF[1]))
    # listt0=[]
    # listt0.append('locus')
    # listt0.append('alleles')
    name0=f'{outfolder}/temp/locus_alleles.csv'
    mt.rows().select('altaf').export(name0, delimiter='\t')
    cmd_glb_csq=f'cd {outfolder}/temp ; cut -d\'\t\' -f 1-2 locus_alleles.csv> temp.csv ; mv  temp.csv  locus_alleles.csv'
    os.system(cmd_glb_csq)  
    #############
    #############
    # glb aff
    glb_aff_sam = hl.literal(hl.set(glb_aff))
    glb_aff_sam_mt=mt.filter_cols(glb_aff_sam.contains(mt.s))
    glb_aff_sam_mt.count()
    # Global 
    ## wildtype 
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_wild = hl.agg.sum(glb_aff_sam_mt.wild))
    # no call
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_ncl = hl.agg.sum(glb_aff_sam_mt.ncl))
    # variant 
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_vrt = hl.agg.sum(glb_aff_sam_mt.vrt))
    # hom_var: contains identical alternate alleles
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_homv = hl.agg.sum(glb_aff_sam_mt.homv))
    # altaf: contains  ALT allele frequency   
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_altaf = (hl.agg.call_stats(glb_aff_sam_mt.GT, glb_aff_sam_mt.alleles).AF[1]))
    listt2=[]
    # listt2.append('locus')
    # listt2.append('alleles')
    name2=f'{outfolder}/temp/glb_aff.csv'
    listt2=['glb_aff_wild','glb_aff_ncl','glb_aff_vrt','glb_aff_homv','glb_aff_altaf']
    glb_aff_sam_mt.rows().select(*listt2).export(name2, delimiter='\t')
    #############
    #############
    # glb_aff
    glb_naf_sam = hl.literal(hl.set(glb_naf))
    glb_naf_sam_mt=mt.filter_cols(glb_naf_sam.contains(mt.s))
    glb_naf_sam_mt.count()
    #############
    ## wildtype 
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_wild = hl.agg.sum(glb_naf_sam_mt.wild))
    # no call
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_ncl = hl.agg.sum(glb_naf_sam_mt.ncl))
    # variant 
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_vrt = hl.agg.sum(glb_naf_sam_mt.vrt))
    # hom_var: contains identical alternate alleles
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_homv = hl.agg.sum(glb_naf_sam_mt.homv))
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_altaf = (hl.agg.call_stats(glb_naf_sam_mt.GT, glb_naf_sam_mt.alleles).AF[1]))
    listt3=[]
    # listt2.append('locus')
    # listt2.append('alleles')
    listt3=['glb_naf_wild','glb_naf_ncl','glb_naf_vrt','glb_naf_homv','glb_naf_altaf']
    name3=f'{outfolder}/temp/glb_naf.csv'
    glb_naf_sam_mt.rows().select(*listt3).export(name3, delimiter='\t')
    cmd00=f'cd {outfolder}/temp ; cut -d\'\t\' -f 3- glb_naf.csv > temp.csv ; mv  temp.csv  glb_naf.csv'
    os.system(cmd00)
    cmd00=f'cd {outfolder}/temp ; cut -d\'\t\' -f 3- glb_aff.csv > temp.csv ; mv  temp.csv  glb_aff.csv'
    os.system(cmd00)
    for i in fam_list:
        #Whole family
        listt1=[]
        fam1[i]=[ x for x in ped.loc[ped.loc[:,'familyid']==i,'individualid']]
        fam_sam = hl.literal(hl.set(fam1[i]))
        fam_sam_mt=mt.filter_cols(fam_sam.contains(mt.s))
        fam_sam_mt = fam_sam_mt.annotate_rows(familyid = i)
        listt1.append(f'familyid')
        fam_sam_mt = fam_sam_mt.annotate_rows(samples = fam1[i])
        listt1.append(f'samples')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
        fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild'})
        listt1.append(f'fam_wild')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
        fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl'})
        listt1.append(f'fam_ncl')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
        fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt'})
        listt1.append(f'fam_vrt')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
        fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv'})
        listt1.append(f'fam_homv')
        name1=f'{outfolder}/temp/fam_{i}.csv'
        fam_sam_mt.rows().select(*listt1).export(name1, delimiter='\t')
        cmd0=f'cd {outfolder}/temp ;  cut -d " " -f 3- fam_{i}.csv > temp.csv ; mv  temp.csv  fam_{i}.csv'
        os.system(cmd0)
        # Affected memeber
        listt1=[]
        fam12[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        fam_sam2 = hl.literal(hl.set(fam12[i]))
        fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
        fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff = fam12[i])
        listt1.append(f'sample_aff')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
        fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff'})
        listt1.append(f'fam_wild_aff')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
        fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff'})
        listt1.append(f'fam_ncl_aff')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
        fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff'})
        listt1.append(f'fam_vrt_aff')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
        fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff'})
        listt1.append(f'fam_homv_aff')
        name1=f'{outfolder}/temp/fam_{i}_aff.csv'
        fam_sam_mt.rows().select(*listt1).export(name1, delimiter='\t')
        cmd0=f'cd {outfolder}/temp ;  cut -d " " -f 3- fam_{i}_aff.csv > temp.csv ; mv  temp.csv  fam_{i}_aff.csv'
        os.system(cmd0)
        # unaffected
        listt1=[]
        fam11[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==1),'individualid']]
        fam_sam1 = hl.literal(hl.set(fam11[i]))
        fam_sam_mt=mt.filter_cols(fam_sam1.contains(mt.s))
        fam_sam_mt = fam_sam_mt.annotate_rows(sample_naf = fam12[i])
        listt1.append(f'sample_naf')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
        fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_naf'})
        listt1.append(f'fam_wild_naf')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
        fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_naf'})
        listt1.append(f'fam_ncl_naf')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
        fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_naf'})
        listt1.append(f'fam_vrt_naf')
        fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
        fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_naf'})
        listt1.append(f'fam_homv_naf')
        name1=f'{outfolder}/temp/fam_{i}_naf.csv'
        fam_sam_mt.rows().select(*listt1).export(name1, delimiter='\t')
        cmd0=f'cd {outfolder}/temp ;  cut -d " " -f 3- fam_{i}_naf.csv > temp.csv ; mv  temp.csv  fam_{i}_naf.csv'
        os.system(cmd0)
        cmd_all=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_naf.csv glb_aff.csv fam_{i}.csv fam_{i}_aff.csv fam_{i}_naf.csv > fam_{i}_all.csv'
        os.system(cmd_all)
        cmd_rm=f'cd {outfolder}/temp ;rm fam_{i}.csv fam_{i}_aff.csv fam_{i}_naf.csv'
        os.system(cmd_rm)   
    outputfile='finalseg.csv'
    cmd_head=f'cd {outfolder}/temp ; head -1 fam_{i}_all.csv > {outputfile}'
    os.system(cmd_head)
    for i in fam_list:
        cmd_rem0=f'cd {outfolder}/temp ;  sed -i 1d fam_{i}_all.csv ; cat fam_{i}_all.csv >> {outputfile}'
        os.system(cmd_rem0)
    cmd_rmall=f'cd {outfolder}/temp ;rm locus_alleles.csv glb_naf.csv glb_aff.csv fam_*.csv'
    os.system(cmd_rmall)
    cmd_header=f'cd {outfolder}/temp; head -1  finalseg.csv > header.txt'
    os.system(cmd_header)
    cmd_final=f'mv {outfolder}/temp/header.txt {outfolder}/; mv {outfolder}/temp/finalseg.csv.txt {outfolder}/; rm -r {outfolder}/temp'
    os.system(cmd_final)


