## segrun.slurm
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file.
```
export PIPELINE_HOME=~/segpy.pip
PWD=~/working_dir
VCF=~/VEP_iPSC.vcf
PED=~/iPSC_multiple.ped
```

#### step 0: Setup
First, run the following code to setup the pipeline. You can change the the parameters in ${PWD}/job_output/segrun.config.ini
```
module load apptainer/1.2.4
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 0 \
--analysis_mode multiple_family \
--jobmode slurm
```
Where analysis_mode is one of single_family, multiple_family, or case-control depending on the study design.

#### Step 1:  Create table matrix
The following code imports the VCF file as a MatrixTable: 
```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 1 \
--vcf $VCF
```

#### Step 2: Run the segregation 
The following code runs the segregation analysis:
```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 2 \
--vcf $VCF
--ped $PED
```

#### Step 3: Clean final data
The following code cleans up the final data file:
```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 3 \
--parser general
```
Where parser is one of general or unique.

### Note
You can easily run step 1 to 3 using the following code 
```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 1-3 \
--vcf $VCF \
--ped $PED \
--parser general
```
