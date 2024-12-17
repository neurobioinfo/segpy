#!/bin/bash

umask 002
echo timestamp $(date +%s)
source $PIPELINE_HOME/tools/utils.sh
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
source $OUTPUT_DIR/logs/.tmp/ini_config.ini
CSQ=${CSQ_VEP}

if [[ $QUEUE =~ bash ]]; then
   call_parameter $1
fi

echo "*******************************************"
echo "* step 2: run segregation"
echo "*******************************************"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* DIR:                  $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* PED:                  $PED"
echo "* NCOL:                 $NCOL"
echo "* CSQ:                  $CSQ"
echo "* SPARKMEM:             $SPARKMEM"
echo "* JAVATOOLOPTIONS:      $JAVATOOLOPTIONS"
echo "* AFFECTEDS_ONLY        $AFFECTEDS_ONLY"
echo "* FILTER_VARIANT        $FILTER_VARIANT"
echo "* RETRIEVE_SAMPLE_ID    $RETRIEVE_SAMPLE_ID"
echo "* analysis_mode         $ANA_MODE"
echo "*******************************************"

#-----------------------------------------------------#
# Step 2: Run Segregation                                     #
#-----------------------------------------------------#
export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}

if [[ -z $SPARKMEM ]]; then  SPARKMEM="False"; fi
if [[ -z $NCOL ]]; then  NCOL=7; fi

VCFFILE=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${VCFFILE%.*}.mt

VCF_PATH=$(dirname $VCF)
PED_PATH=$(dirname $PED)

if [[ $QUEUE =~ bash ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
   # CONTAINER1=$PIPELINE_HOME/soft/container/scrnabox.sif
    CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif 
    PIPELINE_HOME_CONT=/opt/segpy.pip 
    $CONTAINER_CMD exec  --bind  $OUTPUT_DIR,$VCF_PATH,$PED_PATH ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $CSQ $VCF $SPARKMEM $AFFECTEDS_ONLY   $FILTER_VARIANT $NCOL $RETRIEVE_SAMPLE_ID $ANA_MODE
   exit 0
fi
#--------------

#--------------
if [[ $QUEUE =~ sbatch ]] && [[ $CONTAINER ]] && [[ $CONTAINER =~ TRUE ]]; then 
   if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
   if [[ $CONTAINER_MODULE ]]; then module load $CONTAINER_MODULE ; fi
   CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif
   PIPELINE_HOME_CONT=/opt/segpy.pip
   $CONTAINER_CMD exec  --bind  $OUTPUT_DIR,$VCF_PATH,$PED_PATH ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $CSQ $VCF $SPARKMEM $AFFECTEDS_ONLY $FILTER_VARIANT $NCOL $RETRIEVE_SAMPLE_ID $ANA_MODE
   exit 0
fi 
