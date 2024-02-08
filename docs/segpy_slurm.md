# Segpy via slurm
`segpy.pip` is a sheild designed for executing the segpy analysis on Linux workstation or HPC system utilizing the Slurm scheduler. Below, we illustrate the code to submit jobs for (steps 0 to 3) of the pipeline on an HPC system utilizing the Slurm scheduler. This pipeline has been employed on [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga), an HPC system utilizing the Slurm system.

## Contents
- [Step 0: Setup](#step-0-setup)
- [Step 1: Create table matrix](#step-1-create-table-matrix)
- [Step 2: Run segregation](#step-2-run-segregation)
- [Step 3: Clean final data](#step-3-clean-final-data)

The following flowchart illustrates the steps for running the segregation analysis on HPC system utilizing the Slurm system.

|<img src="https://raw.githubusercontent.com/neurobioinfo/segpy/main/segpy_pip.png" width="300" height="500"/>|
|:--:|
| _segpy.svn workflow_ |

To execute the pipeline, you require 1) the path of the pipeline (PIPELINE_HOME), 2) the working directory, 3) the VCF file, and 4) the PED file.

```
export PIPELINE_HOME=~/segpy.slurm
PWD=~/outfolder
VCF=~/data/VEP_iPSC.vcf
PED=~/data/iPSC_2.ped
```

### Step 0: Setup
Initially, execute the following code to set up the pipeline. You can modify the parameters in ${PWD}/job_output/segpy.config.ini.

```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 0 \
--mode slurm
```

### Step 1: Create table matrix
The following code, create  MatrixTable from the VCF file.

```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

### Step 2: Run segregation 
Execute the following code to generate the segregation. 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

### Step 3: Clean final data
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
