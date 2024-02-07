# Adjustable execution parameters for the segregation pipeline
- [Introduction](#introduction)
- [Segpy slurm](#step-parameters)
- - - -

## Introduction
## Segpy slurm parameters
├── ACCOUNT
Specify user name for slurm module. 
├── SPARK_PATH: 
Environment variables to point to the correct Spark executable
├── ENV_PATH
Environment variables to point to the correct Python executable
├── PYTHON_CMD=python3.10
├── MODULEUSE
The path to the environmental module
├── JAVA_CMD=java
├── JAVA_VERSION=11.0.2
├── NCOL=7
To control usage of memory to process CSQ. 
├── CSQ=True 
To process CSQ in the output, Consequence annotations from Ensembl VEP.  
├── GRCH=GRCh38
Genome Reference Consortium Human
├── SPARKMEM="16g"
Spark Memory
├── JAVATOOLOPTIONS="-Xmx8g"
Java Memory and any other options can be added to here. 
#### step 1
├── WALLTIME_ARRAY["step_1"]=00-01:00 
Set a limit on the total run time of the job allocation in the step 1 under slurm. 
├── THREADS_ARRAY["step_1"]=4
Request the maximum ntasks be invoked on each core in the step 1 under slurm.
├── MEM_ARRAY["step_1"]=25g
Specify the real memory required per node in the step 1 under slurm. 
#### [step2] segpy run 
├── WALLTIME_ARRAY["step_2"]=00-02:00 
Set a limit on the total run time of the job allocation in the step 2 under slurm. 
├── THREADS_ARRAY["step_2"]=4
Request the maximum ntasks be invoked on each core in the step 2 under slurm.
├── MEM_ARRAY["step_2"]=17g
Specify the real memory required per node in the step 2 under slurm.
├──INFO_REQUIRED=[1,2,3,4]
One can specify what specify should be in the output 
# 1 Global affected
# 2 Global unaffected
# 3 family-wise
# 4 phenotype-family-wise
# 5 phenotype-family-wise and non-include
# 6 phenotype-family-wise-multipe sample
# 7 phenotype-family-wise-multipe sample and non-include
### [step3] clean 
├── WALLTIME_ARRAY["step_3"]=00-01:00 
Set a limit on the total run time of the job allocation in the step 3 under slurm. 
├── THREADS_ARRAY["step_3"]=4
Request the maximum ntasks be invoked on each core in the step 3 under slurm.
├── MEM_ARRAY["step_3"]=4g
Specify the real memory required per node in the step 3 under slurm. 
