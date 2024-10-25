# Installation
A containerized version of the Segpy pipeline is publicly available from **Zenodo**, which includes the code, libraries, and dependicies required for running the analyses. The container is compatible with both High-Performance Computing (HPC) systems and standard Linux workstations.

To use the Segpy pipeline, the folowing must be installed on your system:

-  [Apptainer](#apptainer)
-  [segpy.pip](#segpypip)

 - - - -

### Apptainer
`segpy.pip` is packaged and tested with [Apptainer](https://apptainer.org/) (formerly Singularity) version 1.2.4. Before proceeding, ensure that Apptainer/Singularity is installed on your system. If you are using an HPC system, Apptainer is likely already installed, and you will simply need to load the module. If you encounter any issues while loading the Apptainer module, please contact your system administrator. Before running the Segpy pipeline, load the Apptainer module using the following command:

```
# Load Apptainer
module apptainer/1.2.4
```

 - - - -

### Segpy.pip
To download the latest version of Segpy run the following command:

```
# Download the Segpy container
#curl "https://zenodo.org/records/12751010/files/scrnabox.slurm.zip?download=1" --output segpy.pip.zip

# Unzip the Segpy container
unzip segpy.pip.zip
```

To ensure that `segpy.pip` is installed properly, run the following command:

```
bash /path/to/segpy.pip/launch_segpy.sh -h
```

If `segpy.pip` is installed properly, the above command should return the folllowing:

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

After successfully installing `segpy.pip` we can proceed with the segregation analysis. 

**[⬆ back to top](#installation)**