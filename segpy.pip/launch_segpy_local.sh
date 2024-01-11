#!/bin/bash

# ===============================================
# STEP 1: Create hail matrix
# ===============================================
#
declare -A THREADS_ARRAY
declare -A  WALLTIME_ARRAY
declare -A  MEM_ARRAY
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $PIPELINE_HOME/tools/utils.sh

TIMESTAMP() { date +%FT%H.%M.%S; }

MODE0=$MODE
if [[ "$MODE" == *"-"* ]]; then
  abc0=`echo $MODE | sed  "s/-/../g"  | awk '{print "{"$0"}"}'`
  MODE0=`eval echo $abc0`
else 
  MODE0=$MODE
fi

# ===============================================
# STEP 1: 
# ===============================================
#

echo "Please leave the pipeline undisturbed until it finishes."
STEP=step_1

if [[  ${MODE0[@]} =~ 1 ]] ; then
  if [  -d $OUTPUT_DIR/step1/ ]; then 
    rm -rf  $OUTPUT_DIR/step1/ ; mkdir -p $OUTPUT_DIR/step1/ &
  else
    mkdir -p $OUTPUT_DIR/step1/ &
  fi 
  if [[(! -s $VCF) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
    TIMESTAMP  >> $LAUNCH_LOG
    echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
    echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
    echo "-------------------------------------------"  >> $LAUNCH_LOG
    echo "STEP 1 submitted"  >> $LAUNCH_LOG
    $QUEUE $PIPELINE_HOME/scripts/step1/pipeline.step1.qsub --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},GRCH=${GRCH}  &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    echo "-------------------------------------------" >> $LAUNCH_LOG
    echo "The Output is under ${OUTPUT_DIR}/step1" >> $LAUNCH_LOG 
fi 


# ===============================================
# STEP 2: Run segregation
# ===============================================
#
STEP=step_2

if [[  ${MODE0[@]}  =~  2 ]]  &&  [[  ${MODE0[@]} =~ 1 ]] ; then
    if [  -d $OUTPUT_DIR/step2/ ]; then 
        rm -rf  $OUTPUT_DIR/step2/ ; mkdir -p $OUTPUT_DIR/step2/ &
    else
        mkdir -p $OUTPUT_DIR/step2/ &
    fi 
    if [[ (! -s $VCF) && (! -s $PED) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
    depend_other scripts/step1/pipeline.step1.qsub
    TIMESTAMP  >> $LAUNCH_LOG
    echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
    echo -e "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
    echo "-------------------------------------------"  >> $LAUNCH_LOG
    echo "STEP 2 submitted following step 1"  >> $LAUNCH_LOG
    $QUEUE $PIPELINE_HOME/scripts/step2/pipeline.step2.qsub --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    echo "-------------------------------------------" >> $LAUNCH_LOG
    echo "The Output is under ${OUTPUT_DIR}/step2" >> $LAUNCH_LOG 
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
    echo "STEP 2 submitted without step 1"  >> $LAUNCH_LOG
    $QUEUE $PIPELINE_HOME/scripts/step2/pipeline.step2.qsub --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},CSQ=${CSQ},SPARKMEM=${SPARKMEM} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    echo "-------------------------------------------" >> $LAUNCH_LOG
    echo "The Output is under ${OUTPUT_DIR}/step2" >> $LAUNCH_LOG 
fi 

# ===============================================
# STEP 3: Final cleanup and formatting
# ===============================================
#
STEP=step_3

if [[  ${MODE0[@]}  =~  3 ]]  &&  [[  ${MODE0[@]} =~ 2 ]] ; then
  if [  -d $OUTPUT_DIR/step3/ ]; then 
    rm -rf  $OUTPUT_DIR/step3/ ; mkdir -p $OUTPUT_DIR/step3/ &
  else
    mkdir -p $OUTPUT_DIR/step3/ &
  fi 
  depend_other scripts/step1/pipeline.step1.qsub
  depend_other scripts/step2/pipeline.step2.qsub
  TIMESTAMP  >> $LAUNCH_LOG
  echo -e "\n-------------------------------------------"  >> $LAUNCH_LOG
  echo -e  "--------Job submitted using pipeline-------" $VERSION >> $LAUNCH_LOG
  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted following step 2"  >> $LAUNCH_LOG
  $QUEUE $PIPELINE_HOME/scripts/step3/pipeline.step3.qsub --export=PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S)
  echo "-------------------------------------------" >> $LAUNCH_LOG
  echo "The Output is under ${OUTPUT_DIR}/step3" >> $LAUNCH_LOG 
elif [[  ${MODE0[@]}  =~  3  ]]  &&  [[  ${MODE0[@]} != 2 ]]; then
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
  $QUEUE $PIPELINE_HOME/scripts/step3/pipeline.step3.qsub --export=PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S) 
    echo "-------------------------------------------" >> $LAUNCH_LOG
    echo "The Output is under ${OUTPUT_DIR}/step3" >> $LAUNCH_LOG 
fi

echo "The pipeline terminated."
exit 0

