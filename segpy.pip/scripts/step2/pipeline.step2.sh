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
echo "* step 2: run segregation"
echo "*******************************************"
echo "* PIPELINE_HOME:        $PIPELINE_HOME"
echo "* SPARK_HOME:           $SPARK_PATH"
echo "* Virtual ENV:          $ENV_PATH"
echo "* Java Module:          ${JAVA_VERSION}"
echo "* Python Version:       $PYTHON_CMD"
echo "* PYTHON_LIB_PATH:      $PYTHON_LIB_PATH"
echo "* DIR:                  $OUTPUT_DIR"
echo "* VCF:                  $VCF"
echo "* PED:                  $PED"
echo "* NCOL:                 $NCOL"
echo "* CSQ:                  $CSQ"
echo "* SPARKMEM:             $SPARKMEM"
echo "* JAVATOOLOPTIONS:      $JAVATOOLOPTIONS"
echo "* JUST_PHENOTYPE        $JUST_PHENOTYPE"
echo "* INFO_REQUIRED         $INFO_REQUIRED"
echo "*******************************************"

#-----------------------------------------------------#
# Step 2: Run Segregation                                     #
#-----------------------------------------------------#
export SPARK_HOME=$SPARK_PATH
export SPARK_LOG_DIR=$OUTPUT_DIR/logs/spark

source ${OUTPUT_DIR}/configs/segpy.config.ini
if [[ $QUEUE =~ sbatch ]]; then
   if [[ $MODULEUSE ]]; then module use $MODULEUSE ; fi
   module load ${JAVA_CMD}/${JAVA_VERSION}
fi

${SPARK_HOME}/sbin/start-master.sh

if [[ ${CONTAINER} =~ False ]]; then 
   source ${ENV_PATH}/bin/activate
fi

# source ${ENV_PATH}/bin/activate
export PYTHONPATH=$PYTHON_LIB_PATH

export JAVA_TOOL_OPTIONS=${JAVATOOLOPTIONS}
echo $JAVATOOLOPTIONS

if [[ -z $SPARKMEM ]]; then  SPARKMEM="False"; fi

file2=$(basename $VCF)
MTFILE=$OUTPUT_DIR/step1/${file2%.*}.mt

# ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $NCOL $CSQ $VCF $SPARKMEM

if [[ ${CONTAINER} =~ False ]]; then 
   ${ENV_PATH}/bin/${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $NCOL $CSQ $VCF $SPARKMEM $JUST_PHENOTYPE $INFO_REQUIRED
else
   ${PYTHON_CMD} ${PIPELINE_HOME}/scripts/step2/step2.py $MTFILE $PED $OUTPUT_DIR/step2 $NCOL $CSQ $VCF $SPARKMEM $JUST_PHENOTYPE $INFO_REQUIRED
fi
