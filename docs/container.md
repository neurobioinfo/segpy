# Container
The pipeline can be run via singularity container  which does not need installing modules in pipeline. 
It can be used on HPC or any workstation.

## Contents
-  [Step 1: Download](#download)
-  [Step 2: Run](#run)

### Download
Donwload the segregration image 
```
singularity pull library://saeidamiri1/mni/seg_cont.sif:latest
```

### Run
Execute ` singularity exec ./seg_cont.sif launch_segpy.sh  -h ` to assure the pipline is working

```
------------------------------------ 
Segregation pipline version 0.2.2.3 

Usage:  /usr/local/bin/launch_segpy.sh [arguments]
        mandatory arguments:
                -d  (--dir)      = Working directory (where all the outputs will be printed) (give full path) 
                -s  (--steps)      = Specify what steps, e.g., 2 to run just step 2, 1-3 (run steps 1 through 3). 'ALL' to run all steps.
                                steps:
                                0: initial setup
                                1: create hail matrix
                                2: run segregation
                                3: final cleanup and formatting

        optional arguments:
                -h  (--help)      = Get the program options and exit.
                --parser             = 'general': to general parsing, 'unique': drop multiplicities 
                -v  (--vcf)      = VCF file (mandatory for steps 1-3)
                -p  (--ped)      = PED file (mandatory for steps 1-3)
                -c  (--config)      = config file [CURRENT: "/usr/local/bin/configs/segpy.config.ini"]
                -V  (--verbose)      = verbose output

```

You can import the data and working directory via `--bind` to container, and the rest is the same as step explain in [segpy local](./segpy_local)

```
singularity exec --bind ~/seg_cont/outfolder ./segr_cont.img launch_segpy.sh -d ~/seg_cont/outfolder/run --steps 0
singularity exec --bind ~/seg_cont/outfolder ./segr_cont.img launch_segpy.sh -d ~/seg_cont/outfolder/run --steps 1 --vcf ~/seg_cont/outfolder/data/VEP_iPSC.vcf
singularity exec --bind ~/seg_cont/outfolder ./segr_cont.img launch_segpy.sh -d ~/seg_cont/outfolder/run --steps 2 --ped ~/seg_cont/outfolder/data/iPSC_2.ped 
singularity exec --bind ~/seg_cont/outfolder ./segr_cont.img launch_segpy.sh -d ~/seg_cont/outfolder/run --steps 3 --parser general 
```

**[⬆ back to top](#contents)**
