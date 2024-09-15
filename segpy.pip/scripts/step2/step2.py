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

print('############################################')
print('Step2 started:')
start_time0 = datetime.now()
print('Local time: ', time.strftime("%Y-%m-%d %H:%M:%S"))

from segpy import seg

mt              = hl.read_matrix_table(sys.argv[1])
# mt=hl.split_multi(mt)
mt=hl.split_multi_hts(mt)
ped             =pd.read_csv(sys.argv[2],sep='\t')
outfolder       =sys.argv[3]
# ncol=int(sys.argv[4])
CSQ             =sys.argv[4]
vcffile         =sys.argv[5]
sparkmem        = sys.argv[6]
if sparkmem != "False": hl.init(spark_conf={'spark.driver.memory': sparkmem})
affecteds_only  = sys.argv[7]
filter_variant  = sys.argv[8]
# just_phenotype=sys.argv[8]
# info_required=eval(sys.argv[9])
# seg.run(mt,ped,outfolder,hl,vcffile,ncol,CSQ)
# print(info_required)
# seg.run(mt, ped, outfolder, hl, vcffile, ncol, CSQ, just_phenotype, info_required)
# print(mt)
# print(ped)
# print(outfolder)
# print(hl)
# print(vcffile)
# print(CSQ)
# print(affecteds_only)
seg.run(mt, ped, outfolder, hl, vcffile, CSQ, affecteds_only, filter_variant)
# cmd_mv = f'cp ./finalseg.csv /step2'
# os.system(cmd_mv)
print(f'Step3 terminated')
print('############')
print('Total time to achieve: {}'.format(datetime.now() - start_time0))
print('############################################')

session_info.show()
