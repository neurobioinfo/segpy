#!/bin/bash
# The pipeline is done as a Project at MNI Neuro Bioinformatics Core
# Copyright belongs Neuro Bioinformatics Core
# Developed\Scripted by Saeid Amiri (saeid.amiri@mcgill.ca) 

VERSION=0.0.6;
DATE0=2024-12-16
PIPELINE_NAME=segregation
echo -e "------------------------------------ "
echo -e "$PIPELINE_NAME pipeline version $VERSION is loaded"

# test on hail 0.2.109,  spark-3.1.3-bin-hadoop3.2
# ===============================================
# default variables values
# ===============================================
unset OUTPUT_DIR QUEUE ACCOUNT VCF PED CONFIG_FILE MODE VERBOSE

export VERSION=${VERSION}
#Assuming script is in root of PIPELINE_HOME
export PIPELINE_HOME=$(cd $(dirname $0) && pwd -P)

TIMESTAMP() { date +%FT%H.%M.%S;}
CONTAINER=TRUE
#set queue-specific values, depending on system check
# QUEUE="sbatch"            # default job scheduler: sbatch

# create function to handle error messages
# ===============================================
Usage() {
	echo
  echo "------------------- " 
	echo -e "Usage:\t$0 [arguments]"
	echo -e "\tmandatory arguments:\n" \
          "\t\t-d  (--dir)      = Working directory (where all the outputs will be printed) (give full path) \n" \
          "\t\t-s  (--steps)      = Specify what steps, e.g., 2 to run just step 2, 1-3 (run steps 1 through 3). 'ALL' to run all steps.\n\t\t\t\tsteps:\n\t\t\t\t0: initial setup\n\t\t\t\t1: create hail matrix\n\t\t\t\t2: run segregation\n\t\t\t\t3: final cleanup and formatting\n"
	echo -e "\toptional arguments:\n " \
          "\t\t-h  (--help)      = Get the program options and exit.\n" \
          "\t\t--jobmode  = The default for the pipeline is local. If you want to run the pipeline on slurm system, use slurm as the argument. \n" \
          "\t\t--analysis_mode  = The default for the pipeline is analysing single or multiple family. If you want to run the pipeline on case-control, use case-control as  the argumnet. \n" \
          "\t\t--parser             = 'general': to general parsing, 'unique': drop multiplicities \n" \
          "\t\t-v  (--vcf)      = VCF file (mandatory for steps 1-3)\n" \
          "\t\t-p  (--ped)      = PED file (mandatory for steps 1-3)\n" \
          "\t\t-c  (--config)      = config file [CURRENT: \"$(realpath $(dirname $0))/configs/segpy.config.ini\"]\n" \
          "\t\t-V  (--verbose)      = verbose output \n \n" \
          "------------------- \n" \
          "For a comprehensive help, visit  https://neurobioinfo.github.io/segpy/latest/ for documentation. "

        echo
}


if ! options=$(getopt --name pipeline --alternative --unquoted --options hv:p:d:s:c:a:V --longoptions dir:,steps:,jobmode:,analysis_mode:,vcf:,ped:,parser:,config:,account:,verbose,help -- "$@")
then
    # something went wrong, getopt will put out an error message for us
    echo "Error processing options."
    exit 42
fi

# ===============================================
# LOAD & OVERRIDE CONFIG FILE FOR PROJECT
# ===============================================
set -- $options

while [ $# -gt 0 ]
do
    case $1 in
    -c| --config) 
      CONFIG_FILE="$2" ;
      if [ -f $CONFIG_FILE ]; then
        echo "* LOADING CONFIG FILE $d";
        . $CONFIG_FILE
      else
        echo "ERROR: invalid CONFIG file: $CONFIG_FILE";
        echo "Please check options and try again"; exit 42;
      fi
    esac
    shift
done

# ===============================================
# LOAD ALL OTHER OPTIONS
# ===============================================
set -- $options

while [ $# -gt 0 ]
do
    case $1 in
    -h| --help) Usage; exit 0;;
    -d| --dir) OUTPUT_DIR="$2" ; shift ;;
    -V| --verbose) VERBOSE=1 ;; 
    -s| --steps) MODE="$2"; shift ;;
    --jobmode) JOB_MODE="$2"; shift ;;
    --analysis_mode) ANA_MODE="$2"; shift ;;
    -v| --vcf) VCF="$2"; shift ;;
    -p| --ped) PED="$2"; shift ;;
    --parser) CLEAN="$2"; shift ;;
    (--) shift; break;;
    (-*) echo "$0: error - unrecognized option $1" 1>&2; exit 42;;
    (*) break;;
    esac
    shift
done

if [[ "$MODE" == *"-"* ]]; then
  abc0=`echo $MODE | sed  "s/-/../g"  | awk '{print "{"$0"}"}'`
  MODE0=`eval echo $abc0`
else 
  MODE0=$MODE
fi

source $PIPELINE_HOME/tools/utils.sh
FOUND_ERROR=0

TEMPCONFIG=$OUTPUT_DIR/logs/.tmp/temp_config.ini
INICONFIG=$OUTPUT_DIR/logs/.tmp/ini_config.ini
LAUNCH_LOG=$OUTPUT_DIR/launch_summary_log.txt
# ===============================================
# CHECKING VARIABLES
# ===============================================
#check to ensure all mandatory arguments have been entered

if [[ ! -d $OUTPUT_DIR ]]; then echo "ERROR: mandatory option: -d (--dir) not specified or does not exist"; FOUND_ERROR=1; fi
if [ -z $MODE ]; then echo "ERROR: missing mandatory option: --steps ('ALL' to run all, 1 to run step 1, step 1-3, run steps 1 through 3) must be specified"; FOUND_ERROR=1; fi
if (( $FOUND_ERROR )); then echo "Please check options and try again"; exit 42; fi
if [ $MODE == 'ALL' ]; then  MODE0=`echo {0..3}`; fi 
# if [ -z $ANA_MODE ]; then ANA_MODE=other ; fi

# echo $ANA_MODE
# set default variables
# CONFIG_FILE=${CONFIG_FILE:-$PIPELINE_HOME/configs/segpy.config.ini}
cd $OUTPUT_DIR
# STEP 1: RUN setting 
# ===============================================
#
for d in $OUTPUT_DIR/logs/{jobs,spark}; do [[ ! -d $d ]] && mkdir -p $d; done
# LAUNCH_LOG=$OUTPUT_DIR/logs/launch_log.$(TIMESTAMP)

if [[ ${MODE0[@]} =~ 0 ]]; then 
  if [[ -d $OUTPUT_DIR/configs ]]; then
      echo "Config file already exists in PWD: $OUTPUT_DIR. Overwrite? y|n"
      read answer
      answer=${answer,,}; answer=${answer:0:1}  # reduce all possible versions of "yes" to "y" for simplicity
      if [[ $answer == "y" ]]; then 
          rm -rf $OUTPUT_DIR/configs/segpy.config.ini
          rm -rf $OUTPUT_DIR/logs/*
          # rm -rf $OUTPUT_DIR/launch_summary_log.txt
          cp $PIPELINE_HOME/configs/segpy.config.ini $OUTPUT_DIR/configs/ 
      fi
  else
      mkdir -p $OUTPUT_DIR/configs
      cp $PIPELINE_HOME/configs/segpy.config.ini $OUTPUT_DIR/configs/
  fi
  echo -e " The config file (segpy.config.ini) is in \n ./configs"
  LAUNCH_LOG=$OUTPUT_DIR/launch_summary_log.txt
  if [ -f $LAUNCH_LOG ]; then
    rm $OUTPUT_DIR/launch_summary_log.txt
  fi
  touch $LAUNCH_LOG
  chmod 775 $LAUNCH_LOG 
  if [[ -d $OUTPUT_DIR/logs/.tmp ]]; then rm -rf $OUTPUT_DIR/logs/.tmp; fi
  mkdir -p $OUTPUT_DIR/logs/.tmp
  chmod 775 $OUTPUT_DIR/logs/.tmp
  # if [[ -d $OUTPUT_DIR/logs/tmp ]]; then rm -rf $OUTPUT_DIR/logs/tmp; fi
  # mkdir -p $OUTPUT_DIR/logs/tmp
  # touch $OUTPUT_DIR/logs/.tmp/temp_config.ini
  if [[ -f "$TEMPCONFIG" ]]; then 
    rm $TEMPCONFIG
  fi
  touch $TEMPCONFIG
  echo " # IT IS A temp FILE. DO NOT EDIT THIS FILE DIRECTLY."  > $TEMPCONFIG
  echo -e  "------------------------------------------------------------------" >> $LAUNCH_LOG  
  echo -e  "-------- $PIPELINE_NAME pipeline is set up for ${VERSION}-----------------"  >> $LAUNCH_LOG
  if [[ $JOB_MODE =~ slurm ]]; then
      echo -e  "--------running with scheduler-----------------" >> $LAUNCH_LOG
      echo JOB_MODE=slurm >> $OUTPUT_DIR/configs/segpy.config.ini
      remove_argument_slurm $OUTPUT_DIR/configs/segpy.config.ini
  elif [[ $JOB_MODE =~ local ]]; then
      echo -e  "--------running without scheduler-----------------" >> $LAUNCH_LOG
      echo JOB_MODE=local >> $OUTPUT_DIR/configs/segpy.config.ini
      remove_argument_local $OUTPUT_DIR/configs/segpy.config.ini
  else
      JOB_MODE=local
      echo -e  "--------running without scheduler-----------------" >> $LAUNCH_LOG
      echo "JOB_MODE=local" >> $OUTPUT_DIR/configs/segpy.config.ini
      remove_argument_local $OUTPUT_DIR/configs/segpy.config.ini
  fi 

  echo "-------------------------------------------"  >> $LAUNCH_LOG
  echo -e "The Output is under \n ${OUTPUT_DIR}/" >> $LAUNCH_LOG
  echo -e  "------------------------------------------------------------------\n" >> $LAUNCH_LOG
  
  echo "NOTE: the segpy is setup with  ${JOB_MODE} mode"
  if [[ $JOB_MODE =~ slurm ]]; then
    QUEUE="sbatch"
  elif [[ $JOB_MODE =~ local ]]; then
    QUEUE="bash"
  else
    echo "The pipeline is tested under slurm system and linux"
    echo "please choose slurm or local for --jobmode"   
    exit 42
  fi
  echo JOB_MODE=$JOB_MODE >> $TEMPCONFIG
  echo QUEUE=$QUEUE >> $TEMPCONFIG
  echo OUTPUT_DIR=$OUTPUT_DIR >> $TEMPCONFIG
  echo LAUNCH_LOG=$LAUNCH_LOG >> $TEMPCONFIG
  if [[ $ANA_MODE ]]; then
  echo ANA_MODE=${ANA_MODE} >> $INICONFIG
  echo "NOTE: User selected analysis_mode: ${ANA_MODE} "
  echo "NOTE: User selected analysis_mode: ${ANA_MODE}" >> $LAUNCH_LOG
  else
    echo ANA_MODE=other >> $INICONFIG
    echo "User did not specify --analysis_mode, so the pipeline will determine how to handle the analysis based on the pedigree file"
    echo "User did not specify --analysis_mode, so the pipeline will determine how to handle the analysis based on the pedigree file." >> $LAUNCH_LOG
  fi
  source $OUTPUT_DIR/configs/segpy.config.ini
   if [[ $JOB_MODE =~ local ]]; then 
      if [[ ! $($CONTAINER_CMD --version) ]]; then
          echo " Apptainer\singularity does not exist on system"
          exit 0 
      else
          echo -e "$($CONTAINER_CMD --version) is installed on the system " >> $LAUNCH_LOG
      fi
   fi 
  exit 0
fi

# if [[ ! -d $OUTPUT_DIR/logs/tmp ]]; then mkdir -p $OUTPUT_DIR/logs/tmp ; fi
cd $OUTPUT_DIR/logs/spark 

# LAUNCH_LOG=$OUTPUT_DIR/logs/launch_summary_log.txt

declare -A THREADS_ARRAY
declare -A  WALLTIME_ARRAY
declare -A  MEM_ARRAY



PYTHON_LIB_PATH=${ENV_PATH}/lib/${PYTHON_CMD}/site-packages
if [[ $PYTHON_LIB_PATH ]];  then   sed -i '/PYTHON_LIB_PATH=/d' $TEMPCONFIG; echo PYTHON_LIB_PATH=$PYTHON_LIB_PATH >> $TEMPCONFIG  ; fi

export OUTPUT_DIR=$OUTPUT_DIR
export PYTHON_LIB_PATH=$PYTHON_LIB_PATH

if [[ $VCF ]];  then   sed -i '/VCF=/d' $TEMPCONFIG; echo VCF=$VCF >> $TEMPCONFIG   ; fi
if [[ $PED ]];  then sed -i '/PED=/d' $TEMPCONFIG; echo PED=${PED} >> $TEMPCONFIG    ; fi
if [[ $CLEAN ]];  then  sed -i "/CLEAN=/d" $TEMPCONFIG; echo CLEAN=$CLEAN >> $TEMPCONFIG   ; fi
if [[ $LAUNCH_LOG ]];  then  sed -i '/LAUNCH_LOG=/d' $TEMPCONFIG; echo LAUNCH_LOG=$LAUNCH_LOG >> $TEMPCONFIG  ; fi
if [[ $MODE ]];  then   sed -i '/MODE=/d' $TEMPCONFIG; echo MODE=$MODE >> $TEMPCONFIG   ; fi



echo CONTAINER=$CONTAINER >> $TEMPCONFIG

source $OUTPUT_DIR/logs/.tmp/temp_config.ini
if [[ ${QUEUE} =~ sbatch ]] ; then
  bash ${PIPELINE_HOME}/launch_segpy_slurm.sh
elif [[ ${QUEUE} =~ bash   ]]; then
  bash ${PIPELINE_HOME}/launch_segpy_local.sh
fi
echo -e " \n"

exit 0
