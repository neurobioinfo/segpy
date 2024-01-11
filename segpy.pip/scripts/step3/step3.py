#!/usr/bin/env python

####################
# step 3
import numpy as np 
import sys
import pandas as pd 
# import hail as hl
outfolder=sys.argv[1]
clean_m=sys.argv[2]

from segpy import parser

import os 
out_dir = os.path.expanduser(outfolder)

if (clean_m=='general'):
    parser.clean(os.path.join(out_dir, 'step2'),method='general')
    cmd_prune1=f'mv {outfolder}/step2/finalseg_modified_general.csv {outfolder}/step3'
    os.system(cmd_prune1)

if (clean_m=='unique'):
    parser.clean(os.path.join(out_dir, 'step2'),method='unique')
    cmd_prune1=f'mv {outfolder}/step2/finalseg_modified_uniq.csv {outfolder}/step3'
    os.system(cmd_prune1)
