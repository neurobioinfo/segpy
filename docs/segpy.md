# Segpy
The following steps show how to run the segregation pipeline using seg module.

|<img src="https://raw.githubusercontent.com/neurobioinfo/segpy/main/segpy.png" width="500" height="400"/>|
|:--:|
| _segpy workflow_ |


## Contents
-  [Step 1: Run Spark](#Step-1-Run-Spark)
-  [Step 2: Create table matrix](#Step-2-Create-table-matrix)
-  [Step 3: Run segregation](#Step-3-Run-segregation)
-  [Step 4: Parsing](#Step-4-Parsing)
-  [Step 5: Shut down spark](#Step-5-Shut-down-spark)

### Step 1: Run Spark 
First activate Spark on your system 
```
export SPARK_HOME=$HOME/spark-3.1.3-bin-hadoop3.2
export SPARK_LOG_DIR=$HOME/temp
module load java/11.0.2
cd ${SPARK_HOME}; ./sbin/start-master.sh
```

### Step 2:  Create table matrix
Next, initialize the hail and import your vcf file and write it as a matrix table, the matrix table is a data structure to present the genetic data as a matrix. In the below, we import the vcf file and write it as `MatrixTable`, then read your matrix table.
For the tutorial, we add data to test the pipeline [https://github.com/The-Neuro-Bioinformatics-Core/segpy/data]. The pipeline is explained using this dataset. 

The following code imports VCF as a MatrixTable: 
```
import sys
import pandas as pd 
import hail as hl
hl.import_vcf('~/test/data/VEP.iPSC.vcf',force=True,reference_genome='GRCh38',array_elements_required=False).write('~/test/output/VEP.iPSC.mt', overwrite=True)
mt = hl.read_matrix_table('~/test/output/VEP.iPSC.mt')
```

### Step 3: Run segregation
Run the following codes to generate the segregation. 
```
from segpy import seg
ped=pd.read_csv('~/test/data/iPSC_2.ped'.ped',sep='\t')
destfolder= '~/test/output/'
vcffile='~/test/data/VEP.iPSC.vcf'
ncol=7
CSQ=True
seg.run(mt,ped,outfolder,hl,ncol,CSQ,vcffile)    
```
It generates two files `header.txt` and [`finalseg.csv`](FAQ.md) in the  `destfolder`; `header.txt`  includes the header of information in `finalseg.csv`. The  
output  of `finalseg.csv` can be categorized to  1) locus and alleles, 2) CSQ, 3) Global- Non-Affected 4) Global-Affected,  5) Family, 6) Family-Affected 7) Family - Non-affected.  If you do not want to have CSQ in the output file, choose `CSQ=False`. 

### Step 4: Parsing
If you want to parse the file, run the following codes, it drops the un-necessary characters ", [, ], etc from the output.    
```
from segpy import parser
parser.clean_general(outfolder)  
```

The info includes several info, to drop the multiplicity run the following code 
```
parser.clean_unique(outfolder)  
```

### Step 5:  Shut down spark  
Do not forget to deactivate environment and stop the spark: 
```
cd ${SPARK_HOME}; ./sbin/stop-master.sh
```


## Todo

**[⬆ back to top](#contents)**
