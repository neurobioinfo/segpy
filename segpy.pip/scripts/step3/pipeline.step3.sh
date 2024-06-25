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
echo "* step 3: clean data"
echo "*******************************************"
echo "* DIR:                  $OUTPUT_DIR"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Python Version:       $PYTHON_CMD"
echo "* PYTHON_LIB_PATH:      $PYTHON_LIB_PATH"
echo "* CLEAN:                $CLEAN"
echo "* SPARKMEM:             $SPARKMEM"
echo "*******************************************"

#-----------------------------------------------------#
# Step 3: Clean Output file                           #
#-----------------------------------------------------#

# set up environment: source configs, load modules, export program variables 
# - java
if [[ $QUEUE =~ sbatch ]]; then
    [[ $MODULEUSE ]] && module use $MODULEUSE
    #module load $JAVA_CMD/$JAVA_VERSION
    cmd="module load $JAVA_CMD/$JAVA_VERSION"
    echo CMD: $cmd
    eval $cmd
fi 
export JAVA_TOOL_OPTIONS=$JAVATOOLOPTIONS

# - spark (only needed for "clean" mode)
if [[ $CLEAN =~ unique ]]; then
    export SPARK_HOME=$SPARK_PATH
    export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
    #SPARK_HOME/sbin/start-master.sh
    cmd="$SPARK_HOME/sbin/start-master.sh"
    echo CMD: $cmd
    eval $cmd
fi

# - python
[[ $CONTAINER =~ False ]] && source $ENV_PATH/bin/activate
export PYTHONPATH=$PIPELINE_HOME/../segpy:$PYTHON_LIB_PATH

# run
[[ $CONTAINER =~ False ]] && PYTHON_CMD=$ENV_PATH/bin/$PYTHON_CMD
[[ -z $SPARKMEM ]] && SPARKMEM="False"
#PYTHON_CMD $PIPELINE_HOME/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM
cmd="$PYTHON_CMD $PIPELINE_HOME/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM"
echo CMD: $cmd
eval $cmd

echo timestamp $(date +%s)
