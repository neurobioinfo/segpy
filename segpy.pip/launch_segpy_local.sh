#!/bin/bash

# ===============================================
# setup run environment, variables and functions
# ===============================================

# - source configs and utility functions
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $PIPELINE_HOME/tools/utils.sh

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

# helper functions:
# - for step logging
LOGGING() { 
    read launch_log version step <<< $@
    date +%FT%H.%M.%S >> $launch_log
    echo -e "\n-------------------------------------------"  >> $launch_log
    echo -e "--------Job submitted using pipeline-------" $version >> $launch_log
    echo -e "-------------------------------------------"  >> $launch_log
    echo "$step submitted"  >> $launch_log
}

# ===============================================
# STEP 1: create hail MatrixTable folder from vcf
# ===============================================

if [[  ${MODE0[@]} =~ 1 ]] ; then

    STEP=step1
    STEP_DIR=${OUTPUT_DIR}/$step

    # remove STEP_DIR if it exists, and create it empty
    [[ -d ${STEP_DIR} ]] && rm -rf ${STEP_DIR}
    mkdir -p ${STEP_DIR}

    # die if input file(s) missing or empty
    [[ ! -s $VCF  ]] && echo ${msg_fail_VCF} && exit ${fail_exit_code}
    
    # log general step info
    LOGGING $LAUNCH_LOG $VERSION $STEP
    echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
    
    # launch step command
    $QUEUE $PIPELINE_HOME/scripts/step1/pipeline.step1.sh --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},GRCH=${GRCH}  &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S)

fi 

# ===============================================
# STEP 2: Run segregation engine
# ===============================================

if [[  ${MODE0[@]}  =~  2 ]]; then 

    STEP=step2
    STEP_DIR=${OUTPUT_DIR}/$step

    # remove STEP_DIR if it exists, and create it empty
    [[ -d ${STEP_DIR} ]] && rm -rf ${STEP_DIR}
    mkdir -p ${STEP_DIR}

    # die if input file(s) missing or empty
    unset FOUND_ERROR
    [[ ! -s $VCF || ! -s $PED ]] && FOUND_ERROR=1
    [[ ! -s $VCF ]] && echo ${msg_fail_VCF}
    [[ ! -s $PED ]] && echo ${msg_fail_PED}
    [[ $FOUND_ERROR ]] && exit ${fail_exit_code}

    # log general step info
    LOGGING $LAUNCH_LOG $VERSION $STEP
    echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 
    
    # launch step command
    $QUEUE $PIPELINE_HOME/scripts/step2/pipeline.step2.sh --export=PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_CMD=${PYTHON_CMD},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},CSQ=${CSQ},SPARKMEM=${SPARKMEM} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S)

fi

# ===============================================
# STEP 3: Final cleanup and formatting
# ===============================================

if [[  ${MODE0[@]}  =~  3 ]]; then

    STEP=step3
    STEP_DIR=${OUTPUT_DIR}/$step

    # remove STEP_DIR if it exists, and create it empty
    [[ -d ${STEP_DIR} ]] && rm -rf ${STEP_DIR}
    mkdir -p ${STEP_DIR}

    # log general step info
    LOGGING $LAUNCH_LOG $VERSION $STEP
    echo "The Output is under ${OUTPUT_DIR}/" >> $LAUNCH_LOG 

    # launch step command
    $QUEUE $PIPELINE_HOME/scripts/step3/pipeline.step3.sh --export=PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_CMD=${PYTHON_CMD},CLEAN=${CLEAN} &> $OUTPUT_DIR/logs/jobs/${STEP}.$(date +%FT%H.%M.%S)

fi
