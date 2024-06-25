#!/usr/bin/env python

####################
# step1
## Create Matrix 

import sys
import hail as hl
import session_info
import time
from datetime import datetime

print('############################################')
print('Step1 started:')
start_time0 = datetime.now()
print('Local time: ', time.strftime("%Y-%m-%d %H:%M:%S"))
print('############################################')

mt_file     = sys.argv[1]
vcf_file    = sys.argv[2]
ref_file    = sys.argv[3]

hl.import_vcf(vcf_file, force=True, reference_genome=ref_file, array_elements_required=False).write(mt_file, overwrite=True)

print(f'Step1 terminated')
print('############')
print('Total time to achieve: {}'.format(datetime.now() - start_time0))
print('############################################')
session_info.show()
