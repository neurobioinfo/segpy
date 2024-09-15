# Segpy on workstation
`segpy.pip` can be used to executing on Linux workstation. Below, we illustrate the code to submit jobs for (steps 0 to 3) of the pipeline on Linux workstation. 

## Contents
- [Step 0: Setup](#step-0-setup)
- [Step 1: Create table matrix](#step-1-create-table-matrix)
- [Step 2: Run segregation](#step-2-run-segregation)
- [Step 3: Clean final data](#step-3-parsing)
- [Note](#note)

The following flowchart illustrates the steps for running the segregation analysis on Linux workstation.

|<img src="https://raw.githubusercontent.com/neurobioinfo/segpy/main/segpy_pip.png" width="200" height="400"/>|
|:--:|
| _segpy.pip local workflow_ |

To execute the pipeline, you require 1) the path of the pipeline (PIPELINE_HOME), 2) the working directory, 3) the VCF file, and 4) the PED file.

```
export PIPELINE_HOME=~/segpy.pip
PWD=~/outfolder
VCF=~/data/VEP_iPSC.vcf
PED=~/data/iPSC.ped
```

### Step 0: Setup
Initially, execute the following code to set up the pipeline. You can modify the parameters in ${PWD}/job_output/segpy.config.ini.

```
sh $PIPELINE_HOME/launch_segpy.sh \
-d ${PWD} \
--steps 0 
```

The parameters are: 

| Parameter   |      default      |  Explanation |
|----------|:-------------|:------|
|CSQ | CSQ=TRUE | include CSQ information in the output by setting CSQ=TRUE. To exclude CSQ from the output, set CSQ=FALSE |
|GRCH| GRCH=GRCh38 | set the reference genome|
|AFFECTEDS_ONLY|AFFECTEDS_ONLY=FALSE| include all families with at least one affected sample if affecteds_only=TRUE|
|FILTER_VARIANT|FILTER_VARIANT=TRUE| filter the output file using relevant counting column values where  'fam_aff_vrt'+'fam_aff_homv'+'fam_naf_vrt'+'fam_naf_homv' >0.|
|SPARKMEM|SPARKMEM="16g"|Amount of memory to use for the driver process, i.e. where SparkContext is initialized. Look at spark.driver.memory of "spark.apache" |
|JAVATOOLOPTIONS|JAVATOOLOPTIONS="-Xmx6g"|specify JVM arguments as an environment variable. Look at "JAVA_TOOL_OPTIONS" Environment Variable|


### Step 1: Create table matrix
The following code, create  MatrixTable from the VCF file.

```
sh $PIPELINE_HOME/launch_segpy.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

### Step 2: Run segregation 
Execute the following code to generate the segregation. 
```
sh $PIPELINE_HOME/launch_segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

### Step 3: Parsing
To parse the file and remove unnecessary characters such as ", [, ], etc., run the following code.

```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--parser general
```

The following code eliminates duplicate information in CSQ. 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--parser unique
```

### Note
You can execute steps 1 to 3 sequentially, as illustrated below.

```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1-3 \
--vcf ${VCF} \
--ped ${PED} \
--parser general
```

**[⬆ back to top](#contents)**
