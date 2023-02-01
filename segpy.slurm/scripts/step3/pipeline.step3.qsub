#!/bin/bash

umask 002
echo timestamp $(date +%s)

echo "*******************************************"
echo "* step 3: clean data"
echo "*******************************************"
echo "* DIR:                  $OUTPUT_DIR"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Python module:        $PYTHON_MODULE"
echo "* Python RUN:           $PYTHON_RUN"
echo "* PYTHON_LIB_PATH       $PYTHON_LIB_PATH"
echo "* CLEAN:                $CLEAN"
echo "*******************************************"

#-----------------------------------------------------#
# Step 3: Clean Output file                                   #
#-----------------------------------------------------#
# 

source ${ENV_PATH}/bin/activate
export PYTHONPATH=$PYTHON_LIB_PATH
module load $PYTHON_MODULE

${ENV_PATH}/bin/${PYTHON_RUN} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN
