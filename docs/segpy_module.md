# Segpy
The steps outlined below demonstrate the process of executing the segregation pipeline using the seg module.

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
Initially, activate Spark on your system. 

```
export SPARK_HOME=$HOME/spark-3.1.3-bin-hadoop3.2
export SPARK_LOG_DIR=$HOME/temp
module load java/11.0.2
${SPARK_HOME}/sbin/start-master.sh
```

### Step 2:  Create table matrix
Following that, initialize Hail, import your VCF file, and save it as a matrix table. The matrix table serves as a data structure for representing genetic data in matrix form. Below, we import the VCF file, save it as a MatrixTable, and proceed to read your matrix table. In the tutorial, additional data is incorporated to test the pipeline, which can be found at [https://github.com/The-Neuro-Bioinformatics-Core/segpy/data]. This dataset is utilized to illustrate the pipeline's functionality.

The subsequent code imports a VCF file and represents it as a MatrixTable:
```
import sys
import pandas as pd 
import hail as hl
hl.import_vcf('~/test/data/VEP.iPSC.vcf',force=True,reference_genome='GRCh38',array_elements_required=False).write('~/test/output/VEP.iPSC.mt', overwrite=True)
mt = hl.read_matrix_table('~/test/output/VEP.iPSC.mt')
```

### Step 3: Run segregation
Execute the following code to generate the segregation. 
```
from segpy import seg
ped=pd.read_csv('~/test/data/iPSC_2.ped'.ped',sep='\t')
destfolder= '~/test/output/'
vcffile='~/test/data/VEP.iPSC.vcf'
ncol=7
CSQ=True
seg.run(mt,ped,outfolder,hl,ncol,CSQ,vcffile)    
```

Running the provided code generates two files, namely `header.txt` and [`finalseg.csv`](FAQ.md), in the `destfolder`. The `header.txt` file contains the header information found in `finalseg.csv`. The output in `finalseg.csv` is organized into the following categories: 1) locus and alleles, 2) CSQ, 3) Global-Non-Affected, 4) Global-Affected, 5) Family, 6) Family-Affected, and 7) Family-Non-Affected. If you prefer not to include CSQ in the output file, you can select `CSQ=False`.

### Step 4: Parsing
To parse the file and remove unnecessary characters such as ", [, ], etc., run the following code.

```
from segpy import parser
parser.clean_general(outfolder)  
```

The information consists of various components; to eliminate redundancy, execute the following code.

```
parser.clean_unique(outfolder)  
```

### Step 5:  Shut down spark  
Do not forget to deactivate environment and stop the spark: 
```
${SPARK_HOME}/sbin/stop-master.sh
```


## Todo

**[⬆ back to top](#contents)**
