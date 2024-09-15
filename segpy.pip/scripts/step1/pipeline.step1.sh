#!/bin/bash

umask 002
echo timestamp $(date +%s)
source $PIPELINE_HOME/tools/utils.sh
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini

if [[ $QUEUE =~ bash ]]; then
   call_parameter $1
fi

echo "*******************************************"
echo "* step 1: generate Matrix file"
echo "*******************************************"
echo "* PIPELINE HOME:        $PIPELINE_HOME"
# echo "* SPARK HOME:           $SPARK_PATH"
# echo "* Virtual ENV:          $ENV_PATH"
# echo "* Python version:       $PYTHON_CMD"
echo "* OUTPUT_DIR:           $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* GRCH:                 $GRCH"
echo "* JAVATOOLOPTIONS:      ${JAVATOOLOPTIONS}"
echo "*******************************************"

#-----------------------------------------------------#
# Step1: Create Matrix                                     #
#-----------------------------------------------------#
# export SPARK_HOME=$SPARK_PATH
export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
# export PYSPARK_SUBMIT_ARGS=$PYSPARKSUBMITARGS
# source ${OUTPUT_DIR}/configs/segpy.config.ini
# if [[ $QUEUE =~ sbatch ]]; then
#    if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
# fi
# if [[ $QUEUE =~ sbatch ]]; then
#    module load ${JAVA_CMD}/${JAVA_VERSION}
# fi

# ${SPARK_HOME}/sbin/start-master.sh

# if [[ ${CONTAINER} =~ False ]]; then 
#    source ${ENV_PATH}/bin/activate
# fi

# echo "PYTHON_LIB_PATH"
# echo $PYTHON_LIB_PATH
# export PYTHONPATH=$PYTHON_LIB_PATH
# module load $PYTHON_MODULE
export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}
# echo $JAVATOOLOPTIONS

file2=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${file2%.*}.mt

# if [[ ${CONTAINER} =~ False ]]; then 
   # ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step1/step1.py $MTFILE  $VCF $GRCH
# else
#   ${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step1/step1.py $MTFILE  $VCF $GRCH
# fi

VCF_PATH=$(dirname $VCF)

if [[ $QUEUE =~ bash ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
   # CONTAINER1=$PIPELINE_HOME/soft/container/scrnabox.sif
   # CONTAINER1=/home/sam/seg_cont/segr_cont.img
   CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif
   PIPELINE_HOME_CONT=/opt/segpy.pip
   $CONTAINER_CMD exec  --bind  $OUTPUT_DIR,$VCF_PATH ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step1/step1.py  $MTFILE  $VCF $GRCH
   exit 0
fi

#--------------
#--------------
if [[ $QUEUE =~ sbatch ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
   if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
   if [[ $CONTAINER_MODULE ]]; then module load $CONTAINER_MODULE ; fi
   CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif
   PIPELINE_HOME_CONT=/opt/segpy.pip
   $CONTAINER_CMD exec  --bind  $OUTPUT_DIR,$VCF_PATH ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step1/step1.py  $MTFILE  $VCF $GRCH
   exit 0
fi 
