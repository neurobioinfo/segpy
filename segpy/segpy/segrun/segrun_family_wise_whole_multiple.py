import pandas as pd
import hail as hl
from datetime import datetime
import gc
import logging
import itertools
import os
import sys
import subprocess
import io
import numpy as np
import pandas as pd 
import time

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType
from pyspark.sql.types import ArrayType
from pyspark.sql.types import IntegerType

import pyspark.sql.functions as F
import pyspark.sql.types as T
from segpy.tools.utils import str_list

####################
# HELPER FUNCTIONS #
# Multiple family
####################

# empty-aware filtering of MatrixTable based on a parent MT
def filterMatrixTableBySampleList(mt, family_list):
    if len(family_list) == 0:
        filterExpression = hl.literal(hl.empty_set(hl.tstr))
    else:
        filterExpression = hl.literal(hl.set(family_list))
    mt_filtered = mt.filter_cols(filterExpression.contains(mt.s))
    return mt_filtered

# generate wild/ncl/vrt/homv counts for one matrixTable
def generate_counts(mt, fam, sample_list):
    # will generate counting rows with generic names and append them to input mt
    # if sample_list is empty, simply pass mt through
    if len(sample_list) > 0:
        mt = mt.annotate_rows(  familyid = fam,
                                _wild = hl.agg.sum(mt.wild),
                                _ncl  = hl.agg.sum(mt.ncl),
                                _vrt  = hl.agg.sum(mt.vrt),
                                _homv = hl.agg.sum(mt.homv))
    else:
        mt = mt.annotate_rows(  familyid = fam,
                                _wild  = 0,
                                _ncl   = 0,
                                _vrt   = 0,
                                _homv  = 0)
    return mt

def export_counts(mt, prefix, outfile):
    counting_rows = ['_wild','_ncl','_vrt','_homv']
    mt.rows().select(*counting_rows).export(outfile, delimiter='\t')
    # rename headers to be prefix-specific
    cmd = f"sed '1!b; s/[^\t]\+/{prefix}&/g' {outfile} -i"
    os.system(cmd)

# generate wild/ncl/vrt/homv counts for one matrixTable for multiple family
def generate_counts_m(mt, fam, sample_list,ped):
    fam_aff=[ x for x in ped.loc[ped.loc[:,'familyid']==fam,'individualid']]
    aff_sam = hl.literal(hl.set(fam_aff))
    aff_sam2=mt.filter_cols(aff_sam.contains(mt.s))
    if len(sample_list) > 0:
        mt2 =  aff_sam2.annotate_rows(  familyid = fam,
                                glb_aff_r=fam_aff, 
                                _wild = hl.agg.sum(aff_sam2.wild),
                                _wild_c = hl.agg.collect(aff_sam2.wild),
                                _ncl  = hl.agg.sum(aff_sam2.ncl),
                                _ncl_c  = hl.agg.collect(aff_sam2.ncl),
                                _vrt  = hl.agg.sum(aff_sam2.vrt),
                                _vrt_c  = hl.agg.collect(aff_sam2.vrt),
                                _homv = hl.agg.sum(aff_sam2.homv),
                                _homv_c = hl.agg.collect(aff_sam2.homv))
    else:
        mt2 = aff_sam2.annotate_rows(familyid = fam,
                                _wild  = 0,
                                _wild_samp  = 0,
                                _ncl   = 0,
                                _ncl_samp   = 0,
                                _vrt   = 0,
                                _vrt_samp   = 0,
                                _homv  = 0,
                                _homv_samp  = 0)
    return mt2

def export_counts_m(mt2, prefix, outfile,sample_list,outfolder):
    if len(sample_list) > 0:
        listt2=['glb_aff_r','_wild','_wild_c','_ncl','_ncl_c','_vrt','_vrt_c','_homv','_homv_c']
        df3=mt2.rows().select(*listt2).to_spark()
        udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
        df4=df3.select('glb_aff_r','_wild','_wild_c',udf_i('_wild_c').alias('_wild_c2'),'_ncl','_ncl_c', udf_i('_ncl_c').alias('_ncl_c2'),'_vrt','_vrt_c',udf_i('_vrt_c').alias('_vrt_c2'),'_homv','_homv_c',udf_i('_homv_c').alias('_homv_c2'))
        del df3
        udf_2b = udf(lambda x,ref: [x[i] for i in ref])
        df5=df4.select('_wild',udf_2b('glb_aff_r','_wild_c2').alias('_wild_s'),'_ncl',udf_2b('glb_aff_r','_ncl_c2').alias('_ncl_s'),'_vrt',udf_2b('glb_aff_r','_vrt_c2').alias('_vrt_s'),'_homv',udf_2b('glb_aff_r','_homv_c2').alias('_homv_s'))
        str_udf = F.udf(str_list, T.StringType())
        df6=df5.select('_wild',str_udf('_wild_s').alias('_wild_samp'),'_ncl',str_udf('_ncl_s').alias('_ncl_samp'),'_vrt',str_udf('_vrt_s').alias('_vrt_samp'),'_homv',str_udf('_homv_s').alias('_homv_samp'))
        del df5
        name_glb_csv=f'{outfolder}/samp/fam_affcsv'
        df6.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name_glb_csv)
        del df6
        cmd_glb_aff0=f'cd {outfolder}/samp/fam_affcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} {outfolder}/samp/fam_aff_out \; ; rm -r  {outfolder}/samp/fam_affcsv'
        os.system(cmd_glb_aff0)
        cmd_prune_glb=f'cd {outfolder}/samp;' + ' sed -i fam_aff_out -e \"s/\[\]/\[\\"\\"\]/g ; s/\[\'/\[\\"/g ;  s/\'\]/\\"\]/g ;  s/\'/\\"/g ; s/\[\]/\[\"\"\]/g \" '
        os.system(cmd_prune_glb)
        cmd_prune_glb_mv=f'mv {outfolder}/samp/fam_aff_out {outfile}'
        os.system(cmd_prune_glb_mv)
        cmd = f"sed '1!b; s/[^\t]\+/{prefix}&/g' {outfile} -i"
        os.system(cmd)
        cmd_paste = f'paste -d"\t" {outfolder}/out_locus {outfile} > {outfolder}/tempf; rm {outfile}; mv {outfolder}/tempf {outfile}'
        os.system(cmd_paste)
    else:
        counting_rows = ['_wild','_wild_samp','_ncl','_ncl_samp','_vrt','_vrt_samp','_homv','_homv_samp']
        mt2.rows().select(*counting_rows).export(outfile, delimiter='\t')
        # rename headers to be prefix-specific
        cmd = f"sed '1!b; s/[^\t]\+/{prefix}&/g' {outfile} -i"
        os.system(cmd)
        cmd = f'cut -f3- {outfile} > {outfolder}/tmp; mv {outfolder}/tmp {outfile}'
        os.system(cmd)
        cmd_paste = f'paste -d"\t" {outfolder}/out_locus {outfile} > {outfolder}/tempf; rm {outfile}; mv {outfolder}/tempf {outfile}'
        os.system(cmd_paste)


# os handling of per-family temp output files
def formatTmpCsv(name, tmpfolder='./temp'):
    cmd_check = f'[ ! -d {tmpfolder} ] && mkdir -p {tmpfolder}'
    os.system(cmd_check)
    tmp = f'{tmpfolder}/tmp'
    cmd = f'cut -f3- {name} > {tmp}; mv {tmp} {name}'
    os.system(cmd)

# timekeeping - using logging module
def timekeeping(tag, start):
    runtime = str(datetime.now()-start)
    logging.info('Runtime: %s\tStep: %s', runtime, tag)


def sample_retrieve(mt, ped, outfolder):
    cmd_samp_mkdir=f'mkdir {outfolder}/samp'
    os.system(cmd_samp_mkdir)
    ##### list of sample in the affected and non-affected family
    glb_aff=[ x for x in ped.loc[ped.loc[:,'phenotype']==2,'individualid']]
    glb_naf=[ x for x in ped.loc[ped.loc[:,'phenotype']==1,'individualid']]
    ##### list of family
    #################################################### Global affected
    glb_aff_sam = hl.literal(hl.set(glb_aff))
    glb_aff_sam_mt=mt.filter_cols(glb_aff_sam.contains(mt.s))
    # fam_aff_mt.count()
    ## wildtype 
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_r= glb_aff)
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_wild = hl.agg.sum(glb_aff_sam_mt.wild))
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_wild_c = hl.agg.collect(glb_aff_sam_mt.wild))
    # no call
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_ncl = hl.agg.sum(glb_aff_sam_mt.ncl))
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_ncl_c = hl.agg.collect(glb_aff_sam_mt.ncl))
    # variant 
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_vrt = hl.agg.sum(glb_aff_sam_mt.vrt))
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_vrt_c = hl.agg.collect(glb_aff_sam_mt.vrt))
    # hom_var: contains identical alternate alleles
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_homv = hl.agg.sum(glb_aff_sam_mt.homv))
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_homv_c = hl.agg.collect(glb_aff_sam_mt.homv))
    # altaf: contains  ALT allele frequency   
    glb_aff_sam_mt = glb_aff_sam_mt.annotate_rows(glb_aff_altaf = (hl.agg.call_stats(glb_aff_sam_mt.GT, glb_aff_sam_mt.alleles).AF[1]))
    # listt2=[]
    # name2=f'{outfolder}/samp/glb_aff.csv'
    listt2=['glb_aff_r','glb_aff_wild','glb_aff_wild_c','glb_aff_ncl','glb_aff_ncl_c','glb_aff_vrt','glb_aff_vrt_c', 'glb_aff_homv', 'glb_aff_homv_c','glb_aff_altaf']
    df3=glb_aff_sam_mt.rows().select(*listt2).to_spark()
    udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
    df4=df3.select('glb_aff_r','glb_aff_wild','glb_aff_wild_c','glb_aff_ncl','glb_aff_ncl_c','glb_aff_vrt','glb_aff_vrt_c', 'glb_aff_homv', 'glb_aff_homv_c','glb_aff_altaf',udf_i('glb_aff_wild_c').alias('glb_aff_wild_c2'),udf_i('glb_aff_ncl_c').alias('glb_aff_ncl_c2'),udf_i('glb_aff_vrt_c').alias('glb_aff_vrt_c2'),udf_i('glb_aff_homv_c').alias('glb_aff_homv_c2'))
    del df3
    udf_2b = udf(lambda x,ref: [x[i] for i in ref])
    df5=df4.select('glb_aff_wild',udf_2b('glb_aff_r', 'glb_aff_wild_c2').alias('glb_aff_wild_s'),'glb_aff_ncl',udf_2b('glb_aff_r', 'glb_aff_ncl_c2').alias('glb_aff_ncl_s'),'glb_aff_vrt', udf_2b('glb_aff_r', 'glb_aff_vrt_c2').alias('glb_aff_vrt_s'),'glb_aff_homv', udf_2b('glb_aff_r', 'glb_aff_homv_c2').alias('glb_aff_homv_s'),'glb_aff_altaf')
    str_udf = F.udf(str_list, T.StringType())
    df6=df5.select('glb_aff_wild',str_udf('glb_aff_wild_s').alias('glb_aff_wild_samp'),'glb_aff_ncl',str_udf('glb_aff_ncl_s').alias('glb_aff_ncl_samp'),'glb_aff_vrt', str_udf('glb_aff_vrt_s').alias('glb_aff_vrt_samp'),'glb_aff_homv',str_udf('glb_aff_homv_s').alias('glb_aff_homv_samp'),'glb_aff_altaf')
    del df5
    name_glb_csv=f'{outfolder}/samp/glb_affcsv'
    df6.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name_glb_csv)
    del df6
    cmd_glb_aff0=f'cd {outfolder}/samp/glb_affcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_aff_out \; ; rm -r  ../glb_affcsv'
    os.system(cmd_glb_aff0)  
    cmd_prune_glb=f'cd {outfolder}/samp;' + ' sed -i glb_aff_out -e \"s/\[\]/\[\\"\\"\]/g ; s/\[\'/\[\\"/g ;  s/\'\]/\\"\]/g ;  s/\'/\\"/g ; s/\[\]/\[\"\"\]/g \" '
    os.system(cmd_prune_glb)
    cmd_prune_glb_mv=f'mv {outfolder}/samp/glb_aff_out {outfolder}/glb_aff_out'
    os.system(cmd_prune_glb_mv)
    # list_generated.append('glb_aff.csv')
    ##################################################### Global unaffected
    ##### generate global non-affected
    glb_naf_sam = hl.literal(hl.set(glb_naf))
    glb_naf_sam_mt=mt.filter_cols(glb_naf_sam.contains(mt.s))
    # glb_naf_sam_mt.count()
    ## wildtype 
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_r= glb_naf)
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_wild = hl.agg.sum(glb_naf_sam_mt.wild))
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_wild_c = hl.agg.collect(glb_naf_sam_mt.wild))
    # no call
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_ncl = hl.agg.sum(glb_naf_sam_mt.ncl))
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_ncl_c = hl.agg.collect(glb_naf_sam_mt.ncl))
    # variant 
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_vrt = hl.agg.sum(glb_naf_sam_mt.vrt))
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_vrt_c = hl.agg.collect(glb_naf_sam_mt.vrt))
    # hom_var: contains identical alternate alleles
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_homv = hl.agg.sum(glb_naf_sam_mt.homv))
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_homv_c = hl.agg.collect(glb_naf_sam_mt.homv))
    # altaf: contains  ALT allele frequency   
    glb_naf_sam_mt = glb_naf_sam_mt.annotate_rows(glb_naf_altaf = (hl.agg.call_stats(glb_naf_sam_mt.GT, glb_naf_sam_mt.alleles).AF[1]))
    # listt2=[]
    # name2=f'{outfolder}/samp/glb_naf.csv'
    listt2=['glb_naf_r','glb_naf_wild','glb_naf_wild_c','glb_naf_ncl','glb_naf_ncl_c','glb_naf_vrt','glb_naf_vrt_c', 'glb_naf_homv', 'glb_naf_homv_c','glb_naf_altaf']
    # spark = SparkSession.builder.appName("myApp").getOrCreate()
    df3=glb_naf_sam_mt.rows().select(*listt2).to_spark()
    # udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
    df4=df3.select('glb_naf_r','glb_naf_wild','glb_naf_wild_c','glb_naf_ncl','glb_naf_ncl_c','glb_naf_vrt','glb_naf_vrt_c', 'glb_naf_homv', 'glb_naf_homv_c','glb_naf_altaf',udf_i('glb_naf_wild_c').alias('glb_naf_wild_c2'),udf_i('glb_naf_ncl_c').alias('glb_naf_ncl_c2'),udf_i('glb_naf_vrt_c').alias('glb_naf_vrt_c2'),udf_i('glb_naf_homv_c').alias('glb_naf_homv_c2'))
    del df3
    # udf_2b = udf(lambda x,ref: [x[i] for i in ref])
    df5=df4.select('glb_naf_wild',udf_2b('glb_naf_r', 'glb_naf_wild_c2').alias('glb_naf_wild_s'),'glb_naf_ncl',udf_2b('glb_naf_r', 'glb_naf_ncl_c2').alias('glb_naf_ncl_s'),'glb_naf_vrt', udf_2b('glb_naf_r', 'glb_naf_vrt_c2').alias('glb_naf_vrt_s'),'glb_naf_homv', udf_2b('glb_naf_r', 'glb_naf_homv_c2').alias('glb_naf_homv_s'),'glb_naf_altaf')
    # str_udf = F.udf(str_list, T.StringType())
    df6=df5.select('glb_naf_wild',str_udf('glb_naf_wild_s').alias('glb_naf_wild_samp'),'glb_naf_ncl',str_udf('glb_naf_ncl_s').alias('glb_naf_ncl_samp'),'glb_naf_vrt', str_udf('glb_naf_vrt_s').alias('glb_naf_vrt_samp'),'glb_naf_homv',str_udf('glb_naf_homv_s').alias('glb_naf_homv_samp'),'glb_naf_altaf')
    del df5
    name_glb_csv=f'{outfolder}/samp/glb_nafcsv'
    df6.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name_glb_csv)
    del df6
    cmd_glb_aff0=f'cd {outfolder}/samp/glb_nafcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_naf_out \; ; rm -r  ../glb_nafcsv'
    os.system(cmd_glb_aff0)  
    cmd_prune_glb=f'cd {outfolder}/samp;' + ' sed -i glb_naf_out -e \"s/\[\]/\[\\"\\"\]/g ; s/\[\'/\[\\"/g ;  s/\'\]/\\"\]/g ;  s/\'/\\"/g ; s/\[\]/\[\"\"\]/g \" '
    os.system(cmd_prune_glb)
    cmd_prune_glb_mv=f'mv {outfolder}/samp/glb_naf_out {outfolder}/glb_naf_out'
    os.system(cmd_prune_glb_mv)
    # mt.rows().export(f'{outfolder}/out_locus0',delimiter='\t')
    # cmd_glb_csq=f'cut -f 1-2 {outfolder}/out_locus0 > {outfolder}/out_locus; rm {outfolder}/out_locus0'
    # os.system(cmd_glb_csq)
    cmd_glb_rm = f"""
                    eval paste {outfolder}/out_locus {outfolder}/glb_aff_out {outfolder}/glb_naf_out > {outfolder}/glb_aff_naf_out
                    rm {outfolder}/out_locus {outfolder}/glb_aff_out {outfolder}/glb_naf_out
                    rm -rf {outfolder}/samp
                    rm {outfolder}/.out_locus0.crc
                    """
    os.system(cmd_glb_rm)
    # list_generated.append('glb_naf.csv')

#################
# MAIN FUNCTION #
#################

def segrun_family_wise_whole_multiple(mt, ped, outfolder, hl, csqlabel, affecteds_only, filter_variant, retrieve_sample_id, ncol):
    # print('temp 0')
    # ncol=7
    # affecteds_only=eval(str(str(affecteds_only)))
    # filter_variant=eval(str(str(filter_variant)))
    ########################################
    # INPUT ARGUMENTS:
    #
    # mt                (hail.MatrixTable)  hail MatrixTable object originally created by step2.py, 
    #                                       read from a folder created in step1 and passed 
    #                                       through seg.py to the current function
    #
    # ped               (pandas.DataFrame)  parsed by step2.py from original pedigree file and passed
    #                                       through seg.py to the current function
    #
    # outfolder         (string)            path to folder where output files from this function
    #                                       will be stored. MUST EXIST
    #
    # hl                (module)            hail module, imported by step2.py and passed through
    #                                       seg.py to the current function to save loading time
    #
    # csqlabel          (list)              CSQ definition, parsed from INFO field of original vcf by seg.py
    #                                       into a list and passed to the current function
    #
    # affecteds_only    (boolean)           Determines function output behaviour: 
    #                                       True = only output variants found in >0 family affecteds [default]
    #                                       False = output all variants found in family, regardless of phenotype
    #
    # ncol              (integer)           Size of chunks to split vcf INFO fields, in order to circumvent 
    #                                       hail problems with exporting overly-large numbers of annotations
    #                                       Increased values will reduce runtime but may cause hail to die
    #
    ########################################
    ########################################
    # POPULATE INPUTS AND DERIVATIVE OBJECTS
    # store overall start time for logging at end of run
    start_time0 = datetime.now()
    # set up logging module
    logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, stream=sys.stderr, filemode='w')
    ##
    # matrixTable info:
    # input matrixTable
    step = 'populate_mt'
    start_time = datetime.now()
    #mt = hl.read_matrix_table(mt)
    # annotate each entry (variant x sample) with specific GT tags
    mt = mt.annotate_entries(   wild = mt.GT.is_hom_ref(),
                                ncl = hl.is_missing(mt.GT),
                                vrt = mt.GT.is_het(),
                                homv = mt.GT.is_hom_var())
    timekeeping(step, start_time)
    # Generate the locus. 
    mt.rows().export(f'{outfolder}/out_locus0',delimiter='\t')
    cmd_glb_csq=f'cut -f 1-2 {outfolder}/out_locus0 > {outfolder}/out_locus; rm {outfolder}/out_locus0'
    os.system(cmd_glb_csq)
    #
    ###
    ###
    # pedigree info
    # input pedigree, plus derived lists
    step = 'populate_ped'
    start_time = datetime.now()
    # populate detailed sample_dict:
    # for each family in ped file: create lists of samples: fam vs nonfam (nfm); all vs affecteds vs non-affecteds (naf)
    sample_dict = {}
    for fam in ped.loc[:,'familyid'].unique(): sample_dict[fam] = {
            'fam': {
                'aff':[x for x in ped.loc[(ped.familyid==fam) & (ped.phenotype==2), 'individualid']], 
                'naf':[x for x in ped.loc[(ped.familyid==fam) & (ped.phenotype==1), 'individualid']]
            },
            'nfm': {
                'aff':[x for x in ped.loc[(ped.familyid!=fam) & (ped.phenotype==2), 'individualid']], 
                'naf':[x for x in ped.loc[(ped.familyid!=fam) & (ped.phenotype==1), 'individualid']]
            }
        }
    timekeeping(step, start_time)
    # populate simple family list:
    # all families, or all families with at least one affected sample if affecteds_only=TRUE
    # affecteds_only=TRUE
    if affecteds_only == "TRUE":
        fam_list = [fam for fam in sample_dict if len(sample_dict[fam]['fam']['aff'])>0]
    else:
        fam_list = list(sample_dict.keys())
    # fam_list =  sample_dict.keys() 
    # if len(fam_list)<3:
        # fam_list=[fam_list[0]]
    timekeeping(step, start_time)
    # print("AAAAAA")
    # print(fam_list)
    #
    ###
    # POPULATE INPUTS AND DERIVATIVE OBJECTS
    ########################################
    ########################################
    # POPULATE GLOBAL ANNOTATIONS: CSQ, INFO

    # processing INFO CSQ field
    # pseudo:   CSQ field comes pre-joined by transcript, and is not natively exportable to table as separate columns
    #           therefore the process to do so is:
    #           0) receive vcf INFO header for CSQ as argument to main function
    #           1) create a new MatrixTable annotation splitting each transcript into a list
    #           2) for each CSQ annotation, create a new MatrixTable row field mapping transcript-specific values (as list)
    #           3) export new row annotations to tsv
    #           NOTE: to reduce memory (and possibly runtime) footprint, split the export operation into chunks
    if csqlabel:
        step = 'process_csq'
        start_time = datetime.now()
        # create new row field containing list (and order) of all transcripts in CSQ fields
        mt = mt.annotate_rows(kept_transcripts = mt.info.CSQ.map(lambda x: x.split('\|')))
        # iterate over csq fields, adding a new row field for each CSQ annotation
        csq_rows = []
        for i in range(1,len(csqlabel)):
            mt = mt.annotate_rows(ab=mt.kept_transcripts.map(lambda x:hl.struct(value=x[i])))
            mt = mt.rename({'ab':f'{csqlabel[i]}'})
            csq_rows.append(csqlabel[i])
        # export to tsv: must split csq_rows into sub-lists of size ncol in order to avoid busting memory
        csq_list_of_lists = [csq_rows[i:i + ncol] for i in range(0, len(csq_rows), ncol)]
        for i in range(0, len(csq_list_of_lists)):
                mt.rows().select(*csq_list_of_lists[i]).export(f'{outfolder}/out_csq_{i}', delimiter='\t')
                formatTmpCsv(f'{outfolder}/out_csq_{i}', f'{outfolder}/temp')
        cmd_paste = f'paste $(ls -rt {outfolder}/out_csq_*) > {outfolder}/out_csq; rm {outfolder}/out_csq_*'
        os.system(cmd_paste)
        timekeeping(step, start_time)
    # processing the rest of the INFO field data
    # pseudo:   vcf INFO fields are not natively exportable as separate columns to tsv;
    #           therefore the process to do so is:
    #           1) "flatten" info fields into a new hail.Table
    #           2) export that table to tsv
    #           3) clean up outputs to remove formatting introduced by step 1
    #           NOTE: to reduce memory (and possibly runtime) footprint, split the export operation into chunks
    step = 'process_info'
    start_time = datetime.now()
    # flatten info field into a new hl.Table
    ht = mt.rows().flatten()
    info_columns = list(map(lambda x: 'info.'+x, list(mt.info)))
    # split info into sub-lists of size ncol in order to be able to export to csv without busting memory for larger datasets
    info_list_of_lists = [info_columns[i:i + ncol] for i in range(0, len(info_columns), ncol)]
    for i in range(0, len(info_list_of_lists)):
        ht.select(*info_list_of_lists[i]).export(f'{outfolder}/out_info_{i}', delimiter='\t')
    # cleanup unwanted formatting
    cmd_sed_header = f"sed '1!b; s/info.//g' -i {outfolder}/out_info_*"
    cmd_sed_body  = f"sed 's/\<NA\>//g' -i {outfolder}/out_info_*"
    os.system(cmd_sed_header)
    os.system(cmd_sed_body)
    # paste split outfiles into a single outfile for ease of processing later
    cmd_paste = f'paste $(ls -1 {outfolder}/out_info_*|sort -t_ -k3g) > {outfolder}/out_info; rm {outfolder}/out_info_*'
    os.system(cmd_paste)
    timekeeping(step, start_time)
    # POPULATE GLOBAL ANNOTATIONS: CSQ, INFO
    ########################################
    if retrieve_sample_id == "TRUE":
        step = 'sample retrieve id'
        # start_time = datetime.now()
        sample_retrieve(mt, ped, outfolder)
        # time.sleep(20)  
        # fam_seg_files_str = ' '.join(['glb_aff_out','glb_naf_out',fam_seg_files_str])
        timekeeping(step, start_time)
        # cmd_glb_rm= f'rm {outfolder}/samp/glb_aff.csv {outfolder}/samp/glb_naf.csv'
        # os.system(cmd_glb_rm)
    ########################################
    # PER-FAMILY PROCESSING
    for fam in fam_list:
        ###
        # create family-specific hail.MatrixTables, to be parsed for counts etc. below
        start_time_fam = datetime.now()
        step = f'family_{fam}:generate fam/nfm x aff/naf matrixTables'
        start_time = datetime.now()
        fam_aff_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['fam']['aff'])
        fam_naf_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['fam']['naf'])
        nfm_aff_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['nfm']['aff'])
        nfm_naf_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['nfm']['naf'])
        timekeeping(step, start_time)
        #
        ###
        ###
        # generate counts for each MT: fam/nfm x aff/naf. 
        step = f'family_{fam}:generate_counts'
        start_time = datetime.now()
        fam_aff_mt = generate_counts_m(fam_aff_mt, fam, sample_dict[fam]['fam']['aff'],ped)
        fam_naf_mt = generate_counts_m(fam_naf_mt, fam, sample_dict[fam]['fam']['naf'],ped)
        nfm_aff_mt = generate_counts_m(nfm_aff_mt, fam, sample_dict[fam]['nfm']['aff'],ped)
        nfm_naf_mt = generate_counts_m(nfm_naf_mt, fam, sample_dict[fam]['nfm']['naf'],ped)
        timekeeping(step, start_time)
        #
        ###
        ###
        # print selected rows to temporary files for later concatenation into final output file
        # processing family counts
        step = f'family_{fam}:export_counting_rows'
        # ... export locus and familyid to file
        fam_aff_mt.rows().select(*['familyid']).export(f'{outfolder}/out_locus',delimiter='\t')
        # ... export counts to files
        export_counts_m(fam_aff_mt, 'fam_aff', f'{outfolder}/out_fam_aff', sample_dict[fam]['fam']['aff'],outfolder)
        export_counts_m(fam_naf_mt, 'fam_naf', f'{outfolder}/out_fam_naf', sample_dict[fam]['fam']['naf'],outfolder)
        export_counts_m(nfm_aff_mt, 'nfm_aff', f'{outfolder}/out_nfm_aff', sample_dict[fam]['nfm']['aff'],outfolder)
        export_counts_m(nfm_naf_mt, 'nfm_naf', f'{outfolder}/out_nfm_naf', sample_dict[fam]['nfm']['naf'],outfolder)
        timekeeping(step, start_time)
        # concatenate temporary files into single per-family output file
        step = f'family_{fam}:finalize_family_output'
        start_time = datetime.now()
        # ... format counting files to remove locus columns
        output_filenames = ['out_fam_aff','out_fam_naf','out_nfm_aff','out_nfm_naf']
        for filename in output_filenames: formatTmpCsv(filename, f'{outfolder}/temp')
        # NOTE: double curly braces in cmd below are literal curly braces 
        #       to be interpreted by os.system(), not f-string notation for python
        if csqlabel:
            # cmd_paste = f'eval paste out_{{locus,info,csq,{{fam,nfm}}_{{aff,naf}}}} > {fam}_seg'
            cmd_paste = f'eval paste out_locus out_info out_csq out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf > {fam}_seg'
            if retrieve_sample_id == "TRUE":
                cmd_paste = f'eval paste out_locus out_info out_csq out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf {outfolder}/glb_aff_naf_out > {fam}_seg'
            else:
                cmd_paste = f'eval paste out_locus out_info out_csq out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf > {fam}_seg'
        else:
            # cmd_paste = f'eval paste out_{{locus,info,{{fam,nfm}}_{{aff,naf}}}} > {fam}_seg'
            if retrieve_sample_id == "TRUE":
                cmd_paste = f'eval paste out_locus out_info out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf {outfolder}/glb_aff_naf_out > {fam}_seg'
            else:
                cmd_paste = f'eval paste out_locus out_info out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf > {fam}_seg'
        os.system(cmd_paste)
        #
        ###
        ###
        # a little cleanup to remove unavoidable matrixTable formatting
        cmd_format = f'sed -i -e "s/\\"value\\"://g" -e "s/{{//g" -e "s/}}//g" {fam}_seg'
        os.system(cmd_format)
        timekeeping(step, start_time)
        #
        ###
        ###
        # garbage collection, to free up memory
        step = f'family_{fam}:garbage_collection'
        start_time = datetime.now()
        del fam_aff_mt, fam_naf_mt, nfm_aff_mt, nfm_naf_mt
        gc.collect()
        timekeeping(step, start_time)
        timekeeping(f'family_{fam}:TOTAL', start_time_fam)
    # PER-FAMILY PROCESSING
    ########################################
    ########################################
    # GENERATE FINAL OUTPUT FILE
    preOutfile = 'pre_out.csv'
    outfile = f'{outfolder}/finalseg.csv'
    # cat per-family results into a single file
    step = 'concat_final_results'
    start_time = datetime.now()
    fam_seg_files_str = ' '.join([f'{x}_seg' for x in fam_list])
    # if retrieve_sample_id == "TRUE":
        # step = 'sample retrieve id'
        # start_time = datetime.now()
        # sample_retrieve(mt, ped, outfolder)
        # time.sleep(20)  
        # fam_seg_files_str = ' '.join(['glb_aff_out','glb_naf_out',fam_seg_files_str])
        # timekeeping(step, start_time)
        # cmd_glb_rm= f'rm {outfolder}/samp/glb_aff.csv {outfolder}/samp/glb_naf.csv'
        # os.system(cmd_glb_rm)
    cmd_cat = f"awk 'NR==1||FNR>1' {fam_seg_files_str} > {preOutfile}"
    os.system(cmd_cat)
    timekeeping(step, start_time)
    # cmd_glb_paste= f'eval paste {preOutfile} {outfolder}/glb_aff_out {outfolder}/glb_naf_out > {preOutfile}'
    # os.system(cmd_glb_paste)
    # remove unwanted lines
    step = 'filter_final_results_by_counts'
    # print('temp 3')
    # ... parse counting column numbers from preOutfile
    cmd_parse_1 =  f'head -n 1 {preOutfile}'
    cmd_parse_2 = "awk -F'\t' '{for (i=1; i<=NF; i++) if ($i~/^(fam|nfm)_/) print $i,i}'"
    pIn  = subprocess.Popen(cmd_parse_1, stdout=subprocess.PIPE, shell=True)
    pOut = io.StringIO(subprocess.check_output(cmd_parse_2, stdin=pIn.stdout, shell=True, text=True).rstrip())
    PandasDataFrameDict = pd.read_table(pOut, sep=' ', header=None).to_dict(orient='list')
    columnName2Index = dict(zip(PandasDataFrameDict[0], PandasDataFrameDict[1]))
    colKeys = ['fam_aff_vrt','fam_aff_homv','fam_naf_vrt','fam_naf_homv']
    col_famAffVrt, col_famAffHomv, col_famNafVrt, col_famNafHomv = [columnName2Index.get(k, None) for k in colKeys]
    # ... filter pre-output file using relevant counting column values
    # if affecteds_only=="TRUE":
    #     cmd_filter_aff =    f"""
    #                         awk -F'\t'  \
    #                             -v a_v={col_famAffVrt} \
    #                             -v a_h={col_famAffHomv} \
    #                             'NR==1 || $a_v + $a_h > 0' \
    #                             {preOutfile} > {outfile}
    #                      """
    #     os.system(cmd_filter_aff)
    if filter_variant == "TRUE":
        cmd_filter =    f"""
                            awk -F'\t'  \
                                -v a_v={col_famAffVrt} \
                                -v a_h={col_famAffHomv} \
                                -v n_v={col_famNafVrt} \
                                -v n_h={col_famNafHomv} \
                                'NR==1 || $a_v + $a_h + $n_v + $n_h > 0' \
                                {preOutfile} > {outfile}
                         """
    else:
        cmd_filter =    f"""
                        cat {preOutfile} > {outfile}
                        """
    os.system(cmd_filter)
    # GENERATE FINAL OUTPUT FILE
    ########################################
    # RETRIEVE SAMPLE ID
    ########################################
    # if retrieve_sample_id == "TRUE":
    #     step = 'sample retrieve id'
    #     start_time = datetime.now()
    #     sample_retrieve(mt, ped, outfolder)
    #     cmd_glb_paste= f'eval paste out_locus {outfolder}/samp/glb_aff.csv {outfolder}/samp/glb_naf.csv > {outfolder}/samp/glb_retrieve.csv'
    #     os.system(cmd_glb_paste)
    #     cmd_glb_rm= f'rm {outfolder}/samp/glb_aff.csv {outfolder}/samp/glb_naf.csv'
    #     os.system(cmd_glb_rm)
    #     timekeeping(step, start_time)
    ########################################
    # FINAL CLEANUP AND LOGGING
    # delete temporary files
    # NOTE: any tmpdir created by function formatTmpCsv will NOT be deleted;
    #       this is to avoid accidentally deleting unintended files if the user ever
    #       happened to have anything else in their tmpfolder for whatever reason
    step = 'cleanup_temporary_files'
    start_time = datetime.now()
    cmd_rm = 'rm ' + ' '.join([f'{fam}_seg' for fam in fam_list]) + f' {preOutfile}' + ' out_locus out_info out_fam_aff out_fam_naf out_nfm_aff out_nfm_naf'
    if csqlabel: cmd_rm = cmd_rm + ' out_csq'
    os.system(cmd_rm)  
    cmd_rm_out_all = 'rm .out_*'
    os.system(cmd_rm_out_all)  
    # print('testing: skipping cleanup for now')#os.system(cmd_rm)  
    timekeeping(step, start_time)
    cmd_rm = f'rm -rf {outfolder}/temp; rm -rf {outfolder}/samp; rm {outfolder}/glb_aff_naf_out '
    os.system(cmd_rm)
    # final timestamp
    timekeeping('Segrun', start_time0)
    # FINAL CLEANUP AND LOGGING
    ########################################
