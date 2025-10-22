# Segpy configuration parameters
The `configs` directory produced after initiating the Segpy pipeline (step 0) contains the `segpy.config.ini`, which contains execution parameters that users must modify prior to running their analysis. 

The `segpy.config.ini` can be modified using the following command:

```
# 1) Open .ini file to edit with nano
nano $PWD/configs/segpy.config.ini

# 2) Make appropriate changes.

# 3) Save and exit the .ini file with ctrl+0, enter ,ctrl+x
```

The following parameters are adjustable for the Segpy pipeline:

| Parameter   |      Default      |  Explanation |
|----------|:-------------|:------|
|CONTAINER_MODULE | CONTAINER_MODULE='apptainer/1.2.4' | The version of Singularity/Apptainer loaded onto your system.|
|ACCOUNT|ACCOUNT=user| Your SLURM user account.|
| CSQ_VEP | CSQ=TRUE | Whether or not to include variant annotations from VEP in the output file. |
|GRCH| GRCH=GRCh38 | Reference genome version (GRCh38 or GRCh37).|
|AFFECTEDS_ONLY|AFFECTEDS_ONLY=FALSE| Whether or not to only include families with at least one affected individual.|
|FILTER_VARIANT|FILTER_VARIANT=TRUE| Filter the output file using relevant variant count values. See [Step 3: Parse output file](segpy_local.md#step-3-parse-output-file) for more information.|
|RETRIEVE_SAMPLE_ID|RETRIEVE_SAMPLE_ID=TRUE| Whether or not to retain SampleIDs in the final output file. |
|JAVATOOLOPTIONS|JAVATOOLOPTIONS="-Xmx6g"| Java Virtual Machine (JVM) configuration setting. For most use cases the default value will be appropriate.|
|WALLTIME_ARRAY["step1"]|WALLTIME_ARRAY["step1"]=00-5:00 | Number of CPUs for the step 1 job sumission. |
|THREADS_ARRAY["step1"]|THREADS_ARRAY["step1"]=8| Amount of memory (RAM) for the step 1 job sumission. |
|MEM_ARRAY["step1"]|MEM_ARRAY["step1"]=10g| Amount of time for the step 1 job sumission.|
|WALLTIME_ARRAY["step2"]|WALLTIME_ARRAY["step2"]=00-5:00 | Number of CPUs for the step 2 job sumission. |
|THREADS_ARRAY["step2"]|THREADS_ARRAY["step2"]=8| Amount of memory (RAM) for the step 2 job sumission. |
|MEM_ARRAY["step2"]|MEM_ARRAY["step2"]=10g| Amount of time for the step 2 job sumission.|
|WALLTIME_ARRAY["step3"]|WALLTIME_ARRAY["step3"]=00-5:00 | Number of CPUs for the step 3 job sumission. |
|THREADS_ARRAY["step3"]|THREADS_ARRAY["step3"]=8| Amount of memory (RAM) for the step 3 job sumission. |
|MEM_ARRAY["step3"]|MEM_ARRAY["step3"]=10g| Amount of time for the step 3 job sumission.|




