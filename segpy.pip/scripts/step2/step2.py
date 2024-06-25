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
from segpy import seg

print('############################################')
print('Step2 started:')
start_time0 = datetime.now()
print('Local time: ', time.strftime("%Y-%m-%d %H:%M:%S"))

# parse input arguments
mt              = hl.read_matrix_table(sys.argv[1])
ped             = pd.read_csv(sys.argv[2],sep='\t')
outfolder       = sys.argv[3]
CSQ             = sys.argv[4]
vcffile         = sys.argv[5]
sparkmem        = sys.argv[6]
affecteds_only  = sys.argv[7]

# set custom spark memory if given as argument
if sparkmem != "False": hl.init(spark_conf={'spark.driver.memory': sparkmem})

# run
seg.run(mt, ped, outfolder, hl, vcffile, CSQ, affecteds_only)

print(f'Step3 terminated')
print('############')
print('Total time to achieve: {}'.format(datetime.now() - start_time0))
print('############################################')

session_info.show()
