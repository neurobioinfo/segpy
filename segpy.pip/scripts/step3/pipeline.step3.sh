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
echo "* step 3: clean data"
echo "*******************************************"
echo "* DIR:                  $OUTPUT_DIR"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Python Version:       $PYTHON_CMD"
echo "* PYTHON_LIB_PATH:      $PYTHON_LIB_PATH"
echo "* CLEAN:                $CLEAN"
echo "*******************************************"

#-----------------------------------------------------#
# Step 3: Clean Output file                                   #
#-----------------------------------------------------#
# 
if [[ $QUEUE =~ sbatch ]]; then
    if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
    module load ${JAVA_CMD}/${JAVA_VERSION}
fi 
if [[ $CLEAN =~ unique ]]; then
    export SPARK_HOME=$SPARK_PATH
    export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
    export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}
    echo $JAVATOOLOPTIONS
    ${SPARK_HOME}/sbin/start-master.sh
fi

if [[ ${CONTAINER} =~ False ]]; then 
   source ${ENV_PATH}/bin/activate
fi
# source ${ENV_PATH}/bin/activate
export PYTHONPATH=$PYTHON_LIB_PATH
# ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN
if [[ ${CONTAINER} =~ False ]]; then 
   ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN
else
   ${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN
fi
