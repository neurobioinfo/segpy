#!/usr/bin/env python

####################
# step1
## Create Matrix 

import sys
import hail as hl
hl.import_vcf(sys.argv[2],force=True,reference_genome=sys.argv[3],array_elements_required=False).write(sys.argv[1], overwrite=True)

