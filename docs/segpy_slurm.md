# Segpy SLURM
In this tutorial we illustrate how to run the Segpy pipeline on a High-Performance Computing (HPC) system using the [SLURM](https://slurm.schedmd.com/) workload manager.

## Contents
- [Input data](#input-data)
- [Step 0: Setup](#step-0-setup)
- [Step 1: VCF to MatrixTable](#step-1-VCF-to-MatrixTable)
- [Step 2: Run segregation](#step-2-run-segregation)
- [Step 3: Parse output file](#step-3-parse-output-file)

The following flowchart illustrates the steps for running the segregation analysis on an HPC system.

 <p align="center">
 <img src="https://github.com/user-attachments/assets/9beb08d2-49cd-41fc-a419-3caca8329c6d" width="450" height="100">
 </p>

**Figure 1. Segpy pipeline workflow.**

 - - - -
### Input data
To execute the pipeline, users must provide two separate input files: <br>

1. **VCF**
2. **Pedigree file**

The **VCF** should be formatted according to the standard VCF specifications, containing information about genetic variants, including their positions, alleles, and genotype information for each individual in the study. <br>

The **Pedigree file** should be in .ped format, structured such that each line describes an individual in the study and includes the following columns: `familyid`, `individualid`, `parentalid`, `maternalid`, `sex`, `phenotype`, facilitating the analysis of inheritance patterns and genetic associations within the family.

 - The `familyid` column must contain identifiers for the family.
 - The `individualid` column must contain identifiers for the individual that match the VCF file.
 - The `parentalid` column must contain identifiers for the father (0 if unknown).
 - The `maternalid` column must contain identifiers for the mother (0 if unknown).
 - The `sex` column must describe the biological sex of the individual (1 = male, 2 = female, 0 = unknown).
 - The `phenotype` column must describe the phenotypic data (1 = unaffected, 2 = affected, -9 = missing).

We provide an example .ped file **HERE**. 

 - - - -

### Step 0: Setup

Prior to initiating the pipeline, users must provide the paths to:

1. The directory containing `segpy.pip` (PIPELINE_HOME)
2. The directory designated for the pipeline's outputs (PWD)
3. The VCF file (VCF)
4. The pedigree file (PED)

Use the following code to define these paths:

```
# Define necessary paths
export PIPELINE_HOME=path/to/segpy.pip
PWD=path/to/outfolder
VCF=path/to/VCF.vcf
PED=path/to/pedigree.ped
```

To ensure that `segpy.pip` was defined properly, run the following command:

```
module load apptainer/1.2.4

bash $PIPELINE_HOME/launch_segpy.sh -h
```

Which should return the following:

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

Once the necessary paths have been defined, we can initialize the pipeline using the following command:

```
module load apptainer/1.2.4

bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 0 \
--jobmode slurm
--analysis_mode cohort_based
```

After running this command, the working directory (PWD) should have the following structure:

```
PWD
├── configs
│   └── segpy.config.ini
├── launch_summary_log.txt
└── logs
    ├── jobs
    └── spark
```

The `configs` directory contains a .ini file with adjustable parameters for the pipeline. Please see **HERE** for more information regarding these parameters. The `logs` directory documents the parameters and outputs from each analytical step of the Segpy pipeline to ensure reproducibility. The `launch_summary_log.txt` is a cumulative documentation of all submitted jobs throughout the analysis.

After completing Step 0, open the `segpy.config.ini` file to adjust the general parameters for the analysis. The following parameters must be adjusted:


| Parameter   |      Default      |  Explanation |
|----------|:-------------|:------|
|CONTAINER_MODULE | CONTAINER_MODULE='apptainer/1.2.4' | The version of Singularity/Apptainer loaded onto your system.|
|ACCOUNT|ACCOUNT=user| Your SLURM user account.|
| CSQ | CSQ=TRUE | Whether or not to include variant annotations from VEP in the output file. |
|GRCH| GRCH=GRCh38 | Reference genome version (GRCh38 or GRCh37).|
|AFFECTEDS_ONLY|AFFECTEDS_ONLY=FALSE| Whether or not to only include families with at least one affected individual.|
|FILTER_VARIANT|FILTER_VARIANT=TRUE| Filter the output file using relevant counting column values where 'fam_aff_vrt'+'fam_aff_homv'+'fam_naf_vrt'+'fam_naf_homv' >0. See [Step 3: Parse output file](#step-3-parse-output-file) for more information.|
|JAVATOOLOPTIONS|JAVATOOLOPTIONS="-Xmx6g"| Java Virtual Machine (JVM) configuration setting. For most use cases the default value will be appropriate.|

Use the following code to modify the `segpy.config.ini` file:

```
# 1) Open .ini file to edit with nano
nano $PWD/configs/segpy.config.ini

# 2) Make appropriate changes.

# 3) Save and exit the .ini file with ctrl+0, enter ,ctrl+x
```

**NOTE**: If you are using Segpy SLURM you must uncomment the `CONTAINER_MODULE` parameter. 

 - - - -

### Step 1: VCF to MatrixTable

In step 1, we will convert the user-provided VCF file to the [Hail MatrixTable](https://hail.is/docs/0.2/overview/matrix_table.html) format, which is designed to efficiently store and manipulate large-scale genomic datasets.

Prior to running step 1, open the `segpy.config.ini` file to adjust the job submission parameters for step 1:

| Parameter   |      Default      |  Explanation |
|----------|:-------------|:------|
|WALLTIME_ARRAY["step1"]|WALLTIME_ARRAY["step1"]=00-5:00 | Number of CPUs for the step 1 job sumission. |
|THREADS_ARRAY["step1"]|THREADS_ARRAY["step1"]=8| Amount of memory (RAM) for the step 1 job sumission. |
|MEM_ARRAY["step1"]|MEM_ARRAY["step1"]=10g| Amount of time for the step 1 job sumission.|

Use the following code to modify the `segpy.config.ini` file:

```
# 1) Open .ini file to edit with nano
nano $PWD/configs/segpy.config.ini

# 2) Make appropriate changes.

# 3) Save and exit the .ini file with ctrl+0, enter ,ctrl+x
```

Once the parameters have been adjusted, run step 1 using the following command:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 1 \
--vcf $VCF
```

After running this command, a `step1` directory will be created in the working directory (PWD), which will contain the output files from Hail. The `step1` directory should have the following structure:

```
step1
└── VEP_iPSC.mt
    ├── cols
    │   ├── metadata.json.gz
    │   ├── README.txt
    │   ├── rows
    │   │   ├── metadata.json.gz
    │   │   └── parts
    │   │       └── part-0
    │   └── _SUCCESS
    ├── entries
    │   ├── metadata.json.gz
    │   ├── README.txt
    │   ├── rows
    │   │   ├── metadata.json.gz
    │   │   └── parts
    │   │       ├── part-0-5eb5d5aa-c7b2-4acf-bea1-b55e6f4d9bff
    │   │       ├── part-1-8ba09e12-618c-416b-8abe-8dd858760e2f
    │   │       └── part-2-7b8e9e61-db1b-4697-8e27-c797f9082545
    │   └── _SUCCESS
    ├── globals
    │   ├── globals
    │   │   ├── metadata.json.gz
    │   │   └── parts
    │   │       └── part-0
    │   ├── metadata.json.gz
    │   ├── README.txt
    │   ├── rows
    │   │   ├── metadata.json.gz
    │   │   └── parts
    │   │       └── part-0
    │   └── _SUCCESS
    ├── index
    │   ├── part-0-5eb5d5aa-c7b2-4acf-bea1-b55e6f4d9bff.idx
    │   │   ├── index
    │   │   └── metadata.json.gz
    │   ├── part-1-8ba09e12-618c-416b-8abe-8dd858760e2f.idx
    │   │   ├── index
    │   │   └── metadata.json.gz
    │   └── part-2-7b8e9e61-db1b-4697-8e27-c797f9082545.idx
    │       ├── index
    │       └── metadata.json.gz
    ├── metadata.json.gz
    ├── README.txt
    ├── references
    ├── rows
    │   ├── metadata.json.gz
    │   ├── README.txt
    │   ├── rows
    │   │   ├── metadata.json.gz
    │   │   └── parts
    │   │       ├── part-0-5eb5d5aa-c7b2-4acf-bea1-b55e6f4d9bff
    │   │       ├── part-1-8ba09e12-618c-416b-8abe-8dd858760e2f
    │   │       └── part-2-7b8e9e61-db1b-4697-8e27-c797f9082545
    │   └── _SUCCESS
    └── _SUCCESS
```

A deatiled description of the outputs can be found in the [Hail documentation](https://hail.is/docs/0.2/index.html)
 - - - -

### Step 2: Run segregation
In step 2, we will leverage the Hail ouputs from step 1 to perform segregation analysis. 

Prior to running step 2, open the segpy.config.ini file to adjust the job submission parameters for step 2:

| Parameter   |      Default      |  Explanation |
|----------|:-------------|:------|
|WALLTIME_ARRAY["step2"]|WALLTIME_ARRAY["step2"]=00-5:00 | Number of CPUs for the step 2 job sumission. |
|THREADS_ARRAY["step2"]|THREADS_ARRAY["step2"]=8| Amount of memory (RAM) for the step 2 job sumission. |
|MEM_ARRAY["step2"]|MEM_ARRAY["step2"]=10g| Amount of time for the step 2 job sumission.|

Use the following code to modify the `segpy.config.ini` file:

```
# 1) Open .ini file to edit with nano
nano $PWD/configs/segpy.config.ini

# 2) Make appropriate changes.

# 3) Save and exit the .ini file with ctrl+0, enter ,ctrl+x
```

Once the parameters have been adjusted, run step 2 using the following command:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 2 \
--vcf $VCF
--ped $PED
--family familyID_1


fam_list = familyID_1

for fam in fam_list:
        ###
        # create family-specific hail.MatrixTables, to be parsed for counts etc. below
        start_time_fam = datetime.now()
        step = f'family_{fam}:generate fam/nfm x aff/naf matrixTables'
        start_time = datetime.now()
        fam_aff_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['fam']['aff'])
        fam_naf_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['fam']['naf'])
        nfm_aff_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['nfm']['aff'])
        nfm_naf_mt = filterMatrixTableBySampleList(mt, sample_dict[fam]['nfm']['naf'])
        timekeeping(step, start_time)



```

After running this command, a `step2` directory will be created in the working directory (PWD), which will contain the output files from the segregation analysis. The `step2` directory should have the following structure:

```
step2
├── finalseg.csv
└── temp
```

The `finalseg.csv` file contains the variant counts obtained from the segregation analysis, as well as the variant annotations supplied by VEP. Please see **HEREEEEEEEEEEEEEEEEEEE** for a comprehensive description of the file contents.  

- - - -

### Step 3: Parse output file
In step 3, we will parse the `finalseg.csv` obtained from step 2 to simplify the outputs.

Prior to running step 3, open the segpy.config.ini file to adjust the job submission parameters for step 3:

| Parameter   |      Default      |  Explanation |
|----------|:-------------|:------|
|WALLTIME_ARRAY["step3"]|WALLTIME_ARRAY["step3"]=00-5:00 | Number of CPUs for the step 3 job sumission. |
|THREADS_ARRAY["step3"]|THREADS_ARRAY["step3"]=8| Amount of memory (RAM) for the step 3 job sumission. |
|MEM_ARRAY["step3"]|MEM_ARRAY["step3"]=10g| Amount of time for the step 3 job sumission.|

Use the following code to modify the `segpy.config.ini` file:

```
# 1) Open .ini file to edit with nano
nano $PWD/configs/segpy.config.ini

# 2) Make appropriate changes.

# 3) Save and exit the .ini file with ctrl+0, enter ,ctrl+x
```

Once the parameters have been adjusted, we can run step 3. If you simply want to remove unnecessary characters such as `"`, `[, ]`, etc., use the following command:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 3 \
--parser general
```

If you want to eliminate duplicated variant entries resulting from VEP annotations, use the following command:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 3 \
--parser unique
```

After running this command, a `step3` directory will be created in the working directory (PWD), which will contain the output files from the segregation analysis. The `step3` directory should have the following structure:

```
step3
└── finalseg_cleaned_general.csv
└── finalseg_cleaned_unique.csv
```

The `finalseg_cleaned_general.csv` and `finalseg_cleaned_unique.csv` files contain the parsed variant counts obtained from the segregation analysis, as well as the variant annotations supplied by VEP. Please see **HEREEEEEEEEEEEEEEEEEEE** for a comprehensive description of the file contents.  

- - - -

**Note**: You can execute steps 1 to 3 sequentially, using the following command:

```
bash $PIPELINE_HOME/launch_segpy.sh \
-d $PWD \
--steps 1-3 \
--vcf $VCF \
--ped $PED \
--parser general
```


**[⬆ back to top](#segpy-slurm)**
