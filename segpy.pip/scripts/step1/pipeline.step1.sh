#!/bin/bash

umask 002
echo timestamp $(date +%s)
source $PIPELINE_HOME/tools/utils.sh
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
CSQ=${CSQ_VEP}

if [[ $QUEUE =~ bash ]]; then
   call_parameter $1
fi

echo "*******************************************"
echo "* step 1: generate Matrix file"
echo "*******************************************"
echo "* PIPELINE HOME:        $PIPELINE_HOME"
echo "* OUTPUT_DIR:           $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* GRCH:                 $GRCH"
echo "* JAVATOOLOPTIONS:      ${JAVATOOLOPTIONS}"
echo "*******************************************"

#-----------------------------------------------------#
# Step1: Create Matrix                                     #
#-----------------------------------------------------#
export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}

file2=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${file2%.*}.mt

VCF_PATH=$(dirname $VCF)

if [[ $QUEUE =~ bash ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
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
