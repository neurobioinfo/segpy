# Adjustable execution parameters for the segregation pipeline
- [Introduction](#introduction)
- [Segpy parameters](#segpy-parameters)
- - - -

## Introduction
The configs/ directory contains the segpy.config.ini file which allows users to specify the parameters of interest explained below 
## Segpy parameters
`ACCOUNT` Specify user name for slurm module. <br />
`SPARK_PATH` Environment variables to point to the correct Spark executable <br />
`ENV_PATH` Environment variables to point to the correct Python executable <br />
`PYTHON_CMD=python3.10` <br />
`MODULEUSE` The path to the environmental module <br />
`JAVA_CMD=java` <br /> 
`JAVA_VERSION=11.0.2` <br /> Specify the version of Java
`NCOL=7` To control usage of memory to process CSQ.  <br />
`CSQ=True` To process CSQ in the output, Consequence annotations from Ensembl VEP.   <br />
`GRCH=GRCh38` Genome Reference Consortium Human <br />
`SPARKMEM="16g"` Spark Memory <br />
`JAVATOOLOPTIONS="-Xmx8g"` Java Memory and any other options can be added to here.  <br />
#### [step 1] Create table matrix
`WALLTIME_ARRAY["step_1"]=00-01:00`  Set a limit on the total run time of the job allocation in the step 1 under slurm. <br />
`THREADS_ARRAY["step_1"]=4` Request the maximum ntasks be invoked on each core in the step 1 under slurm. <br />
`MEM_ARRAY["step_1"]=25g` Specify the real memory required per node in the step 1 under slurm.  <br />
#### [step 2] Run segregation 
`WALLTIME_ARRAY["step_2"]=00-02:00 ` Set a limit on the total run time of the job allocation in the step 2 under slurm.  <br />
`THREADS_ARRAY["step_2"]=4` Request the maximum ntasks be invoked on each core in the step 2 under slurm. <br />
`MEM_ARRAY["step_2"]=17g` Specify the real memory required per node in the step 2 under slurm. <br />
`INFO_REQUIRED=[1,2,3,4]` One can determine the desired content to be included in the output <br />
 1: Global affected, 2: Global unaffected, 3: family-wise, 4: phenotype-family-wise, 5: phenotype-family-wise and non-include, 6: phenotype-family-wise-multipe sample, 7: phenotype-family-wise-multipe sample and non-include
#### [step 3] Parsing 
`WALLTIME_ARRAY["step_3"]=00-01:00` Set a limit on the total run time of the job allocation in the step 3 under slurm.  <br />
`THREADS_ARRAY["step_3"]=4` Request the maximum ntasks be invoked on each core in the step 3 under slurm. <br />
`MEM_ARRAY["step_3"]=4g` Specify the real memory required per node in the step 3 under slurm.  <br />
