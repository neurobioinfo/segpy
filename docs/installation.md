# Installation
The pipeline is containerized and can be run using Singularity, eliminating the need to install modules within the pipeline. It is compatible with both High-Performance Computing (HPC) systems and standard Linux workstations.

## Contents
-  [Step 1: Apptainer](#apptainer)
-  [Step 2: Download](#download)
-  [Step 3: Run](#run)

### Apptainer
`segpy.pip`  is packaged and tested with Apptainer (formerly known as Singularity) version 1.2.4. Ensure that Apptainer/Singularity is installed on your system before proceeding.

### Download
Download the pipeline from Zenodo, which includes the segregated image.

```
????????
```

### Run
To test the pipeline, execute the following code

``` 
bash ~/segpy.pip/launch_segpy.sh -h
```

If you see the following the pipeline is functioning correctly.

```
------------------------------------
segregation pipeline version 0.0.3 is loaded

-------------------
Usage:  /home/sam/seg_cont/segpy003/segpy.pip/launch_segpy.sh [arguments]
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
                --jobmode  = The default for the pipeline is local. If you want to run the pipeline on slurm system, use slurm as the argument.
                --parser             = 'general': to general parsing, 'unique': drop multiplicities
                -v  (--vcf)      = VCF file (mandatory for steps 1-3)
                -p  (--ped)      = PED file (mandatory for steps 1-3)
                -V  (--verbose)      = verbose output

```

**[⬆ back to top](#contents)**