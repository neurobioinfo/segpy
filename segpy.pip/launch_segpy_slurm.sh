#!/bin/bash
# ===============================================
# setup run environment, variables and functions
# ===============================================
# - initialize slurm resource arrays
declare -A THREADS_ARRAY
declare -A  WALLTIME_ARRAY
declare -A  MEM_ARRAY
unset FOUND_ERROR
# - source configs and utility functions
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $PIPELINE_HOME/tools/utils.sh
CSQ=${CSQ_VEP}

if [[ $MODULEUSE ]]; then export MODULEUSE=$MODULEUSE ; fi

# - parse run mode from launch_segpy.sh:
# - convert hyphenated input range to bash brace expansion
# - e.g: turn "1-3" into "1 2 3" via use of `eval echo {1..3}`

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

LOGGINGFOLLOW() { 
    read launch_log version step stepfollow <<< $@
    echo -e "\n---------------------------------------------------"  >> $launch_log
    echo -e "-------- Job submitted using pipeline ${version}-------" >> $launch_log
    echo -e "-------------------------------------------"  >> $launch_log
    echo "$step submitted following $stepfollowat `date +%FT%H.%M.%S`"  >> $launch_log
}

LOGOUT() {
    read launch_log output_dir step <<< $@
    echo "-------------------------------------------" >> $launch_log
    echo "The Output is under ${output_dir}/${step}" >> $launch_log
    echo "-------------------------------------------" >> $launch_log
}


# MODE0=$MODE
# ===============================================
# STEP 1: create hail MatrixTable folder from vcf
# ===============================================

STEP=step1
if [[  ${MODE0[@]} =~ 1 ]] ; then
  if [  -d $OUTPUT_DIR/step1/ ]; then 
    rm -rf  $OUTPUT_DIR/step1/ ; mkdir -p $OUTPUT_DIR/step1/ &
  else
    mkdir -p $OUTPUT_DIR/step1/ &
  fi 
  if [ -z "${THREADS_ARRAY[$STEP]}" ]; then
      THREADS=4 
  else
      THREADS=${THREADS_ARRAY[$STEP]}
  fi
  if [ -z "${MEM_ARRAY[$STEP]}" ]; then
      MEM=25g 
  else 
      MEM=${MEM_ARRAY[$STEP]}
  fi
  if [ -z "${WALLTIME_ARRAY[$STEP]}" ]; then
      WALLTIME=00-01:00
  else
      WALLTIME=${WALLTIME_ARRAY[$STEP]}
  fi
  export THREADS=$THREADS
  export WALLTIME=$WALLTIME
  export MEM=$MEM

  [[ ! -s $VCF ]] && FOUND_ERROR=1
  [[ ! -s $VCF ]] && echo ${msg_fail_VCF}
  [[ $FOUND_ERROR ]] && exit ${fail_exit_code}

   # log general step info
    LOGGING $LAUNCH_LOG $VERSION $STEP
  
  export ACCOUNT=$ACCOUNT
  step_1="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM}  \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},GRCH=${GRCH} \
    --output $OUTPUT_DIR/logs/jobs/%x.o%j \
    $PIPELINE_HOME/scripts/step1/pipeline.step1.sh"
  echo -e "Submitted job and its number:"
  step_1=$($step_1 | grep -oP "\d+")
  echo "[Q] STEP 1        : $step_1 " >> $LAUNCH_LOG
  echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
  DEPEND_step_1="--dependency=afterok:$step_1"
  echo step_1:$step_1
fi 


# ===============================================
# STEP 2: Run segregation
# ===============================================
#
STEP=step2
  if [ -z "${THREADS_ARRAY[$STEP]}" ]; then
      THREADS=4 
  else
      THREADS=${THREADS_ARRAY[$STEP]}
  fi
  if [ -z "${MEM_ARRAY[$STEP]}" ]; then
      MEM=17g 
  else 
      MEM=${MEM_ARRAY[$STEP]}
  fi
  if [ -z "${WALLTIME_ARRAY[$STEP]}" ]; then
      WALLTIME=00-02:00
  else
      WALLTIME=${WALLTIME_ARRAY[$STEP]}
  fi
  export THREADS=$THREADS
  export WALLTIME=$WALLTIME
  export MEM=$MEM
if [[  ${MODE0[@]}  =~  2 ]]  &&  [[  ${MODE0[@]} =~ 1 ]] ; then
  if [  -d $OUTPUT_DIR/step2/ ]; then 
    rm -rf  $OUTPUT_DIR/step2/ ; mkdir -p $OUTPUT_DIR/step2/ &
  else
    mkdir -p $OUTPUT_DIR/step2/ &
  fi 
    [[ ! -s $VCF || ! -s $PED ]] && FOUND_ERROR=1
    [[ ! -s $VCF ]] && echo ${msg_fail_VCF}
    [[ ! -s $PED ]] && echo ${msg_fail_PED}
    [[ $FOUND_ERROR ]] && exit ${fail_exit_code}
     LOGGINGFOLLOW $LAUNCH_LOG $VERSION $STEP step1
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_1 \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM},AFFECTEDS_ONLY=${AFFECTEDS_ONLY},FILTER_VARIANT=${FILTER_VARIANT} \
    --output $OUTPUT_DIR/logs/jobs/%x.o%j \
    $PIPELINE_HOME/scripts/step2/pipeline.step2.sh"
  step_2=$($step_2 | grep -oP "\d+")
  echo "[Q] STEP 2         : $step_2 " >> $LAUNCH_LOG
  echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
  DEPEND_step_2="--dependency=afterok:$step_2"
  echo step_2:$step_2
elif [[  ${MODE0[@]}  =~  2  ]]  &&  [[  ${MODE0[@]} != 1 ]]; then
  if [  -d $OUTPUT_DIR/step2/ ]; then 
    rm -rf  $OUTPUT_DIR/step2/ ; mkdir -p $OUTPUT_DIR/step2/ &
  else
    mkdir -p $OUTPUT_DIR/step2/ &
  fi 
  LOGGING $LAUNCH_LOG $VERSION $STEP
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM},AFFECTEDS_ONLY=${AFFECTEDS_ONLY},FILTER_VARIANT=${FILTER_VARIANT} \
    --output $OUTPUT_DIR/logs/jobs/%x.o%j \
    $PIPELINE_HOME/scripts/step2/pipeline.step2.sh"
  step_2=$($step_2 | grep -oP "\d+")
  echo "[Q] STEP 2         : $step_2 " >> $LAUNCH_LOG 
  echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
  DEPEND_step_2="--dependency=afterok:$step_2"
  echo step_2:$step_2
fi 


# ===============================================
# STEP 3: Final cleanup and formatting
# ===============================================
#
STEP=step3
if [ -z "${THREADS_ARRAY[$STEP]}" ]; then
    THREADS=4 
else
    THREADS=${THREADS_ARRAY[$STEP]}
fi
if [ -z "${MEM_ARRAY[$STEP]}" ]; then
    MEM=4g 
else 
    MEM=${MEM_ARRAY[$STEP]}
fi
if [ -z "${WALLTIME_ARRAY[$STEP]}" ]; then
    WALLTIME=00-02:00
else
    WALLTIME=${WALLTIME_ARRAY[$STEP]}
fi
export THREADS=$THREADS
export WALLTIME=$WALLTIME
export MEM=$MEM
if [[  ${MODE0[@]}  =~  3 ]]  &&  [[  ${MODE0[@]} =~ 2 ]] ; then
  if [  -d $OUTPUT_DIR/step3/ ]; then 
    rm -rf  $OUTPUT_DIR/step3/ ; mkdir -p $OUTPUT_DIR/step3/ &
  else
    mkdir -p $OUTPUT_DIR/step3/ &
  fi 
  LOGGINGFOLLOW $LAUNCH_LOG $VERSION $STEP step2  
  step_3="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_2 \
    --export PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} \
    --output $OUTPUT_DIR/logs/jobs/%x.o%j \
    $PIPELINE_HOME/scripts/step3/pipeline.step3.sh"
  step_3=$($step_3 | grep -oP "\d+")
  echo "[Q] STEP 3         : $step_3 " >> $LAUNCH_LOG
  echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
  DEPEND_step_3="--dependency=afterok:$step_3"
  echo step_3:$step_3
elif [[  ${MODE0[@]}  =~  3  ]]  &&  [[  ${MODE0[@]} != 2 ]]; then
  if [  -d $OUTPUT_DIR/step3/ ]; then 
    rm -rf  $OUTPUT_DIR/step3/ ; mkdir -p $OUTPUT_DIR/step3/ &
  else
    mkdir -p $OUTPUT_DIR/step3/ &
  fi 
  LOGGING $LAUNCH_LOG $VERSION $STEP
  step_3="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} \
    --output $OUTPUT_DIR/logs/jobs/%x.o%j \
    $PIPELINE_HOME/scripts/step3/pipeline.step3.sh"
  step_3=$($step_3 | grep -oP "\d+")
  echo "[Q] STEP 3         : $step_3 " >> $LAUNCH_LOG 
  echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
  DEPEND_step_3="--dependency=afterok:$step_3"
  echo step_3:$step_3
fi

exit 0
