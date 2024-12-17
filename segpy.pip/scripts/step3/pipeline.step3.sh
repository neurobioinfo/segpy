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
echo "* step 3: clean data"
echo "*******************************************"
echo "* OUTPUT_DIR:           $OUTPUT_DIR"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* CLEAN:                $CLEAN"
echo "* SPARKMEM:             $SPARKMEM"
echo "*******************************************"

#-----------------------------------------------------#
# Step 3: Clean Output file                           #
#-----------------------------------------------------#
# 


if [[ -z $CLEAN  ]]; then
   echo "The user did not specify the --parser flag, so the pipeline defaulted to using the general parser."
   CLEAN=general
    exit 0
fi

if [[ $CLEAN =~ unique ]]; then
    export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
    export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}
fi

# [[ -z $SPARKMEM ]] && SPARKMEM="False"
if [[ -z $SPARKMEM ]]; then  SPARKMEM="False"; fi


if [[ $QUEUE =~ bash ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
   CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif
   PIPELINE_HOME_CONT=/opt/segpy.pip
   $CONTAINER_CMD exec  --bind  $OUTPUT_DIR ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM
   exit 0
fi
#--------------
#--------------
if [[ $QUEUE =~ sbatch ]] && [[ $CONTAINER =~ TRUE ]]; then 
   if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
   if [[ $CONTAINER_MODULE ]]; then module load $CONTAINER_MODULE ; fi
   CONTAINER_PATH=$PIPELINE_HOME/soft/segpy.sif
   PIPELINE_HOME_CONT=/opt/segpy.pip
   $CONTAINER_CMD exec  --bind  $OUTPUT_DIR ${CONTAINER_PATH} python3 $PIPELINE_HOME_CONT/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM
   exit 0
fi 
