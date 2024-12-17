#!/usr/bin/env python
####################
# step 2 
import numpy as np 
import sys
import pandas as pd 
import hail as hl
import session_info
import time
from datetime import datetime
import collections
import subprocess
import io
import os 


print('############################################')
print('Step2 started:')
start_time0 = datetime.now()
print('Local time: ', time.strftime("%Y-%m-%d %H:%M:%S"))

from segpy import seg

mt              = hl.read_matrix_table(sys.argv[1])
# mt=hl.split_multi(mt)
# mt=hl.split_multi_hts(mt)
ped             = pd.read_csv(sys.argv[2],sep='\t')
outfolder       = sys.argv[3]
CSQ             = sys.argv[4]
vcffile         = sys.argv[5]
sparkmem        = sys.argv[6]
if sparkmem != "False": hl.init(spark_conf={'spark.driver.memory': sparkmem})
affecteds_only  = sys.argv[7]
filter_variant  = sys.argv[8]
ncol            = int(sys.argv[9])
retrieve_sample_id = sys.argv[10]
ana_mode = sys.argv[11]

if ana_mode=='case-control':
    """No change"""
elif len(ped.iloc[:,0].unique())==1:
    ana_mode='single'
else:
    ana_mode='multiple'


seg.run(mt, ped, outfolder, hl, vcffile, CSQ, affecteds_only, filter_variant, retrieve_sample_id, ncol, ana_mode)


print('############################################')
print('Step2 - renaming step started:')

preOutfile = f'{outfolder}/finalseg.csv'
preOutfile_temp = f'{outfolder}/finalseg_temp.csv'


if ana_mode=='case-control':
    print('############')
    print('NOTE: Pipeline run case-control')
    print('############')
    cmd_parse_1 =  f'head -n 1 {preOutfile}'
    cmd_parse_2 = "awk -F'\t' '{for (i=1; i<=NF; i++) if ($i~/(glb_aff_wild?$|glb_aff_ncl?$|glb_aff_vrt?$|glb_aff_homv?$|glb_naf_wild?$|glb_naf_ncl?$|glb_naf_vrt?$|glb_naf_homv?$|nfm_aff_wild?$|nfm_aff_ncl?$|nfm_aff_vrt?$|nfm_aff_homv?$|nfm_naf_wild?$|nfm_naf_ncl?$|nfm_naf_vrt?$|nfm_naf_homv?$)/) print $i,i}'"
    #
    pIn  = subprocess.Popen(cmd_parse_1, stdout=subprocess.PIPE, shell=True)
    pOut = io.StringIO(subprocess.check_output(cmd_parse_2, stdin=pIn.stdout, shell=True, text=True).rstrip())
    PandasDataFrameDict = pd.read_table(pOut, sep=' ', header=None).to_dict(orient='list')
    #
    cmd_cut = 'cut ' + '--complement'+' ' +'-f' +''.join([f'{fam},' for fam in  PandasDataFrameDict[1][:-1]])  + f'{PandasDataFrameDict[1][-1]}' + f' {preOutfile} > {preOutfile_temp}'
    os.system(cmd_cut)
    #
    cmd_rm = f'rm -rf {preOutfile} '
    os.system(cmd_rm)
    #
    cmd_sed = f"sed 's/\<fam_aff_wild\>/case_WT/g;s/\<fam_aff_ncl\>/case_nocall/g;s/\<fam_aff_vrt\>/case_heterozygous/g;s/\<fam_aff_homv\>/case_homozygous/g;s/\<fam_naf_wild\>/control_WT/g;s/\<fam_naf_ncl\>/control_nocall/g;s/\<fam_naf_vrt\>/control_heterozygous/g;s/\<fam_naf_homv\>/control_homozygous/g;s/glb_aff_vrt_samp/case_heterozygous_ID/g;s/glb_aff_homv_samp/case_homozygous_ID/g;s/glb_naf_vrt_samp/control_heterozygous_ID/g;s/glb_naf_homv_samp/control_homozygous_ID/g;s/glb_aff_altaf/case_AF/g;s/glb_naf_altaf/control_AF/g;s/glb_aff_wild_samp/case_WT_ID/g;s/glb_aff_ncl_samp/case_nocall_ID/g;s/glb_naf_wild_samp/control_WT_ID/g;s/glb_naf_ncl_samp/control_nocall_ID/g' -i {preOutfile_temp}"
    os.system(cmd_sed)
    #
    cmd_rename = f'mv {preOutfile_temp}  {preOutfile} '
    os.system(cmd_rename)
elif len(ped.iloc[:,0].unique())==1:
    print('############')
    print('NOTE: Pipeline run single family')
    print('############')
    cmd_parse_1 =  f'head -n 1 {preOutfile}'
    cmd_parse_2 = "awk -F'\t' '{for (i=1; i<=NF; i++) if ($i~/(glb_aff_wild?$|glb_aff_ncl?$|glb_aff_vrt?$|glb_aff_homv?$|glb_naf_wild?$|glb_naf_ncl?$|glb_naf_vrt?$|glb_naf_homv?$|nfm_aff_wild?$|nfm_aff_ncl?$|nfm_aff_vrt?$|nfm_aff_homv?$|nfm_naf_wild?$|nfm_naf_ncl?$|nfm_naf_vrt?$|nfm_naf_homv?$)/) print $i,i}'"
    #
    pIn  = subprocess.Popen(cmd_parse_1, stdout=subprocess.PIPE, shell=True)
    pOut = io.StringIO(subprocess.check_output(cmd_parse_2, stdin=pIn.stdout, shell=True, text=True).rstrip())
    PandasDataFrameDict = pd.read_table(pOut, sep=' ', header=None).to_dict(orient='list')
    #
    cmd_cut = 'cut ' + '--complement'+' ' +'-f' +''.join([f'{fam},' for fam in  PandasDataFrameDict[1][:-1]])  + f'{PandasDataFrameDict[1][-1]}' + f' {preOutfile} > {preOutfile_temp}'
    os.system(cmd_cut)
    #
    cmd_rm = f'rm -rf {preOutfile} '
    os.system(cmd_rm)
    #
    cmd_sed = f"sed 's/\<fam_aff_wild\>/affected_WT/g;s/\<fam_aff_ncl\>/affected_nocall/g;s/\<fam_aff_vrt\>/affected_heterozygous/g;s/\<fam_aff_homv\>/affected_homozygous/g;s/\<fam_naf_wild\>/unaffected_WT/g;s/\<fam_naf_ncl\>/unaffected_nocall/g;s/\<fam_naf_vrt\>/unaffected_heterozygous/g;s/\<fam_naf_homv\>/unaffected_homozygous/g;s/\<glb_aff_vrt_samp\>/affected_heterozygous_ID/g;s/\<glb_aff_homv_samp\>/affected_homozygous_ID/g;s/\<glb_naf_vrt_samp\>/unaffected_heterozygous_ID/g;s/\<glb_naf_homv_samp\>/unaffected_homozygous_ID/g;s/\<glb_aff_altaf\>/affected_AF/g;s/\<glb_naf_altaf\>/unaffected_AF/g;s/\<glb_aff_wild_samp\>/affected_WT_ID/g;s/\<glb_aff_ncl_samp\>/affected_nocall_ID/g;s/\<glb_naf_wild_samp\>/unaffected_WT_ID/g;s/\<glb_naf_ncl_samp\>/unaffected_nocall_ID/g' -i {preOutfile_temp}"
    os.system(cmd_sed)
    #
    cmd_rename = f'mv {preOutfile_temp}  {preOutfile} '
    os.system(cmd_rename)
else:
    print('############')
    print('NOTE: Pipeline run multiple family')
    print('############')
    cmd_parse_1 =  f'head -n 1 {preOutfile}'
    cmd_parse_2 = "awk -F'\t' '{for (i=1; i<=NF; i++) if ($i~/(nfm_aff_wild?$|nfm_aff_ncl?$|nfm_aff_vrt?$|nfm_aff_homv?$|nfm_naf_wild?$|nfm_naf_ncl?$|nfm_naf_vrt?$|nfm_naf_homv?$|nfm_aff_wild_samp?$|nfm_aff_ncl_samp?$|nfm_aff_vrt_samp?$|nfm_aff_homv_samp?$|nfm_naf_wild_samp?$|nfm_naf_ncl_samp?$|nfm_naf_vrt_samp?$|nfm_naf_homv_samp?$|glb_aff_wild_samp?$|glb_aff_wild_samp?$|glb_aff_ncl_samp?$|glb_aff_vrt_samp?$|glb_aff_homv_samp?$|glb_naf_wild_samp?$|glb_naf_ncl_samp?$|glb_naf_vrt_samp?$|glb_naf_homv_samp?$)/) print $i,i}'"
    #
    pIn  = subprocess.Popen(cmd_parse_1, stdout=subprocess.PIPE, shell=True)
    pOut = io.StringIO(subprocess.check_output(cmd_parse_2, stdin=pIn.stdout, shell=True, text=True).rstrip())
    PandasDataFrameDict = pd.read_table(pOut, sep=' ', header=None).to_dict(orient='list')
    #
    cmd_cut = 'cut ' + '--complement'+' ' +'-f' +''.join([f'{fam},' for fam in  PandasDataFrameDict[1][:-1]])  + f'{PandasDataFrameDict[1][-1]}' + f' {preOutfile} > {preOutfile_temp}'
    os.system(cmd_cut)
    #
    cmd_rm = f'rm -rf {preOutfile} '
    os.system(cmd_rm)
    #
    cmd_sed = f"sed 's/\<fam_aff_wild\>/family_affected_WT/g;s/\<fam_aff_ncl\>/family_affected_nocall/g;s/\<fam_aff_vrt\>/family_affected_heterozygous/g;s/\<fam_aff_homv\>/family_affected_homozygous/g;s/\<fam_naf_wild\>/family_unaffected_WT/g;s/\<fam_naf_ncl\>/family_unaffected_nocall/g;s/\<fam_naf_vrt\>/family_unaffected_heterozygous/g;s/\<fam_naf_homv\>/family_unaffected_homozygous/g;s/\<glb_aff_wild\>/total_affected_WT/g;s/\<glb_aff_ncl\>/total_affected_nocall/g;s/\<glb_aff_vrt\>/total_affected_heterozygous/g;s/\<glb_aff_homv\>/total_affected_homozygous/g;s/\<glb_naf_wild\>/total_unaffected_WT/g;s/\<glb_naf_ncl\>/total_unaffected_nocall/g;s/\<glb_naf_vrt\>/total_unaffected_heterozygous/g;s/\<glb_naf_homv\>/total_unaffected_homozygous/g;s/fam_aff_vrt_samp/family_affected_heterozygous_ID/g;s/fam_aff_homv_samp/family_affected_homozygous_ID/g;s/fam_naf_vrt_samp/family_unaffected_heterozygous_ID/g;s/fam_naf_homv_samp/family_unaffected_homozygous_ID/g;s/glb_aff_altaf/affected_AF/g;s/glb_naf_altaf/unaffected_AF/g;s/fam_aff_wild_samp/family_affected_WT_ID/g;s/fam_aff_ncl_samp/family_affected_nocall_ID/g;s/fam_aff_wild_samp/family_unaffected_WT_ID/g;s/fam_naf_ncl_samp/family_unaffected_nocall_ID/g;s/\<fam_naf_wild_samp\>/family_unaffected_WT_ID/g' -i {preOutfile_temp}"
    os.system(cmd_sed)
    #
    cmd_rename = f'mv {preOutfile_temp}  {preOutfile}'
    os.system(cmd_rename)


# Drop duplicated columns
def duplicates(n):
     counter=collections.Counter(n)
     dups=[i for i in counter if counter[i]!=1] 
     result={}
     for item in dups:
             result[item]=[i for i,j in enumerate(n) if j==item] 
     return result

def rm_dup(x,i):
    try:
        return(x.remove(i))
    except:
        return(x)

fline=open(preOutfile).readline().rstrip()

dup_dic=duplicates(fline.split('\t'))
flat_list=[]
for i in list(dup_dic.keys()):
    for x in dup_dic[i]:
        flat_list.append(x)
flat_list.sort()

rm_dup(flat_list,0)
rm_dup(flat_list,1)
rm_dup(flat_list,2)

flat_list=[i+1 for i in flat_list]

cmd_drop_dup = 'cut ' + '--complement'+' ' +'-f' +''.join([f'{fam},' for fam in  flat_list[:-1]])  + f'{flat_list[-1]}' + f' {preOutfile} > {preOutfile_temp}'
os.system(cmd_drop_dup)

cmd_mv = f'mv {preOutfile_temp} {preOutfile}'
os.system(cmd_mv)

print(f'Step2 - renaming step terminated')
print('############')
print('Total time to achieve: {}'.format(datetime.now() - start_time0))
print('############################################')

print(f'Step2 terminated')
print('############')
print('Total time to achieve: {}'.format(datetime.now() - start_time0))
print('############################################')

session_info.show()
