#!/usr/bin/env python

####################
# step3 
import numpy as np 
import sys
import pandas as pd 
import hail as hl
hl.init(spark_conf={'spark.driver.memory': sys.argv[6]})
from segpy import seg
mt = hl.read_matrix_table(sys.argv[1])
outfolder=sys.argv[2]
ped=pd.read_csv(sys.argv[3],sep='\t')
vcffile=sys.argv[4]
ncol=int(sys.argv[5])
seg.run(mt, ped,outfolder,hl,ncol,vcffile)

