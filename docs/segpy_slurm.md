# Segpy.slurm
`segpy.slurm` is a shield developed to run the segpy pipeline in HPC system (slurm) to submit jobs (step 0 to step 3), it has been used under [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga), an HPC that uses slurm system. 



## Contents
- [Step 0: Setup](#step-0-setup)
- [Step 1: Create table matrix](#step-1-create-table-matrix)
- [Step 2: Run segregation](#step-2-run-segregation)
- [Step 3: Clean final data](#step-3-clean-final-data)


The following followchart show the step of running the segregation analying usning `segpy_slurm`

|<img src="https://raw.githubusercontent.com/neurobioinfo/segpy/main/segpy_slurm.png" width="300" height="500"/>|
|:--:|
| _segpy.svn workflow_ |

To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=~/segpy.slurm
PWD=~/outfolder
VCF=~/data/VEP_iPSC.vcf
PED=~/data/iPSC_2.ped
```

### Step 0: Setup
First run the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segpy.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 0
```

### Step 1: Create table matrix
The following code, create  MatrixTable from the VCF file
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

### Step 2: Run segregation 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

### Step 3: Clean final data
The following drops the unnecessary characters from the output.
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--clean general
```

The following drops the multiplicities info.
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--clean unique
```

### Note
You can easily run step 1 to 3 together, see below 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1-3 \
--vcf ${VCF} \
--ped ${PED} \
--clean general
```


**[⬆ back to top](#contents)**
