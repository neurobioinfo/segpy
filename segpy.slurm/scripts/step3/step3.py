#!/usr/bin/env python

####################
# step 2 
import numpy as np 
import sys
import pandas as pd 
# import hail as hl
outfolder=sys.argv[1]
clean=sys.argv[2]

from segpy import parser

if (clean=='F'):
    parser.clean_general(outfolder)

if (clean=='general'):
    parser.clean_general(outfolder)   

if (clean=='unique'):
    parser.clean_unique(outfolder)
