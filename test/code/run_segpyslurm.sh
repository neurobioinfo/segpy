## segrun.sslurm
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/segpy.slurm
export PWD=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_segpy.slurm
export VCF=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VEP_iPSC.vcf
export PED=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/iPSC_2.ped
```

#### step1: Setup
First run runs the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segrun.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 0
```

#### Step 1:  Create table matrix
The following code, import VCF as a MatrixTable, 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

#### Step 2: Run the segregation 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

You can run Steps 1 and 2 using 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1-2 \
--vcf ${VCF} \
--ped ${PED}  
```

#### Step 3: Clean final data
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 3
```

### Note
You can easily run step 1 to 3 using the following code 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1-3 \
--vcf ${VCF} \
--ped ${PED}
```