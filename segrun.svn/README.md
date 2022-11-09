# segrun.svn: A pipeline for segregation analysis
***

## Contents
- [segrun.svn]
 - setup 
 - step 1 
 - step 2 
 - step 3

## segrun.svn
To run the pipepline, you need 1) path of the pipeline (PIPELINE_HOME), 2) Working directory , 3) VCF, and 4) PED file
```
export PIPELINE_HOME=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/segrun.svn
PWD=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSC
VCF=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSC/VCF_xy.vcf
PED=/lustre03/project/6004655/COMMUN/runs/samamiri/general_files/hail/practiceiPSC/iPSC_PBMC.ped
```

#### Setup
First run runs the following code to setup the pipeline, you can change the the parameters in ${PWD}/job_output/segrun.config.ini
```
sh $PIPELINE_HOME/launch_pipeline.segrun.sh \
-d ${PWD} \
--steps 0
```

#### Step 1:  Create table matrix
The following code, import VCF as a MatrixTable, 
```
sh $PIPELINE_HOME/launch_pipeline.segrun.sh \
-d ${PWD} \
--steps 1 \
--vcf ${VCF}
```

#### Step 2: Run the segregation 
```
sh $PIPELINE_HOME/launch_pipeline.segrun.sh \
-d ${PWD} \
--steps 2 \
--vcf ${VCF} \
--ped ${PED}  
```

#### Step 3: Clean final data
```
sh $PIPELINE_HOME/launch_pipeline.segrun.sh \
-d ${PWD} \
--steps 3 
```

### Note
You can easily run step 1 to 3 to gether, see below 
```
sh $PIPELINE_HOME/launch_pipeline.segrun.sh \
-d ${PWD} \
--steps 1-3 \
--vcf ${VCF} \
--ped ${PED} 
```



## Contributing
This is an early version, any contribute or suggestion is appreciated.

## Changelog
Every release is documented on the [GitHub Releases page](https://github.com/The-Neuro-Bioinformatics-Core/seganalysis/releases).

## License
This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/The-Neuro-Bioinformatics-Core/seganalysis/blob/main/LICENSE) file for details


**[⬆ back to top](#contents)**