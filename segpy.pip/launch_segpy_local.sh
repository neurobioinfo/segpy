#!/bin/bash

# ===============================================
# setup run environment, variables and functions
# ===============================================
#
# declare -A THREADS_ARRAY
# declare -A  WALLTIME_ARRAY
# declare -A  MEM_ARRAY
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $PIPELINE_HOME/tools/utils.sh
unset FOUND_ERROR

CSQ=${CSQ_VEP}

MODE0=$MODE
if [[ "$MODE" == *"-"* ]]; then
  abc0=`echo $MODE | sed  "s/-/../g"  | awk '{print "{"$0"}"}'`
  MODE0=`eval echo $abc0`
else 
  MODE0=$MODE
fi

# - set local error messages and exit codes
fail_exit_code=42
msg_fail_VCF="ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"
msg_fail_PED="ERROR: missing mandatory option for steps 1-3: -p (--ped) empty, not specified or does not exist"

TIMESTAMP() { date +%FT%H.%M.%S; }
# helper functions:
# - for step logging
LOGGING() { 
    read launch_log version step <<< $@
    echo -e "\n---------------------------------------------------"  >> $launch_log
    echo -e "-------- Job submitted using pipeline ${version} -------" >> $launch_log
    echo -e "-------------------------------------------------"  >> $launch_log
    echo "$step submitted at `date +%FT%H.%M.%S`"  >> $launch_log
}

LOGOUT() {
    read launch_log output_dir step <<< $@
    echo "-------------------------------------------" >> $launch_log
    echo "The Output is under ${output_dir}/${step}" >> $launch_log
    echo "-------------------------------------------" >> $launch_log
}

LOGGINGFOLLOW() {
    read launch_log version step stepfollow <<< $@
    echo -e "\n---------------------------------------------------"  >> $launch_log
    echo -e "--------Job submitted using pipeline ${version}-------" >> $launch_log
    echo -e "-------------------------------------------"  >> $launch_log
    echo "$step submitted following $stepfollow at `date +%FT%H.%M.%S`"  >> $launch_log
}

# ===============================================
# STEP 1: create hail MatrixTable folder from vcf
# ===============================================

echo "Please leave the pipeline undisturbed until it finishes."
STEP=step1

if [[  ${MODE0[@]} =~ 1 ]] ; then
  if [  -d $OUTPUT_DIR/step1/ ]; then 
    rm -rf  $OUTPUT_DIR/step1/ ; mkdir -p $OUTPUT_DIR/step1/ &
  else
    mkdir -p $OUTPUT_DIR/step1/ &
  fi 
    # if [[(! -s $VCF) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
    # die if input file(s) missing or empty    
    [[ ! -s $VCF ]] && FOUND_ERROR=1
    [[ ! -s $VCF ]] && echo ${msg_fail_VCF}
    [[ $FOUND_ERROR ]] && exit ${fail_exit_code}

    # log general step info
    LOGGING $LAUNCH_LOG $VERSION $STEP
    $QUEUE $PIPELINE_HOME/scripts/step1/pipeline.step1.sh --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},GRCH=${GRCH}  &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    LOGOUT $LAUNCH_LOG $OUTPUT_DIR $STEP
fi 


# ===============================================
# STEP 2: Run segregation
# ===============================================
#
STEP=step2

if [[  ${MODE0[@]}  =~  2 ]]  &&  [[  ${MODE0[@]} =~ 1 ]] ; then
    if [  -d $OUTPUT_DIR/step2/ ]; then 
        rm -rf  $OUTPUT_DIR/step2/ ; mkdir -p $OUTPUT_DIR/step2/ &
    else
        mkdir -p $OUTPUT_DIR/step2/ &
    fi 
    # if [[ (! -s $VCF) && (! -s $PED) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
     # die if input file(s) missing or empty
    # unset FOUND_ERROR
    [[ ! -s $VCF || ! -s $PED ]] && FOUND_ERROR=1
    [[ ! -s $VCF ]] && echo ${msg_fail_VCF}
    [[ ! -s $PED ]] && echo ${msg_fail_PED}
    [[ $FOUND_ERROR ]] && exit ${fail_exit_code}
    
    depend_other scripts/step1/pipeline.step1.sh
    LOGGINGFOLLOW $LAUNCH_LOG $VERSION $STEP step1
    $QUEUE $PIPELINE_HOME/scripts/step2/pipeline.step2.sh --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM},AFFECTEDS_ONLY=${AFFECTEDS_ONLY},FILTER_VARIANT=${FILTER_VARIANT} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    # echo "-------------------------------------------" >> $LAUNCH_LOG
    # echo "The Output is under ${OUTPUT_DIR}/step2" >> $LAUNCH_LOG 
    LOGOUT $LAUNCH_LOG $OUTPUT_DIR $STEP
elif [[  ${MODE0[@]}  =~  2  ]]  &&  [[  ${MODE0[@]} != 1 ]]; then
    if [  -d $OUTPUT_DIR/step2/ ]; then 
        rm -rf  $OUTPUT_DIR/step2/ ; mkdir -p $OUTPUT_DIR/step2/ &
    else
        mkdir -p $OUTPUT_DIR/step2/ &
    fi 
    LOGGING $LAUNCH_LOG $VERSION $STEP
    $QUEUE $PIPELINE_HOME/scripts/step2/pipeline.step2.sh --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM},AFFECTEDS_ONLY=${AFFECTEDS_ONLY},FILTER_VARIANT=${FILTER_VARIANT} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 

    LOGOUT $LAUNCH_LOG $OUTPUT_DIR $STEP
fi 

# ===============================================
# STEP 3: Final cleanup and formatting
# ===============================================
#
STEP=step3

if [[  ${MODE0[@]}  =~  3 ]]  &&  [[  ${MODE0[@]} =~ 2 ]] ; then
  if [  -d $OUTPUT_DIR/step3/ ]; then 
    rm -rf  $OUTPUT_DIR/step3/ ; mkdir -p $OUTPUT_DIR/step3/ &
  else
    mkdir -p $OUTPUT_DIR/step3/ &
  fi 
  depend_other scripts/step1/pipeline.step1.sh
  depend_other scripts/step2/pipeline.step2.sh
  LOGGINGFOLLOW $LAUNCH_LOG $VERSION $STEP step2  
  $QUEUE $PIPELINE_HOME/scripts/step3/pipeline.step3.sh --export=PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S)
  # echo "-------------------------------------------" >> $LAUNCH_LOG
  # echo "The Output is under ${OUTPUT_DIR}/step3" >> $LAUNCH_LOG 
  LOGOUT $LAUNCH_LOG $OUTPUT_DIR $STEP
elif [[  ${MODE0[@]}  =~  3  ]]  &&  [[  ${MODE0[@]} != 2 ]]; then
  if [  -d $OUTPUT_DIR/step3/ ]; then 
    rm -rf  $OUTPUT_DIR/step3/ ; mkdir -p $OUTPUT_DIR/step3/ &
  else
    mkdir -p $OUTPUT_DIR/step3/ &
  fi 
  LOGGING $LAUNCH_LOG $VERSION $STEP
  $QUEUE $PIPELINE_HOME/scripts/step3/pipeline.step3.sh --export=PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 

  LOGOUT $LAUNCH_LOG $OUTPUT_DIR $STEP
fi

echo "The pipeline terminated."
exit 0

