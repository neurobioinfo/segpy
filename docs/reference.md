# Adjustable execution parameters for the segregation pipeline
- [Introduction](#introduction)
- [Segpy slurm](#step-parameters)
- [Segpy local](#differential-gene-expression-contrast-matrices)
- - - -

## Introduction

## Segpy slurm parameters

├── ACCOUNT

├── SPARK_PATH: 
Environment variables to point to the correct Spark executable
├── ENV_PATH
Environment variables to point to the correct Python executable
├── PYTHON_CMD=python3.10

├── MODULEUSE

├── JAVA_CMD=java
├── JAVA_VERSION=11.0.2
├── NCOL=7

├── CSQ=True 
GRCH=GRCh38
# Spark Memory
├── SPARKMEM="16g"
# Java Memory
├── JAVATOOLOPTIONS="-Xmx8g"
###  step 1
├── WALLTIME_ARRAY["step_1"]=00-01:00 

├── THREADS_ARRAY["step_1"]=4

├── MEM_ARRAY["step_1"]=25g

### [step2] segpy run 
├── WALLTIME_ARRAY["step_2"]=00-02:00 

├── THREADS_ARRAY["step_2"]=4

├── MEM_ARRAY["step_2"]=17g

### [step3] clean 
├── WALLTIME_ARRAY["step_3"]=00-01:00 

├── THREADS_ARRAY["step_3"]=4

├── MEM_ARRAY["step_3"]=4g


## Segpy local parameters
