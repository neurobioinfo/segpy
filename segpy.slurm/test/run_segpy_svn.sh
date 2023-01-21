## segrun.svn
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/segpy.svn
PWD=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/run_segpy_svn
VCF=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/VCF_y.vcf
PED=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSCy/data/iPSC_PBMC2.ped
```

#### step1: Setup
First run runs the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segrun.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 1
```

#### Step 2:  Create table matrix
The following code, import VCF as a MatrixTable, 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF}
```

#### Step 3: Run the segregation 
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

### Note
You can easily run step 1 to 3 to gether, see below 
```
sh $PIPELINE_HOME/launch_pipeline.segpy.sh \
-d ${PWD} \
--steps 2-4 \
--vcf ${VCF} \
--ped ${PED} 
```