import os 
import numpy as np 


from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StructType
from pyspark.sql.types import ArrayType
from pyspark.sql.types import IntegerType

import pyspark.sql.functions as F
import pyspark.sql.types as T
from segpy.tools.utils import str_list
import time
from datetime import datetime

def segrun_family_wise_whole(mt, ped, outfolder,hl, ncol,csqlabel,just_phenotype, info_required):
    print('############################################')
    print('Segrun started:')
    start_time0 = datetime.now()
    print('Local time: ', time.strftime("%Y-%m-%d %H:%M:%S"))
    print('############################################')
    list_exist=[]
    list_generated=['locus_alleles.csv']
#################################################### : GLOBAL
    start_time = datetime.now()
    stepofpip='Global'
    print('############################################')
    print(f'Step: {stepofpip}, start')
    print('############')
    ##### list of sample in the affected and non-affected family
    glb_aff=[ x for x in ped.loc[ped.loc[:,'phenotype']==2,'individualid']]
    glb_naf=[ x for x in ped.loc[ped.loc[:,'phenotype']==1,'individualid']]
    ##### list of family 
    fam_list=ped.loc[:,'familyid'].unique()
    fam1=fam11=fam12={}
    ##### generate sample in the family 
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
    ##### save locus_alleles
    name0=f'{outfolder}/temp/locus_alleles.csv'
    mt.rows().select('altaf').export(name0, delimiter='\t')
    cmd_glb_csq=f'cd {outfolder}/temp ; cut -d\'\t\' -f 1-2 locus_alleles.csv> temp.csv ; mv  temp.csv  locus_alleles.csv'
    os.system(cmd_glb_csq)
    print(f'Step: {stepofpip}, terminated')
    print('############')
    print('Total time to achieve: {}'.format(datetime.now() - start_time))
    print('############################################')
#################################################### : CSQ info 
    if (csqlabel is not False):
        start_time = datetime.now()
        stepofpip='CSQ'
        print('############################################')
        print(f'Step: {stepofpip}, start')
        print('############')
        mt1=mt
        mt1=mt1.annotate_rows(kept_transcripts =mt1.info.CSQ.map(lambda x: x.split('\|')))
        j2=0
        j1=0
        listt_csq=[]
        for i in range(1,len(csqlabel)):
            mt1=mt1.annotate_rows(ab=mt1.kept_transcripts.map(lambda x:hl.struct(value=x[i])))
            mt1 = mt1.rename({'ab':f'{csqlabel[i]}'})
            listt_csq.append(csqlabel[i])    
            j1=j1+1
            if j1>ncol:
                j1=1
                j2=j2+1
                name3=f'{outfolder}/temp/glb_csq_temp{j2}.csv'
                mt1.rows().select(*listt_csq).export(name3, delimiter='\t')
                cmd_glb_csq=f'cd {outfolder}/temp ; cut -d\'\t\' -f 3- glb_csq_temp{j2}.csv > temp.csv ; mv  temp.csv  glb_csq_temp{j2}.csv'
                os.system(cmd_glb_csq)      
                mt1=mt
                mt1=mt1.annotate_rows(kept_transcripts =mt1.info.CSQ.map(lambda x: x.split('\|'))) 
                listt_csq=[]
        if (j1<=ncol) & (1<j1):
            j1=1
            j2=j2+1
            name3=f'{outfolder}/temp/glb_csq_temp{j2}.csv'
            mt1.rows().select(*listt_csq).export(name3, delimiter='\t')
            cmd_glb_csq=f'cd {outfolder}/temp ; cut -d\'\t\' -f 3- glb_csq_temp{j2}.csv > temp.csv ; mv  temp.csv  glb_csq_temp{j2}.csv'
            os.system(cmd_glb_csq)      
            mt1=mt
            mt1=mt1.annotate_rows(kept_transcripts =mt1.info.CSQ.map(lambda x: x.split('\|'))) 
            listt_csq=[]                  
        cmd_glb_csq_all=f'cd {outfolder}/temp ; paste -d\'\t\' glb_csq_temp*.csv > temp.csv ; mv  temp.csv  glb_csq.csv; rm glb_csq_temp*.csv' 
        os.system(cmd_glb_csq_all)
        list_generated.append('glb_csq.csv')
        # list_exist.append('glb_csq.csv')
        print(f'Step: {stepofpip}, terminated')
        print('############')
        print('Total time to achieve: {}'.format(datetime.now() - start_time))
        print('############################################')
#################################################### Global affected
    if (1 in info_required):
        start_time = datetime.now()
        stepofpip='Global affected'
        print('############################################')
        print(f'Step: {stepofpip}, start')
        print('############')
        #############
        #############
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
        df3=glb_aff_sam_mt.rows().select(*listt2).to_spark()
        udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
        df4=df3.select('glb_aff_r','glb_aff_wild','glb_aff_wild_c','glb_aff_ncl','glb_aff_ncl_c','glb_aff_vrt','glb_aff_vrt_c', 'glb_aff_homv', 'glb_aff_homv_c','glb_aff_altaf',udf_i('glb_aff_wild_c').alias('glb_aff_wild_c2'),udf_i('glb_aff_ncl_c').alias('glb_aff_ncl_c2'),udf_i('glb_aff_vrt_c').alias('glb_aff_vrt_c2'),udf_i('glb_aff_homv_c').alias('glb_aff_homv_c2'))
        del df3
        udf_2b = udf(lambda x,ref: [x[i] for i in ref])
        df5=df4.select('glb_aff_wild',udf_2b('glb_aff_r', 'glb_aff_wild_c2').alias('glb_aff_wild_s'),'glb_aff_ncl',udf_2b('glb_aff_r', 'glb_aff_ncl_c2').alias('glb_aff_ncl_s'),'glb_aff_vrt', udf_2b('glb_aff_r', 'glb_aff_vrt_c2').alias('glb_aff_vrt_s'),'glb_aff_homv', udf_2b('glb_aff_r', 'glb_aff_homv_c2').alias('glb_aff_homv_s'),'glb_aff_altaf')
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
        list_generated.append('glb_aff.csv')
        # list_exist.append('glb_aff.csv')
        #############
        print(f'Step: {stepofpip}, terminated')
        print('############')
        print('Total time to achieve: {}'.format(datetime.now() - start_time))
        print('############################################')
##################################################### Global unaffected
    if (2 in info_required):
        start_time = datetime.now()
        stepofpip='Global non-affected'
        print('############################################')
        print(f'Step: {stepofpip}, start')
        print('############')
    ##### generate global non-affected
        glb_naf_sam = hl.literal(hl.set(glb_naf))
        glb_naf_sam_mt=mt.filter_cols(glb_naf_sam.contains(mt.s))
        glb_naf_sam_mt.count()
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
        spark = SparkSession.builder.appName("myApp").getOrCreate()
        df3=glb_naf_sam_mt.rows().select(*listt2).to_spark()
        udf_i = udf(lambda x: np.where(x)[0].tolist(), ArrayType(IntegerType()))
        df4=df3.select('glb_naf_r','glb_naf_wild','glb_naf_wild_c','glb_naf_ncl','glb_naf_ncl_c','glb_naf_vrt','glb_naf_vrt_c', 'glb_naf_homv', 'glb_naf_homv_c','glb_naf_altaf',udf_i('glb_naf_wild_c').alias('glb_naf_wild_c2'),udf_i('glb_naf_ncl_c').alias('glb_naf_ncl_c2'),udf_i('glb_naf_vrt_c').alias('glb_naf_vrt_c2'),udf_i('glb_naf_homv_c').alias('glb_naf_homv_c2'))
        del df3
        udf_2b = udf(lambda x,ref: [x[i] for i in ref])
        df5=df4.select('glb_naf_wild',udf_2b('glb_naf_r', 'glb_naf_wild_c2').alias('glb_naf_wild_s'),'glb_naf_ncl',udf_2b('glb_naf_r', 'glb_naf_ncl_c2').alias('glb_naf_ncl_s'),'glb_naf_vrt', udf_2b('glb_naf_r', 'glb_naf_vrt_c2').alias('glb_naf_vrt_s'),'glb_naf_homv', udf_2b('glb_naf_r', 'glb_naf_homv_c2').alias('glb_naf_homv_s'),'glb_naf_altaf')
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
        list_generated.append('glb_naf.csv')
        # list_exist.append('glb_naf.csv')
    ####################
    ####################
        print(f'Step: {stepofpip}, terminated')
        print('############')
        print('Total time to achieve: {}'.format(datetime.now() - start_time))
        print('############################################')
    # list_exist=[]
    for i in fam_list:
#################################################### family-wise
        listt1=[]
        fam1[i]=[ x for x in ped.loc[ped.loc[:,'familyid']==i,'individualid']]
        if (fam1[i]) and (3 in info_required):
            start_time = datetime.now()
            stepofpip='info for family wise'
            print('############################################')
            print(f'Step: {stepofpip}, start')
            print('############')            
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
            print(f'Step: {stepofpip}, terminated')
            print('############')
            print('Total time to achieve: {}'.format(datetime.now() - start_time))
            print('############################################')
            list_generated.append(f'fam_{i}.csv')
#################################################### affected-family-wise
        listt12=[]
        fam12[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        if (fam12[i]) and (1 in info_required) and (3 in info_required) and (4 in info_required):
            start_time = datetime.now()
            stepofpip='info for affected family wise'
            print('############################################')
            print(f'Step: {stepofpip}, start')
            print('############')
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
            print(f'Step: {stepofpip}, terminated')
            print('############')
            print('Total time to achieve: {}'.format(datetime.now() - start_time))
            print('############################################')
            list_generated.append(f'fam_{i}_aff.csv')
####################################################  affected-family-wise and non-include
        fam12n={}
        listt12n=[]
        fam12n[i]=[ x for x in ped.loc[(ped.familyid!=i) & (ped.phenotype==2),'individualid']]
        if (fam12n[i]) and (1 in info_required) and (3 in info_required) and (4 in info_required) and (5 in info_required):
            start_time = datetime.now()
            stepofpip='info for affected family and non-included'
            print('############################################')
            print(f'Step: {stepofpip}, start')
            print('############')            
            # list_exist.append(f'fam_{i}_aff.csv')
            fam_sam2 = hl.literal(hl.set(fam12n[i]))
            fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
            fam_sam_mt = fam_sam_mt.annotate_rows(familyid_aff_non = i)
            listt12n.append(f'familyid_aff_non')
            fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff_non = fam12n[i])
            listt12n.append(f'sample_aff_non')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
            fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff_non'})
            listt12n.append(f'fam_wild_aff_non')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
            fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff_non'})
            listt12n.append(f'fam_ncl_aff_non')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
            fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff_non'})
            listt12n.append(f'fam_vrt_aff_non')
            fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
            fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff_non'})
            listt12n.append(f'fam_homv_aff_non')
            name1=f'{outfolder}/temp/fam_{i}_aff_non.csv'
            fam_sam_mt.rows().select(*listt12n).export(name1, delimiter='\t')
            cmd_fam12=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_aff_non.csv > temp.csv ; mv  temp.csv  fam_{i}_aff_non.csv'
            os.system(cmd_fam12)
            cmd_pack12=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_aff_non.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_aff_non.csv'
            os.system(cmd_pack12)
            print(f'Step: {stepofpip}, terminated')
            print('############')
            print('Total time to achieve: {}'.format(datetime.now() - start_time))
            print('############################################')
            list_generated.append(f'fam_{i}_aff_non.csv')
##################################################### unaffected-family-wise
        listt11=[]
        fam11[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==1),'individualid']]
        run_below=True
        if (just_phenotype==True &  len(fam12[i])==0):
            run_below=False
        if run_below: 
            if (fam11[i]) and (2 in info_required) and (3 in info_required) and (4 in info_required):
                start_time = datetime.now()
                stepofpip='info for unaffected family'
                print('############################################')
                print(f'Step: {stepofpip}, start')
                print('############')                
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
                print(f'Step: {stepofpip}, terminated')
                print('############')
                print('Total time to achieve: {}'.format(datetime.now() - start_time))
                print('############################################')
                list_generated.append(f'fam_{i}_naf.csv')
##################################################### unaffected-family-wise and non-include
        fam11n={}
        listt11n=[]
        fam11n[i]=[ x for x in ped.loc[(ped.familyid!=i) & (ped.phenotype==1),'individualid']]
        run_below=True
        if (just_phenotype==True &  len(fam12[i])==0):
            run_below=False
        if run_below: 
            if (fam11n[i]) and (2 in info_required) and (3 in info_required) and (4 in info_required) and (5 in info_required):
                start_time = datetime.now()
                stepofpip='info for unaffected family and non-included'
                print('############################################')
                print(f'Step: {stepofpip}, start')
                print('############')                
                fam_sam1 = hl.literal(hl.set(fam11n[i]))
                fam_sam_mt=mt.filter_cols(fam_sam1.contains(mt.s))
                fam_sam_mt = fam_sam_mt.annotate_rows(familyid_naf_non = i)
                listt11n.append(f'familyid_naf_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sample_naf_non = fam11n[i])
                listt11n.append(f'sample_naf_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
                fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_naf_non'})
                listt11n.append(f'fam_wild_naf_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
                fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_naf_non'})
                listt11n.append(f'fam_ncl_naf_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
                fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_naf_non'})
                listt11n.append(f'fam_vrt_naf_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
                fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_naf_non'})
                listt11n.append(f'fam_homv_naf_non')
                name1=f'{outfolder}/temp/fam_{i}_naf_non.csv'
                fam_sam_mt.rows().select(*listt11n).export(name1, delimiter='\t')
                cmd_fam11=f'cd {outfolder}/temp ;  cut -f 4- fam_{i}_naf_non.csv > temp.csv ; mv  temp.csv  fam_{i}_naf_non.csv'
                os.system(cmd_fam11)
                cmd_pack11=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_naf_non.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_naf_non.csv'
                os.system(cmd_pack11)
                print(f'Step: {stepofpip}, terminated')
                print('############')
                print('Total time to achieve: {}'.format(datetime.now() - start_time))
                print('############################################')
                list_generated.append(f'fam_{i}_naf_non.csv')
###### Generate info for Affected memeber in the family, here we have more than one sample, and generate info for each sample
#################################################### affected-family-wise-multipe sample
        fam12s={}    
        fam12s[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==2),'individualid']]
        if fam12s[i] and len(fam12s[i])>1 and (1 in info_required) and (3 in info_required) and (4 in info_required) and  (6 in info_required):
            start_time = datetime.now()
            stepofpip='info for affected family-multipe sample'
            print('############################################')
            print(f'Step: {stepofpip}, start')
            print('############')
            for ifs in fam12s[i]:
                listt12s=[]
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
                list_generated.append(f'fam_{i}_aff_{ifs}.csv')
            print(f'Step: {stepofpip}, terminated')
            print('############')
            print('Total time to achieve: {}'.format(datetime.now() - start_time))
            print('############################################')
#################################################### affected-family-wise-multipe sample and non-included
        fam12sn={} 
        fam12sn[i]=[ x for x in ped.loc[(ped.familyid!=i) & (ped.phenotype==2),'individualid']]
        if fam12sn[i] and len(fam12sn[i])>1 and (1 in info_required) and (3 in info_required) and (4 in info_required) and (7 in info_required):
            start_time = datetime.now()
            stepofpip='info for affected family-multipe sample and non-included'
            print('############################################')
            print(f'Step: {stepofpip}, start')
            print('############')
            for ifs in fam12sn[i]:
                listt12sn=[]
                fam_sam2 = hl.literal(hl.set([ifs]))
                fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
                fam_sam_mt = fam_sam_mt.annotate_rows(familyid_aff_non = i)
                listt12sn.append(f'familyid_aff_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sample_aff_non = [ifs])
                listt12sn.append(f'sample_aff_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
                fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_aff_non'})
                listt12sn.append(f'fam_wild_aff_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
                fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_aff_non'})
                listt12sn.append(f'fam_ncl_aff_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
                fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_aff_non'})
                listt12sn.append(f'fam_vrt_aff_non')
                fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
                fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_aff_non'})
                listt12sn.append(f'fam_homv_aff_non')
                name1=f'{outfolder}/temp/fam_{i}_aff_non_{ifs}.csv'
                fam_sam_mt.rows().select(*listt12sn).export(name1, delimiter='\t')
                cmd_fam12_s=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_aff_non_{ifs}.csv > temp.csv ; mv  temp.csv  fam_{i}_aff_non_{ifs}.csv'
                os.system(cmd_fam12_s)
                cmd_pack12=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_aff_non_{ifs}.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_aff_non_{ifs}.csv'
                os.system(cmd_pack12)
                list_generated.append(f'fam_{i}_aff_non_{ifs}.csv')
            print(f'Step: {stepofpip}, terminated')
            print('############')
            print('Total time to achieve: {}'.format(datetime.now() - start_time))
            print('############################################')
##################################################### unaffected-family-wise-multipe sample
        fam11s={}
        fam11s[i]=[ x for x in ped.loc[(ped.familyid==i) & (ped.phenotype==1),'individualid']]
        run_below=True
        if (just_phenotype==True &  len(fam12s[i])==0):
            run_below=False
        if run_below: 
            if fam11s[i] and len(fam11s[i])>1  and (2 in info_required) and (3 in info_required) and (4 in info_required) and (6 in info_required):
                start_time = datetime.now()
                stepofpip='info for unaffected family-multipe sample'
                print('############################################')
                print(f'Step: {stepofpip}, start')
                print('############')
                for ifs in fam11s[i]:
                    listt11s=[]
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
                    list_generated.append(f'fam_{i}_naf_{ifs}.csv')
                print(f'Step: {stepofpip}, terminated')
                print('############')
                print('Total time to achieve: {}'.format(datetime.now() - start_time))
                print('############################################')
##################################################### unaffected-family-wise-multipe sample and non-include
        fam11sn={}
        fam11sn[i]=[ x for x in ped.loc[(ped.familyid!=i) & (ped.phenotype==1),'individualid']]
        run_below=True
        if (just_phenotype==True &  len(fam12s[i])==0):
            run_below=False
        if run_below: 
            if fam11sn[i] and len(fam11sn[i])>1 and (2 in info_required) and (3 in info_required) and (4 in info_required) and (7 in info_required):
                start_time = datetime.now()
                stepofpip='info for unaffected family-multipe sample, non-included'
                print('############################################')
                print(f'Step: {stepofpip}, start')
                print('############')
                for ifs in fam11sn[i]:
                    listt11sn=[]
                    fam_sam2 = hl.literal(hl.set([ifs]))
                    fam_sam_mt=mt.filter_cols(fam_sam2.contains(mt.s))
                    fam_sam_mt = fam_sam_mt.annotate_rows(familyid_naf_non = i)
                    listt11sn.append(f'familyid_naf_non')
                    fam_sam_mt = fam_sam_mt.annotate_rows(sample_naf_non = [ifs])
                    listt11sn.append(f'sample_naf_non')
                    fam_sam_mt = fam_sam_mt.annotate_rows(sam_wi = hl.agg.sum(fam_sam_mt.wild))
                    fam_sam_mt=fam_sam_mt.rename({'sam_wi': f'fam_wild_naf_non'})
                    listt11sn.append(f'fam_wild_naf_non')
                    fam_sam_mt = fam_sam_mt.annotate_rows(sam_ncl = hl.agg.sum(fam_sam_mt.ncl))
                    fam_sam_mt=fam_sam_mt.rename({'sam_ncl': f'fam_ncl_naf_non'})
                    listt11sn.append(f'fam_ncl_naf_non')
                    fam_sam_mt = fam_sam_mt.annotate_rows(sam_vrt = hl.agg.sum(fam_sam_mt.vrt))
                    fam_sam_mt=fam_sam_mt.rename({'sam_vrt': f'fam_vrt_naf_non'})
                    listt11sn.append(f'fam_vrt_naf_non')
                    fam_sam_mt = fam_sam_mt.annotate_rows(sam_homv = hl.agg.sum(fam_sam_mt.homv))
                    fam_sam_mt=fam_sam_mt.rename({'sam_homv': f'fam_homv_naf_non'})
                    listt11sn.append(f'fam_homv_naf_non')
                    name1=f'{outfolder}/temp/fam_{i}_naf_non_{ifs}.csv'
                    fam_sam_mt.rows().select(*listt11sn).export(name1, delimiter='\t')
                    cmd_fam11_s=f'cd {outfolder}/temp ;  cut  -f 4- fam_{i}_naf_non_{ifs}.csv > temp.csv ; mv  temp.csv  fam_{i}_naf_non_{ifs}.csv'
                    os.system(cmd_fam11_s)
                    cmd_pack11=f'cd {outfolder}/temp ;paste -d\'\t\' fam_{i}.csv fam_{i}_naf_non_{ifs}.csv > tmptmp.csv; mv tmptmp.csv fam_{i}.csv; rm fam_{i}_naf_non_{ifs}.csv'
                    os.system(cmd_pack11)
                    list_generated.append(f'fam_{i}_naf_non_{ifs}.csv')
                print(f'Step: {stepofpip}, terminated')
                print('############')
                print('Total time to achieve: {}'.format(datetime.now() - start_time))
                print('############################################')
    for run_list in list_exist:
        if (csqlabel is not False)  and (1 in info_required) and (2 in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_csq.csv glb_aff.csv glb_naf.csv {run_list} > la_temp_{run_list}'; os.system(cmd_pack2)
        elif (csqlabel is not False) and (1 in info_required) and (2 not in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_csq.csv glb_aff.csv {run_list} > la_temp_{run_list}';os.system(cmd_pack2)
        elif (csqlabel is not False) and (1 not in info_required) and (2 in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_csq.csv glb_naf.csv {run_list} > la_temp_{run_list}';os.system(cmd_pack2)
        elif (csqlabel is not False) and (1 not in info_required) and (2 not in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_csq.csv {run_list} > la_temp_{run_list}' ; os.system(cmd_pack2)
        elif (csqlabel is False) and (1 in info_required) and (2 in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_aff.csv glb_naf.csv {run_list} > la_temp_{run_list}' ; os.system(cmd_pack2)
        elif (csqlabel is False) and (1 in info_required) and (2 not in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_aff.csv {run_list} > la_temp_{run_list}' ; os.system(cmd_pack2)
        elif (csqlabel is False) and (1 not in info_required) and (2 in info_required): 
            cmd_pack2=f'cd {outfolder}/temp ;paste -d\'\t\' locus_alleles.csv glb_naf.csv {run_list} > la_temp_{run_list}' ; os.system(cmd_pack2)
    cmd_rm2=f'cd {outfolder}/temp ;ls --hide=la_temp_*.csv | xargs rm'
    os.system(cmd_rm2)
    outputfile='finalseg.csv'
    cmd_head=f'cd {outfolder}/temp ; head -1 la_temp_{list_exist[0]} > {outputfile}'
    os.system(cmd_head)
    for run_list in list_exist:
        cmd_rem0=f'cd {outfolder}/temp ;  sed -i 1d la_temp_{run_list} ; cat la_temp_{run_list} >> {outputfile}'
        os.system(cmd_rem0)
    cmd_rmall=f'cd {outfolder}/temp ;rm la_temp_*.csv'
    os.system(cmd_rmall)
    cmd_prune1=f'cd {outfolder}/temp; sed -i finalseg.csv -e "s/\\"value\\"://g"'
    os.system(cmd_prune1)
    cmd_prune2=f'cd {outfolder}/temp;'+ " sed -i finalseg.csv -e \"s/{//g"+ "; s/}//g\""
    os.system(cmd_prune2)
    cmd_header=f'cd {outfolder}/temp; head -1  finalseg.csv > header.txt'
    os.system(cmd_header)
    cmd_final=f'mv {outfolder}/temp/header.txt {outfolder}/; mv {outfolder}/temp/finalseg.csv {outfolder}/; rm -r {outfolder}/temp'
    os.system(cmd_final)
    print(f'Segrun terminated')
    print('############')
    print('Total time to achieve: {}'.format(datetime.now() - start_time0))
    print('############################################')


