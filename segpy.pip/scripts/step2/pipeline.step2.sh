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
echo "* step 2: run segregation"
echo "*******************************************"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* SPARK_HOME:           $SPARK_PATH"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Java Module:          $JAVA_VERSION"
echo "* Python Version:       $PYTHON_CMD"
echo "* PYTHON_LIB_PATH:      $PYTHON_LIB_PATH"
echo "* DIR:                  $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* PED:                  $PED"
echo "* CSQ:                  $CSQ"
echo "* SPARKMEM:             $SPARKMEM"
echo "* JAVATOOLOPTIONS:      $JAVATOOLOPTIONS"
echo "* AFFECTEDS_ONLY        $AFFECTEDS_ONLY"
echo "*******************************************"

#-----------------------------------------------------#
# Step 2: Run Segregation                             #
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
[[ -z $SPARKMEM ]] && SPARKMEM="False"
file2=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${file2%.*}.mt

# run
[[ $CONTAINER =~ False ]] && PYTHON_CMD=$ENV_PATH/bin/$PYTHON_CMD
$PYTHON_CMD $PIPELINE_HOME/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $CSQ $VCF $SPARKMEM $AFFECTEDS_ONLY

echo timestamp $(date +%s)
