salloc -A rrg-grouleau-ac --time=0-1 -c 2 --mem=20g
base_hail=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail
export SPARK_HOME=$base_hail/spark-3.1.3-bin-hadoop3.2
export SPARK_LOG_DIR=$HOME
module load java/11.0.2
${SPARK_HOME}/sbin/start-master.sh
source ${base_hail}/hail_env2/bin/activate
export PYTHONPATH=$base_hail/hail_env2/lib/python3.10/site-packages
module  load python/3.10.2  
${base_hail}/hail_env2/bin/python3.10

import os 
import pandas as pd
import sys
import hail as hl

mt=hl.import_vcf('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VEP_iPSC.vcf',force=True,reference_genome='GRCh38',array_elements_required=False)
ped=pd.read_csv('/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/iPSC_2.ped',sep='\t')
outfolder= '/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_segpy'
vcffile='/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VEP_iPSC.vcf'
ncol=7

from segpy import seg
seg.run(mt, ped, outfolder,hl,ncol,vcffile)   

from segpy import parser
parser.clean_seg(outfolder)  

cd ${SPARK_HOME}; ./sbin/stop-master.sh


