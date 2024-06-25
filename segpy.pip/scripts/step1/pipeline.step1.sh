#!/bin/bash

# initial setup
umask 002
echo timestamp $(date +%s)
source $PIPELINE_HOME/tools/utils.sh
source $OUTPUT_DIR/configs/segpy.config.ini
source $OUTPUT_DIR/logs/.tmp/temp_config.ini
[[ $QUEUE =~ bash ]] && call_parameter $1

# log of input arguments
echo "*******************************************"
echo "* step 1: generate Matrix file"
echo "*******************************************"
echo "* PIPELINE HOME:        $PIPELINE_HOME"
echo "* SPARK HOME:           $SPARK_PATH"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Python version:       $PYTHON_CMD"
echo "* OUTPUT_DIR:           $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* GRCH:                 $GRCH"
echo "* JAVATOOLOPTIONS:      $JAVATOOLOPTIONS"
echo "*******************************************"

#-----------------------------------------------------#
# Step1: Create Matrix                                #
#-----------------------------------------------------#

# set up environment: source configs, load modules, export program variables 
# - java
if [[ $QUEUE =~ sbatch ]]; then
    [[ $MODULEUSE ]] && module use $MODULEUSE
    module load $JAVA_CMD/$JAVA_VERSION
fi
export JAVA_TOOL_OPTIONS=$JAVATOOLOPTIONS

# - spark
export SPARK_HOME=$SPARK_PATH
export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
$SPARK_HOME/sbin/start-master.sh

# - python
[[ $CONTAINER =~ False ]] && source $ENV_PATH/bin/activate
export PYTHONPATH=$PIPELINE_HOME/../segpy:$PYTHON_LIB_PATH


# set up run variables
file2=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${file2%.*}.mt

# run
[[ $CONTAINER =~ False ]] && PYTHON_CMD=$ENV_PATH/bin/$PYTHON_CMD
$PYTHON_CMD $PIPELINE_HOME/scripts/step1/step1.py $MTFILE $VCF $GRCH

echo timestamp $(date +%s)
