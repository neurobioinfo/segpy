salloc -A rrg-grouleau-ac --time=0-5 -c 6 --mem=20g
base_hail=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail
export SPARK_HOME=$base_hail/spark-3.1.2-bin-hadoop3.2
export SPARK_LOG_DIR=$HOME
module load java/11.0.2
${SPARK_HOME}/sbin/start-master.sh
source ${base_hail}/hail_env/bin/activate
# ${SPARK_HOME}/sbin/stop-master.sh 
export PYTHONPATH=$base_hail/hail_env/lib/python3.8/site-packages
module  load python/3.8.10  
${base_hail}/hail_env/bin/python3.8 
# ${base_hail}/hail_env/bin/python3.8 -m pip install /home/samamiri/runs/samamiri/general_files/hail/segpy/

import os 
import pandas as pd
import sys
import hail as hl
# hl.import_vcf(sys.argv[1],force=True,reference_genome='GRCh38',array_elements_required=False).write(sys.argv[2], overwrite=True)

mt=hl.import_vcf('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VCF_y.vcf',force=True,reference_genome='GRCh38',array_elements_required=False)
# mt = hl.read_matrix_table('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VCF_y.mt')
#### with sole phenotype
ped=pd.read_csv('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/iPSC_PBMC1.ped',sep='\t')
outfolder= '/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_pyseg'
vcffile='/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VCF_y.vcf'
ncol=7

from segpy import seg
seg.run(mt, ped, outfolder,hl,ncol,vcffile)   

from segpy import parser
header_need='/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_pyseg/header.txt'
parser.sub_seg(outfolder, header_need)


#### with two phenotype
ped=pd.read_csv('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/iPSC_PBMC2.ped',sep='\t')
outfolder= '/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_pyseg'
vcffile='/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VCF_y.vcf'
ncol=7

from segpy import seg
seg.run(mt, ped, outfolder,hl,ncol,vcffile)   

from segpy import parser
header_need='/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_pyseg/header.txt'
parser.sub_seg(outfolder, header_need)

