# segpy.slurm: A scheduler to run sepy under HPC
`segpy.slurm` is a shield developed to run the segpy pipeline in HPC system slurm to submit jobs (step 0 to step 3), it has been used under [Beluga](https://docs.alliancecan.ca/wiki/B%C3%A9luga), an HPC that uses slurm system, the detail of using it is discussed in [segpy.svn](https://github.com/neurobioinfo/segpy/tree/main/segpy.svn). 

## Contents
- [segpy.svn](#segpy.svn)
  - [Step 0: Setup](#step0:-setup)
  - [Step 1: Create table matrix](#step1:-create-table-matrix)
  - [step 2: Run segregation](#step2:-run-segregation)
  - [step 3: clean final data](#step3:-clean-final-data)
  - [Note](#note)

## segpy.slurm
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=~/segpy.slurm
PWD=~/outfolder
VCF=~/data/VEP_iPSC.vcf
PED=~/data/iPSC_2.ped
```

#### Step 0: Setup
First run the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segpy.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 0
```


#### Step 1: Create table matrix
The following code, create  MatrixTable from the VCF file
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

#### Step 2: Run segregation 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

#### Step 3: Clean final data
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--clean general 
```

#### Note
You can easily run step 1 to 3 together, see below 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1-3 \
--vcf ${VCF} \
--ped ${PED} \
--clean general 
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/The-Neuro-Bioinformatics-Core/segpy/blob/main/LICENSE) file for details

## Acknowledgement
The pipeline is done as a project by Neuro Bioinformatics Core, it is developed by [Saeid Amiri](https://github.com/saeidamiri1) with associate of Dan Spiegelman and Sali Farhan. 

**[⬆ back to top](#contents)**