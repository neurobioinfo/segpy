#!/usr/bin/env python

####################
# step 2 
import numpy as np 
import sys
import pandas as pd 
import hail as hl

if sys.argv[7] != "False":
    hl.init(spark_conf={'spark.driver.memory': sys.argv[7]})

from segpy import seg

mt = hl.read_matrix_table(sys.argv[1])
ped=pd.read_csv(sys.argv[2],sep='\t')
outfolder=sys.argv[3]
ncol=int(sys.argv[4])
CSQ=sys.argv[5]
vcffile=sys.argv[6]

seg.run(mt,ped,outfolder,hl,vcffile,ncol,CSQ)
