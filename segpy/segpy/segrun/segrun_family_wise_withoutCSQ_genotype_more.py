import os 
# import pandas as pd
import numpy as np 

from pyspark.sql import SparkSession
# import pyspark as spark
# import pyspark
from pyspark.sql.functions import udf
# from pyspark.sql.types import StructType
from pyspark.sql.types import ArrayType
from pyspark.sql.types import IntegerType

import pyspark.sql.functions as F
import pyspark.sql.types as T
from segpy.tools.utils import str_list


##### seg with CSQ with different phenotypes
def segrun_family_wise_withoutCSQ_genotype_more(mt, ped, outfolder,hl):
    ###
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
    listt2=[]
    name2=f'{outfolder}/temp/glb_aff.csv'
    listt2=['glb_aff_r','glb_aff_wild','glb_aff_wild_c','glb_aff_ncl','glb_aff_ncl_c','glb_aff_vrt','glb_aff_vrt_c', 'glb_aff_homv', 'glb_aff_homv_c','glb_aff_altaf']
    # spark = SparkSession.builder.appName("myApp").getOrCreate()
    df3=glb_aff_sam_mt.rows().select(*listt2).to_spark()
    # df3 = (aa)
    # del aa
    udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
    df4=df3.select('glb_aff_r','glb_aff_wild','glb_aff_wild_c','glb_aff_ncl','glb_aff_ncl_c','glb_aff_vrt','glb_aff_vrt_c', 'glb_aff_homv', 'glb_aff_homv_c','glb_aff_altaf',udf_i('glb_aff_wild_c').alias('glb_aff_wild_c2'),udf_i('glb_aff_ncl_c').alias('glb_aff_ncl_c2'),udf_i('glb_aff_vrt_c').alias('glb_aff_vrt_c2'),udf_i('glb_aff_homv_c').alias('glb_aff_homv_c2'))
    del df3
    udf_2b = udf(lambda x,ref: [x[i] for i in ref])
    df5=df4.select('glb_aff_wild',udf_2b('glb_aff_r', 'glb_aff_wild_c2').alias('glb_aff_wild_s'),'glb_aff_ncl',udf_2b('glb_aff_r', 'glb_aff_ncl_c2').alias('glb_aff_ncl_s'),'glb_aff_vrt', udf_2b('glb_aff_r', 'glb_aff_vrt_c2').alias('glb_aff_vrt_s'),'glb_aff_homv', udf_2b('glb_aff_r', 'glb_aff_homv_c2').alias('glb_aff_homv_s'),'glb_aff_altaf')
    # name2b=f'{outfolder}/temp/glb_affcsv'
    # df5.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name2b)
    # cmd_glb_aff0=f'cd {outfolder}/temp/glb_affcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_aff.csv \; ; rm -r  ../glb_affcsv'
    # os.system(cmd_glb_aff0) 
    # def str_list(x):
        # return str(x)
    str_udf = F.udf(str_list, T.StringType())
    df6=df5.select('glb_aff_wild',str_udf('glb_aff_wild_s').alias('glb_aff_wild_s'),'glb_aff_ncl',str_udf('glb_aff_ncl_s').alias('glb_aff_ncl_s'),'glb_aff_vrt', str_udf('glb_aff_vrt_s').alias('glb_aff_vrt_s'),'glb_aff_homv',str_udf('glb_aff_homv_s').alias('glb_aff_homv_s'),'glb_aff_altaf')
    del df5
    name2b=f'{outfolder}/temp/glb_affcsv'
    df6.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name2b)
    del df6
    cmd_glb_aff0=f'cd {outfolder}/temp/glb_affcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_aff.csv \; ; rm -r  ../glb_affcsv'
    os.system(cmd_glb_aff0)  
    cmd_prune_glb=f'cd {outfolder}/temp;' + ' sed -i glb_aff.csv -e \"s/\[\]/\[\\"\\"\]/g ; s/\[\'/\[\\"/g ;  s/\'\]/\\"\]/g ;  s/\'/\\"/g ; s/\[\]/\[\"\"\]/g \" '
    os.system(cmd_prune_glb)
    #############
    #############
    # glb_naf
    glb_naf_sam = hl.literal(hl.set(glb_naf))
    glb_naf_sam_mt=mt.filter_cols(glb_naf_sam.contains(mt.s))
    glb_naf_sam_mt.count()
    # Global 
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
    listt2=[]
    name2=f'{outfolder}/temp/glb_naf.csv'
    listt2=['glb_naf_r','glb_naf_wild','glb_naf_wild_c','glb_naf_ncl','glb_naf_ncl_c','glb_naf_vrt','glb_naf_vrt_c', 'glb_naf_homv', 'glb_naf_homv_c','glb_naf_altaf']
    # listt2=['glb_wild','glb_ncl','glb_vrt','glb_homv','glb_altaf']
    # glb_naf_sam_mt.rows().select(*listt2).export(name2, delimiter='\t')
    # spark = SparkSession.builder.appName("myApp").getOrCreate()
    df3=glb_naf_sam_mt.rows().select(*listt2).to_spark()
    # df3 = spark.createDataFrame(aa)
    # del aa
    udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
    df4=df3.select('glb_naf_r','glb_naf_wild','glb_naf_wild_c','glb_naf_ncl','glb_naf_ncl_c','glb_naf_vrt','glb_naf_vrt_c', 'glb_naf_homv', 'glb_naf_homv_c','glb_naf_altaf',udf_i('glb_naf_wild_c').alias('glb_naf_wild_c2'),udf_i('glb_naf_ncl_c').alias('glb_naf_ncl_c2'),udf_i('glb_naf_vrt_c').alias('glb_naf_vrt_c2'),udf_i('glb_naf_homv_c').alias('glb_naf_homv_c2'))
    del df3
    udf_2b = udf(lambda x,ref: [x[i] for i in ref])
    df5=df4.select('glb_naf_wild',udf_2b('glb_naf_r', 'glb_naf_wild_c2').alias('glb_naf_wild_s'),'glb_naf_ncl',udf_2b('glb_naf_r', 'glb_naf_ncl_c2').alias('glb_naf_ncl_s'),'glb_naf_vrt', udf_2b('glb_naf_r', 'glb_naf_vrt_c2').alias('glb_naf_vrt_s'),'glb_naf_homv', udf_2b('glb_naf_r', 'glb_naf_homv_c2').alias('glb_naf_homv_s'),'glb_naf_altaf')
    # name3b=f'{outfolder}/temp/glb_nafcsv'
    # df5.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name3b)
    # cmd_glb_naf0=f'cd {outfolder}/temp/glb_nafcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_naf.csv \; ; rm -r  ../glb_nafcsv'
    # os.system(cmd_glb_naf0)  
    # def str_list(x):
        # return str(x)
    str_udf = F.udf(str_list, T.StringType())
    df6=df5.select('glb_naf_wild',str_udf('glb_naf_wild_s').alias('glb_naf_wild_s'),'glb_naf_ncl',str_udf('glb_naf_ncl_s').alias('glb_naf_ncl_s'),'glb_naf_vrt', str_udf('glb_naf_vrt_s').alias('glb_naf_vrt_s'),'glb_naf_homv',str_udf('glb_naf_homv_s').alias('glb_naf_homv_s'),'glb_naf_altaf')
    del df5
    name2b=f'{outfolder}/temp/glb_nafcsv'
    df6.repartition(1).write.format("csv").mode('overwrite').option("sep","\t").option("header", "true").save(name2b)
    del df6
    cmd_glb_aff0=f'cd {outfolder}/temp/glb_nafcsv ; find . -type f -name \""*.csv"\" -exec mv {{}} ../glb_naf.csv \; ; rm -r  ../glb_nafcsv'
    os.system(cmd_glb_aff0)  
    cmd_prune_glb=f'cd {outfolder}/temp;' + ' sed -i glb_naf.csv -e \"s/\[\]/\[\\"\\"\]/g ; s/\[\'/\[\\"/g ;  s/\'\]/\\"\]/g ;  s/\'/\\"/g ; s/\[\]/\[\"\"\]/g \" '
    os.system(cmd_prune_glb)
    list_exist=[]
    for i in fam_list:
        #Whole family
        listt1=[]
        fam1[i]=[ x for x in ped.loc[ped.loc[:,'familyid']==i,'individualid']]
        if fam1[i]:
            list_exist.append(f'fam_{i}.csv')
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
            cmd_fam1=f'cd {outfolder}/temp ;  cut  -f 3- fam_{i}.csv > temp.csv ; mv  temp.csv  fam_{i}.csv'
            os.system(cmd_fam1)
        # Affected memeber
        listt12=[]
        fam12[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        if fam12[i]:
            # list_exist.append(f'fam_{i}_aff.csv')
            fam_sam2 = hl.literal(hl.set(fam12[i]))
            fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
            fam_sam_mt = fam_sam_mt.annotate_rows(familyid_aff = i)
            listt12.append(f'familyid_aff')
            fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff = fam12[i])
            listt12.append(f'sample_aff')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
            fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff'})
            listt12.append(f'fam_wild_aff')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
            fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff'})
            listt12.append(f'fam_ncl_aff')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
            fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff'})
            listt12.append(f'fam_vrt_aff')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
            fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff'})
            listt12.append(f'fam_homv_aff')
            name1=f'{outfolder}/temp/fam_{i}_aff.csv'
            fam_sam_mt.rows().select(*listt12).export(name1, delimiter='\t')
            cmd_fam12=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_aff.csv > temp.csv ; mv  temp.csv  fam_{i}_aff.csv'
            os.system(cmd_fam12)
            cmd_pack12=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_aff.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_aff.csv'
            os.system(cmd_pack12)
        # fam12s={}    
        # fam12s[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        # if fam12s[i] and len(fam12s[i])>1:
        #     for ifs in fam12s[i]:
        #         listt12s=[]
        #         # list_exist.append(f'fam_{i}_aff_{ifs}.csv')
        #         fam_sam2 = hl.literal(hl.set([ifs]))
        #         fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
        #         fam_sam_mt = fam_sam_mt.annotate_rows(familyid_aff = i)
        #         listt12s.append(f'familyid_aff')
        #         fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff = [ifs])
        #         listt12s.append(f'sample_aff')
        #         fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
        #         fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff'})
        #         listt12s.append(f'fam_wild_aff')
        #         fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
        #         fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff'})
        #         listt12s.append(f'fam_ncl_aff')
        #         fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
        #         fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff'})
        #         listt12s.append(f'fam_vrt_aff')
        #         fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
        #         fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff'})
        #         listt12s.append(f'fam_homv_aff')
        #         name1=f'{outfolder}/temp/fam_{i}_aff_{ifs}.csv'
        #         fam_sam_mt.rows().select(*listt12s).export(name1, delimiter='\t')
        #         cmd_fam12_s=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_aff_{ifs}.csv > temp.csv ; mv  temp.csv  fam_{i}_aff_{ifs}.csv'
        #         os.system(cmd_fam12_s)
        #         cmd_pack12=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_aff_{ifs}.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_aff_{ifs}.csv'
        #         os.system(cmd_pack12)
        # unaffected
        listt11=[]
        fam11[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==1),'individualid']]
        if fam11[i]:
            # list_exist.append(f'fam_{i}_naf.csv')        
            fam_sam1 = hl.literal(hl.set(fam11[i]))
            fam_sam_mt=mt.filter_cols(fam_sam1.contains(mt.s))
            fam_sam_mt = fam_sam_mt.annotate_rows(familyid_naf = i)
            listt11.append(f'familyid_naf')
            fam_sam_mt = fam_sam_mt.annotate_rows(sample_naf = fam11[i])
            listt11.append(f'sample_naf')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
            fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_naf'})
            listt11.append(f'fam_wild_naf')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
            fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_naf'})
            listt11.append(f'fam_ncl_naf')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
            fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_naf'})
            listt11.append(f'fam_vrt_naf')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
            fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_naf'})
            listt11.append(f'fam_homv_naf')
            name1=f'{outfolder}/temp/fam_{i}_naf.csv'
            fam_sam_mt.rows().select(*listt11).export(name1, delimiter='\t')
            cmd_fam11=f'cd {outfolder}/temp ;  cut -f 4- fam_{i}_naf.csv > temp.csv ; mv  temp.csv  fam_{i}_naf.csv'
            os.system(cmd_fam11)
            cmd_pack11=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_naf.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_naf.csv'
            os.system(cmd_pack11)
        fam12s={}    
        fam12s[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        if fam12s[i] and len(fam12s[i])>1:
            for ifs in fam12s[i]:
                listt12s=[]
                # list_exist.append(f'fam_{i}_aff_{ifs}.csv')
                fam_sam2 = hl.literal(hl.set([ifs]))
                fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
                fam_sam_mt = fam_sam_mt.annotate_rows(familyid_aff = i)
                listt12s.append(f'familyid_aff')
                fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff = [ifs])
                listt12s.append(f'sample_aff')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
                fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff'})
                listt12s.append(f'fam_wild_aff')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
                fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff'})
                listt12s.append(f'fam_ncl_aff')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
                fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff'})
                listt12s.append(f'fam_vrt_aff')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
                fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff'})
                listt12s.append(f'fam_homv_aff')
                name1=f'{outfolder}/temp/fam_{i}_aff_{ifs}.csv'
                fam_sam_mt.rows().select(*listt12s).export(name1, delimiter='\t')
                cmd_fam12_s=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_aff_{ifs}.csv > temp.csv ; mv  temp.csv  fam_{i}_aff_{ifs}.csv'
                os.system(cmd_fam12_s)
                cmd_pack12=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_aff_{ifs}.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_aff_{ifs}.csv'
                os.system(cmd_pack12)            
        fam11s={}    
        fam11s[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==1),'individualid']]
        if fam11s[i] and len(fam11s[i])>1:
            for ifs in fam11s[i]:
                listt11s=[]
                # list_exist.append(f'fam_{i}_naf_{ifs}.csv')
                fam_sam2 = hl.literal(hl.set([ifs]))
                fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
                fam_sam_mt = fam_sam_mt.annotate_rows(familyid_naf = i)
                listt11s.append(f'familyid_naf')
                fam_sam_mt = fam_sam_mt.annotate_rows(sample_naf = [ifs])
                listt11s.append(f'sample_naf')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
                fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_naf'})
                listt11s.append(f'fam_wild_naf')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
                fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_naf'})
                listt11s.append(f'fam_ncl_naf')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
                fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_naf'})
                listt11s.append(f'fam_vrt_naf')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
                fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_naf'})
                listt11s.append(f'fam_homv_naf')
                name1=f'{outfolder}/temp/fam_{i}_naf_{ifs}.csv'
                fam_sam_mt.rows().select(*listt11s).export(name1, delimiter='\t')
                cmd_fam11_s=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_naf_{ifs}.csv > temp.csv ; mv  temp.csv  fam_{i}_naf_{ifs}.csv'
                os.system(cmd_fam11_s)
                cmd_pack11=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_naf_{ifs}.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_naf_{ifs}.csv'
                os.system(cmd_pack11)
    # outputfile='finalseg.csv'
    # cmd_head=f'cd {outfolder}/temp ; head -1 fam_{i}_all.csv > {outputfile}'
    # cmd_pack1=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_csq.csv glb_naf.csv glb_aff.csv {list_exist[0]} > all_temp.csv'
    # os.system(cmd_pack1)    
    for run_list in list_exist:
        cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_naf.csv glb_aff.csv {run_list} > all_temp{run_list}'
        os.system(cmd_pack2)
    for run_list in list_exist:
        cmd_rm2=f'cd {outfolder}/temp ;rm {run_list}'
        os.system(cmd_rm2)            
        # cmd_temp=f'cd {outfolder}/temp ;rm fam_{i}_temp.csv'
        # os.system(cmd_temp)
        # cmd_rm=f'cd {outfolder}/temp ;rm {target_list}'
        # os.system(cmd_rm)  
    outputfile='finalseg.csv'
    cmd_head=f'cd {outfolder}/temp ; head -1 all_temp{list_exist[0]} > {outputfile}'
    os.system(cmd_head)
    for run_list in list_exist:
        cmd_rem0=f'cd {outfolder}/temp ;  sed -i 1d all_temp{run_list} ; cat all_temp{run_list} >> {outputfile}'
        os.system(cmd_rem0)
    cmd_rmall=f'cd {outfolder}/temp ;rm locus_alleles.csv glb_naf.csv glb_aff.csv all_temp*.csv'
    os.system(cmd_rmall)
    # cmd_temp_mv=f'cd {outfolder}/temp ;mv all_temp.csv {outputfile}'
    # os.system(cmd_temp_mv)
    # cmd_head=f'cd {outfolder}/temp ; head -1 fam_{i}_all.csv > {outputfile}'
    # os.system(cmd_head)
    # for i in fam_list:
    #     cmd_rem0=f'cd {outfolder}/temp ;  sed -i 1d fam_{i}_all.csv ; cat fam_{i}_all.csv >> {outputfile}'
    #     os.system(cmd_rem0)
    # cmd_rmall=f'cd {outfolder}/temp ;rm locus_alleles.csv glb_csq.csv glb_naf.csv glb_aff.csv'
    # os.system(cmd_rmall)
    # cmd_prune=f'cd {outfolder}/temp; sed -i finalseg.csv -e "s/\"value\"://g"'
    # os.system(cmd_prune)
    cmd_prune1=f'cd {outfolder}/temp; sed -i finalseg.csv -e "s/\\"value\\"://g"'
    os.system(cmd_prune1)
    cmd_prune2=f'cd {outfolder}/temp;'+ " sed -i finalseg.csv -e \"s/{//g"+ "; s/}//g\""
    os.system(cmd_prune2)
    cmd_header=f'cd {outfolder}/temp; head -1  finalseg.csv > header.txt'
    os.system(cmd_header)
    cmd_final=f'mv {outfolder}/temp/header.txt {outfolder}/; mv {outfolder}/temp/finalseg.csv {outfolder}/; rm -r {outfolder}/temp'
    os.system(cmd_final)
