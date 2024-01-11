#!/bin/bash
# The pipeline is done as a Project at MNI Neuro Bioinformatics Core
# Copyright belongs Neuro Bioinformatics Core
# Developed by Saeid Amiri (saeid.amiri@mcgill.ca) 

VERSION=0.2.2;
DATE0=2024-01-04
echo -e "------------------------------------ "
echo -e "Segregation pipline version $VERSION "

# test on hail 0.2.107,  spark-3.1.3-bin-hadoop3.2
# ===============================================
# default variables values
# ===============================================
unset OUTPUT_DIR QUEUE ACCOUNT VCF PED CONFIG_FILE MODE VERBOSE

#Assuming script is in root of PIPELINE_HOME
export PIPELINE_HOME=$(cd $(dirname $0) && pwd -P)

TIMESTAMP() { date +%FT%H.%M.%S; }
CONTAINER=False
#set queue-specific values, depending on system check
# QUEUE="sbatch"            # default job scheduler: sbatch

# create function to handle error messages
# ===============================================
Usage() {
	echo
	echo -e "Usage:\t$0 [arguments]"
	echo -e "\tmandatory arguments:\n" \
          "\t\t-d  (--dir)               = Working directory (where all the outputs will be printed) (give full path) \n" \
          "\t\t-s  (--steps)             = Specify what steps, e.g., 2 to run just step 2, 1-3 (run steps 1 through 4). 'ALL' to run all steps.\n\t\t\t\tsteps:\n\t\t\t\t1: initial setup\n\t\t\t\t2: create hail matrix\n\t\t\t\t3: run segregation\n\t\t\t\t4: final cleanup and formatting\n"            
	echo -e "\toptional arguments:\n " \
          "\t\t-h  (--help)              = See helps regarding the pipeline arguments.\n" \
          "\t\t--parser             = 'general': to general parsing, 'unique': drop multiplicities" \
          "\t\t-v  (--vcf)               = VCF file (mandatory for steps 1-3)\n" \
          "\t\t-p  (--ped)               = PED file (mandatory for steps 1-3)\n" \
          "\t\t-c  (--config)            = config file [CURRENT: \"$(realpath $(dirname $0))/configs/segpy.config.ini\"]\n" \
          "\t\t-V  (--verbose)           = verbose output\n"
        echo
}


if ! options=$(getopt --name pipeline --alternative --unquoted --options hv:p:d:s:c:a:V --longoptions dir:,steps:,jobmode:,vcf:,ped:,parser:,config:,account:,verbose,help -- "$@")
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
    # for options with required arguments, an additional shift is required
    -d| --dir) OUTPUT_DIR="$2" ; shift ;;
    -V| --verbose) VERBOSE=1 ;; 
    -s| --steps) MODE="$2"; shift ;; #SA
    --jobmode) JOB_MODE="$2"; shift ;;     
    -v| --vcf) VCF="$2"; shift ;; #SA
    -p| --ped) PED="$2"; shift ;; #SA
    --parse) CLEAN="$2"; shift ;;
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
LAUNCH_LOG=$OUTPUT_DIR/launch_summary_log.txt
# ===============================================
# CHECKING VARIABLES
# ===============================================
#check to ensure all mandatory arguments have been entered

if [[ ! -d $OUTPUT_DIR ]]; then echo "ERROR: mandatory option: -d (--dir) not specified or does not exist"; FOUND_ERROR=1; fi
if [ -z $MODE ]; then echo "ERROR: missing mandatory option: --steps ('ALL' to run all, 1 to run step 1, step 1-3, run steps 1 through 3) must be specified"; FOUND_ERROR=1; fi
if (( $FOUND_ERROR )); then echo "Please check options and try again"; exit 42; fi
if [ $MODE == 'ALL' ]; then  MODE0=`echo {0..3}`; fi 

# set default variables
# CONFIG_FILE=${CONFIG_FILE:-$PIPELINE_HOME/configs/segpy.config.ini}

# STEP 1: RUN setting 
# ===============================================
#

for d in $OUTPUT_DIR/logs/{jobs,spark}; do [[ ! -d $d ]] && mkdir -p $d; done
# LAUNCH_LOG=$OUTPUT_DIR/logs/launch_log.$(TIMESTAMP)

if [[ ${MODE0[@]} =~ 0 ]]; then 
  if [[ -s $OUTPUT_DIR/configs ]]; then
      echo "config file $($OUTPUT_DIR/configs) already exists in PWD: $OUTPUT_DIR. Overwrite? y|n"
      read answer
      answer=${answer,,}; answer=${answer:0:1}  # reduce all possible versions of "yes" to "y" for simplicity
      [[ $answer == "y" ]] && cp $PIPELINE_HOME/configs/segpy.config.ini $OUTPUT_DIR/configs/ || echo "will not overwrite existing config file"
  else
      mkdir -p $OUTPUT_DIR/configs
      cp $PIPELINE_HOME/configs/segpy.config.ini $OUTPUT_DIR/configs/
  fi
  echo -e " The config file (segpy.config.ini) is in \n ./configs"
  LAUNCH_LOG=$OUTPUT_DIR/launch_summary_log.txt
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
  echo -e  "-------------------------------------------" >> $LAUNCH_LOG  
  echo -e  "--------Pipeline is set up for ${SCRNA_METHOD0}-----------------" $VERSION >> $LAUNCH_LOG
  if [[ $JOB_MODE =~ slurm ]]; then
      echo -e  "--------running with scheduler-----------------" >> $LAUNCH_LOG
      echo JOB_MODE=slurm >> $OUTPUT_DIR/configs/segpy.config.ini
  elif [[ $JOB_MODE =~ local ]]; then
      echo -e  "--------running without scheduler-----------------" >> $LAUNCH_LOG
      echo JOB_MODE=local >> $OUTPUT_DIR/configs/segpy.config.ini
      remove_argument $OUTPUT_DIR/configs/segpy.config.ini
  else
      JOB_MODE=local
      echo -e  "--------running without scheduler-----------------" >> $LAUNCH_LOG
      echo JOB_MODE=local >> $OUTPUT_DIR/configs/segpy.config.ini
      remove_argument $OUTPUT_DIR/configs/segpy.config.ini
  fi 
  echo "-----------------------------------------------------------"  >> $LAUNCH_LOG
  echo -e "The Output is under \n ${OUTPUT_DIR}/" >> $LAUNCH_LOG
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
  exit 0
fi

# if [[ ! -d $OUTPUT_DIR/logs/tmp ]]; then mkdir -p $OUTPUT_DIR/logs/tmp ; fi
cd $OUTPUT_DIR/logs/spark 

# LAUNCH_LOG=$OUTPUT_DIR/logs/launch_summary_log.txt

declare -A THREADS_ARRAY
declare -A  WALLTIME_ARRAY
declare -A  MEM_ARRAY

source $OUTPUT_DIR/configs/segpy.config.ini
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
