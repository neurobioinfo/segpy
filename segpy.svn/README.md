# segpy.svn: A pipeline for segregation analysis
***

## Contents
- [segpy.svn](#segpy.svn)
  - [Step 1: Setup](#step1:-setup)
  - [Step 2: Create table matrix](#step2:-create-table-matrix)
  - [step 3: Run segregation](#step3:-run-segregation)
  - [step 4: clean final data](#step4:-clean-final-data)
  - [Note](#note)

## segpy.svn
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=~/segpy.svn
PWD=~/outfolder
VCF=~/data/VEP_iPSC.vcf
PED=~/data/iPSC_2.ped
```

#### Step1: Setup
First run the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segpy.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1
```

#### Step 2: Create table matrix
The following code, create  MatrixTable from the VCF file
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF}
```

#### Step 3: Run segregation 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3 \
--vcf ${VCF} \
--ped ${PED}  
```

#### Step 4: Clean final data
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 4 
```

#### Note
You can easily run step 1 to 3 together, see below 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2-4 \
--vcf ${VCF} \
--ped ${PED} 
```

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/The-Neuro-Bioinformatics-Core/segpy/blob/main/LICENSE) file for details


**[⬆ back to top](#contents)**