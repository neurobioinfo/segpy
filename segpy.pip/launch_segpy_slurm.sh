#!/bin/bash

declare -A THREADS_ARRAY
declare -A  WALLTIME_ARRAY
declare -A  MEM_ARRAY
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $PIPELINE_HOME/tools/utils.sh

if [[ $MODULEUSE ]]; then export MODULEUSE=$MODULEUSE ; fi

TIMESTAMP() { date +%FT%H.%M.%S; }

MODE0=$MODE
if [[ "$MODE" == *"-"* ]]; then
  abc0=`echo $MODE | sed  "s/-/../g"  | awk '{print "{"$0"}"}'`
  MODE0=`eval echo $abc0`
else 
  MODE0=$MODE
fi

# MODE0=$MODE
# ===============================================
# STEP 1: 
# ===============================================
#

STEP=step_1
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
  if [[(! -s $VCF) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 1 submitted"  >> $LAUNCH_LOG
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
STEP=step_2
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
   if [[ (! -s $VCF) && (! -s $PED) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 2 submitted following step 1"  >> $LAUNCH_LOG
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_1 \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM} \
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
  echo "just step 2 at" $(TIMESTAMP) >> $LAUNCH_LOG
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 2 submitted (without following  step 1) "  >> $LAUNCH_LOG
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM} \
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
STEP=step_3
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
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted following step 2"  >> $LAUNCH_LOG
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
  echo "just step 3 at" $(TIMESTAMP) >> $LAUNCH_LOG
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted (without following  step 2) "  >> $LAUNCH_LOG
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
