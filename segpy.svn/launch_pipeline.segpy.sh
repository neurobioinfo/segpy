#!/bin/bash

# The pipeline is done as a Project at MNI Neuro Bioinformatics Core
# Copyright belongs Neuro Bioinformatics Core
# Written by Saeid Amiri (saeid.amiri@mcgill.ca) 
VERSION=0.1.0; echo " ongoing segregation pipeline version $VERSION"
#last updated version 2022-11-10
# test on hail 0.2.81,  spark-3.1.2-bin-hadoop3.2

# ===============================================
# default variables values
# ===============================================
unset OUTPUT_DIR QUEUE ACCOUNT VCF PED CONFIG_FILE MODE VERBOSE

#Assuming script is in root of PIPELINE_HOME
export PIPELINE_HOME=$(cd $(dirname $0) && pwd -P)

# export CONFIG_FILES=$PIPELINE_HOME/configs/scrnabox.config.ini
TIMESTAMP() { date +%FT%H.%M.%S; }

#set queue-specific values, depending on system check
QUEUE="sbatch"                                       # default job scheduler: sbatch

# create function to handle error messages
# ===============================================
Usage() {
	echo
	echo -e "Usage:\t$0 [arguments]"
	echo -e "\tmandatory arguments:\n" \
          "\t\t-d  (--dir)               = run directory (where all the outputs will be printed) (give full path)\n" \
          "\t\t-s  (--steps)             = 'ALL' to run all steps, or specify steps eg. 2 (just step 2), 0-3 (steps 0 through 3)\n\t\t\t\tsteps:\n\t\t\t\t0: initial setup\n\t\t\t\t1: create hail matrix\n\t\t\t\t2: run segregation\n\t\t\t\t3: final cleanup and formatting\n" 
	echo -e "\toptional arguments:\n " \
          "\t\t-h  (--help)              = get the program options and exit\n" \
          "\t\t-v  (--vcf)               = VCF file (mandatory for steps 1-3)\n" \
          "\t\t-p  (--ped)               = PED file (mandatory for steps 1-3)\n" \
          "\t\t-c  (--config)            = config file [CURRENT: \"$(realpath $(dirname $0))/configs/segpy.config.ini\"]\n" \
          "\t\t-V  (--verbose)           = verbose output\n"
        echo
}


# ===============================================
# step 0 create folder 
# ===============================================

if ! options=$(getopt --name pipeline --alternative --unquoted --options hv:p:d:s:c:a:V --longoptions dir:,steps:,vcf:,ped:,config:,account:,verbose,help -- "$@")
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
        echo "* LOADING CONFIG FILE $CONFIG_FILE";
        . $CONFIG_FILE
      else
        echo "ERROR: invalid CONFIG file: $CONFIG_FILE";
        echo "Please check options and try again"; exit 42;
      fi
    esac
    shift
done

# if [[ -n $ACCOUNT ]]; then ACCOUNT="-A $ACCOUNT"; fi

# ===============================================
# LOAD ALL OTHER OPTIONS
# ===============================================
set -- $options

while [ $# -gt 0 ]
#echo -e "$1 $2"
do
    case $1 in
    -h| --help) Usage; exit 0;;
    # for options with required arguments, an additional shift is required
    -d| --dir) OUTPUT_DIR="$2" ; shift ;;
    -V| --verbose) VERBOSE=1 ;; 
    -s| --steps) MODE="$2"; shift ;; #SA
    -v| --vcf) VCF="$2"; shift ;; #SA
    -p| --ped) PED="$2"; shift ;; #SA
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

FOUND_ERROR=0


# ===============================================
# CHECKING VARIABLES
# ===============================================
#check to ensure all mandatory arguments have been entered

# if [ -z $SAMPLE ]; then echo "ERROR: missing mandatory option: -s (sample folder) must be specified"; FOUND_ERROR=1; fi
if [[ ! -d $OUTPUT_DIR ]]; then echo "ERROR: mandatory option: -d (--dir) not specified or does not exist"; FOUND_ERROR=1; fi
if [ -z $MODE ]; then echo "ERROR: missing mandatory option: --steps ('ALL' to run all, 2 to run step 2, step 2-3, run steps 2 through 3) must be specified"; FOUND_ERROR=1; fi
if (( $FOUND_ERROR )); then echo "Please check options and try again"; exit 42; fi
if [ $MODE == 'ALL' ]; then  MODE0=`echo {2..4}`; fi 

# set default variables
CONFIG_FILE=${CONFIG_FILE:-$PIPELINE_HOME/configs/segpy.config.ini}

# STEP 0: RUN setting 
# ===============================================
#

for d in $OUTPUT_DIR/logs/{slurm,spark}; do [[ ! -d $d ]] && mkdir -p $d; done
LAUNCH_LOG=$OUTPUT_DIR/logs/launch_log.$(TIMESTAMP)

if [[ ${MODE0[@]} =~ 1 ]]; then 
  if [[ -s $OUTPUT_DIR/$(basename $CONFIG_FILE) ]]; then
      echo "config file $(basename $CONFIG_FILE) already exists in run directory $OUTPUT_DIR. Overwrite? y|n"
      read answer
      answer=${answer,,}; answer=${answer:0:1}  # reduce all possible versions of "yes" to "y" for simplicity
      [[ $answer == "y" ]] && cp $CONFIG_FILE $OUTPUT_DIR/ || echo "will not overwrite existing config file"
  else
    cp $CONFIG_FILE $OUTPUT_DIR/
  fi
  echo " The config file is in $OUTPUT_DIR/$(basename $CONFIG_FILE)"
fi 

source $OUTPUT_DIR/$(basename $CONFIG_FILE)

# ===============================================
# STEP 2: Create hail matrix
# ===============================================
#
STEP=step_2
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
if [[  ${MODE0[@]} =~ 2 ]] ; then
  if [[(! -s $VCF) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 1 submitted"  >> $LAUNCH_LOG
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem-per-cpu=6g \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},VCF=${VCF},GRCH=${GRCH} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step2/pipeline.step2.qsub"
  step_2=$($step_2 | grep -oP "\d+")
  echo "[Q] STEP 2        : $step_2 " >> $LAUNCH_LOG
  DEPEND_step_2="--dependency=afterok:$step_2"
  echo step_2:$step_2
fi 


# ===============================================
# STEP 2: Run segregation
# ===============================================
#
STEP=step_3
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
if [[  ${MODE0[@]}  =~  3 ]]  &&  [[  ${MODE0[@]} =~ 2 ]] ; then
   if [[ (! -s $VCF) && (! -s $PED) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted following step 2"  >> $LAUNCH_LOG
  step_3="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem-per-cpu=6g \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_2 \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},SPARKMEM=${SPARKMEM} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step3/pipeline.step3.qsub"
  step_3=$($step_3 | grep -oP "\d+")
  echo "[Q] STEP 3         : $step_3 " >> $LAUNCH_LOG
  DEPEND_step_3="--dependency=afterok:$step_3"
  echo step_3:$step_3
elif [[  ${MODE0[@]}  =~  3  ]]  &&  [[  ${MODE0[@]} != 2 ]]; then
  echo "just step 3 at" $(TIMESTAMP) >> $LAUNCH_LOG
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted (without following  step 2) "  >> $LAUNCH_LOG
  step_3="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem-per-cpu=6g \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},SPARKMEM=${SPARKMEM} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step3/pipeline.step3.qsub"
  step_3=$($step_3 | grep -oP "\d+")
  echo "[Q] STEP 3         : $step_3 " >> $LAUNCH_LOG 
  DEPEND_step_3="--dependency=afterok:$step_3"
  echo step_3:$step_3
fi 


# ===============================================
# STEP 4: Final cleanup and formatting
# ===============================================
#
STEP=step_4
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
if [[  ${MODE0[@]}  =~  4 ]]  &&  [[  ${MODE0[@]} =~ 3 ]] ; then
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 4 submitted following step 3"  >> $LAUNCH_LOG
  step_4="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem-per-cpu=6g \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_3 \
    --export OUTPUT_DIR=${OUTPUT_DIR} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step4/pipeline.step4.qsub"
  step_4=$($step_4 | grep -oP "\d+")
  echo "[Q] STEP 4         : $step_4 " >> $LAUNCH_LOG
  DEPEND_step_4="--dependency=afterok:$step_4"
  echo step_4:$step_4
elif [[  ${MODE0[@]}  =~  4  ]]  &&  [[  ${MODE0[@]} != 3 ]]; then
  echo "just step 4 at" $(TIMESTAMP) >> $LAUNCH_LOG
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 4 submitted (without following  step 3) "  >> $LAUNCH_LOG
  step_4="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem-per-cpu=6g \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export OUTPUT_DIR=${OUTPUT_DIR},PIPELINE_HOME=${PIPELINE_HOME} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step4/pipeline.step4.qsub"
  step_4=$($step_4 | grep -oP "\d+")
  echo "[Q] STEP 4         : $step_4 " >> $LAUNCH_LOG 
  DEPEND_step_4="--dependency=afterok:$step_4"
  echo step_4:$step_4
fi 

exit 0

