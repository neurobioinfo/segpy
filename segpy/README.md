# Segpy: A pipline for segregation analysis
***

## Contents
- [introduction](#introduction)
- [How to run](#how-to-run)




## Introduction 
`Segpy` module is developed on Python 3.10.2 to work with annotated VCF file. 
Run [VEP](https://useast.ensembl.org/info/docs/tools/vep/script/vep_tutorial.html) to generate the annotated file. `Segpy` module is developed on top of [Hail, hail==0.2.107](https://hail.is/),  and [spark-3.1.3-bin-hadoop3.2](https://spark.apache.org/downloads.html). Hail module is an open-source, scalable framework for exploring and analyzing genomic data which is a module in Python on the top of Apache Spark. 

## How to run 
#### Step 1: Run Spark 
First activate Spark on your system 
```
export SPARK_HOME=$HOME/spark-3.1.3-bin-hadoop3.2
export SPARK_LOG_DIR=$HOME/temp
module load java/11.0.2
cd ${SPARK_HOME}; ./sbin/start-master.sh
```

#### Step 2:  Create table matrix
The following code, import VCF  and convert to a MatrixTable, 
```
import sys
import pandas as pd 
import hail as hl
hl.import_vcf('~/test/data/VEP.iPSC.vcf',force=True,reference_genome='GRCh38',array_elements_required=False).write('~/test/output/VEP.iPSC.mt', overwrite=True)
mt = hl.read_matrix_table('~/test/output/VEP.iPSC.mt')
```

#### Step 3: Run segregation
Run the following codes to generate the segregation. 
```
from segpy import seg
ped=pd.read_csv('~/test/data/iPSC_2.ped'.ped',sep='\t')
destfolder= '~/test/output/'
vcffile='~/test/data/VEP.iPSC.vcf'
ncol=7
seg.segrun(mt,ped,outfolder,hl,ncol,vcffile)  
```

It generates two files `header.txt` and `finalseg.csv` in the  `destfolder`; `header.txt`  includes the header of information in `finalseg.csv`. The  
output  of `finalseg.csv` can be categorized to  1) locus and alleles, 2) CSQ, 3) Global- Non-Affected 4) Global-Affected,  5) Family, 6) Family-Affected 7) Family - Non-affected.  

##### locus and alleles
locus: chromosome <br/>
alleles:  a variant form of a gene
##### CSQ
VEP put all the requested information in infront CSQ, running  `seg.run()` split CSQ to columns.  
##### Global - Non-Affected
glb_naf_wild:  Global - Non-Affecteds, wildtype<br/>
glb_naf_ncl:     Global - Non-Affecteds, no call  <br/>   
glb_naf_vrt:     Global - Non-Affecteds, with variant    <br/>
glb_naf_homv:    Global - Non-Affecteds, homozygous for ALT allele<br/>
glb_naf_altaf:   Global - Non-Affecteds, ALT allele frequency   <br/>
##### Global - Affected
glb_aff_wild: Global - Affecteds, wildtype <br/>
glb_aff_ncl:     Global - Affecteds, no call    <br/> 
glb_aff_vrt:     Global - Affecteds, with variant  <br/>
glb_aff_homv:    Global - Affecteds, homozygous for ALT allele<br/>
glb_aff_altaf:   Global - Affecteds, ALT allele frequency   <br/>
##### Family
{famid}_wild: Family - Affecteds: wildtype <br/>
{famid}_ncl: Family - Affecteds: no call<br/>
{famid}_vrt: Family - Affecteds: with variant<br/>
{famid}_homv: Family - Affecteds: homozygous for ALT allele<br/>
##### Family - Affected
{famid}_wild_aff: Family - Affecteds: wildtype <br/>
{famid}_ncl_aff: Family - Affecteds: no call<br/>
{famid}_vrt_aff: Family - Affecteds: with variant<br/>
{famid}_homv_aff: Family - Affecteds: homozygous for ALT allele<br/>
##### Family - Nonaffected   
{famid}_wild_naf: Family - Nonaffecteds: wildtype <br/>
{famid}_ncl_naf: Family - Nonaffecteds: no call<br/>
{famid}_vrt_naf: Family - Nonaffecteds: with variant<br/>
{famid}_homv_naf: Family - Nonaffecteds: homozygous for ALT allele<br/>


#### Step 4: Parsing
If you want to parse the file, run the following codes.  
```
from segpy import parser
parser.clean_general(outfolder)
```

#### Step 5:  Shut down spark  
Do not forget to deactivate environment and stop the spark: 
```
cd ${SPARK_HOME}; ./sbin/stop-master.sh
```

## Contributing
This is an early version, any contribute or suggestion is appreciated.

## Changelog
Every release is documented on the [GitHub Releases page](https://github.com/neurobioinfo/segpy/releases).

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/neurobioinfo/segpy/blob/main/LICENSE) file for details

## Acknowledgement
The pipeline is done as a project by Neuro Bioinformatics Core, it is written by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Dan Spiegelman and Sali Farhan. 

**[⬆ back to top](#contents)**