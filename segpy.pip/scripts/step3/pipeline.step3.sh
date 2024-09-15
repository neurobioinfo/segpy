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
echo "* OUTPUT_DIR:           $OUTPUT_DIR"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
# echo "* Virtual ENV:          $ENV_PATH"
# echo "* Python Version:       $PYTHON_CMD"
# echo "* PYTHON_LIB_PATH:      $PYTHON_LIB_PATH"
echo "* CLEAN:                $CLEAN"
echo "* SPARKMEM:             $SPARKMEM"
echo "*******************************************"

#-----------------------------------------------------#
# Step 3: Clean Output file                                   #
#-----------------------------------------------------#
# 
# if [[ $QUEUE =~ sbatch ]]; then
#    [[ $MODULEUSE ]] && module use $MODULEUSE
#    #  module load ${JAVA_CMD}/${JAVA_VERSION}
#    cmd="module load $JAVA_CMD/$JAVA_VERSION"
#    echo CMD: $cmd
#    eval $cmd
# fi 

if [[ $CLEAN =~ unique ]]; then
   #  export SPARK_HOME=$SPARK_PATH
    export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark
    export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}
   #  echo $JAVATOOLOPTIONS
   #  ${SPARK_HOME}/sbin/start-master.sh
   #  cmd="$SPARK_HOME/sbin/start-master.sh"
   #  echo CMD: $cmd
   #  eval $cmd
fi

# [[ ${CONTAINER} =~ False ]] && source ${ENV_PATH}/bin/activate

# source ${ENV_PATH}/bin/activate
[[ -z $SPARKMEM ]] && SPARKMEM="False"
# export PYTHONPATH=$PYTHON_LIB_PATH
# ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN
# if [[ ${CONTAINER} =~ False ]]; then 
#    ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM
# else
#    ${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step3/step3.py $OUTPUT_DIR $CLEAN $SPARKMEM
# fi

# echo "SPARKMEM"
# echo $SPARKMEM
# echo "Test"
if [[ $QUEUE =~ bash ]] &&  [[ $CONTAINER =~ TRUE ]]; then 
   # CONTAINER1=$PIPELINE_HOME/soft/container/scrnabox.sif
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
