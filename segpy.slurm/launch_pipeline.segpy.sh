#!/bin/bash

# The pipeline is done as a Project at MNI Neuro Bioinformatics Core
# Copyright belongs Neuro Bioinformatics Core
# Written by Saeid Amiri (saeid.amiri@mcgill.ca) 
VERSION=0.2.0; echo " ongoing segregation pipeline version $VERSION"
#last updated version 2023-01-25
# test on hail 0.2.107,  spark-3.1.3-bin-hadoop3.2

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
          "\t\t-s  (--steps)             = 'ALL' to run all steps, or specify steps eg. 1 (just step 1), 1-3 (steps 1 through 4)\n\t\t\t\tsteps:\n\t\t\t\t1: initial setup\n\t\t\t\t2: create hail matrix\n\t\t\t\t3: run segregation\n\t\t\t\t4: final cleanup and formatting\n"            
	echo -e "\toptional arguments:\n " \
          "\t\t-h  (--help)              = get the program options and exit\n" \
          "\t\t--clean             = 'general': to general cleaning, 'unique': drop multiplicities" \
          "\t\t-v  (--vcf)               = VCF file (mandatory for steps 1-3)\n" \
          "\t\t-p  (--ped)               = PED file (mandatory for steps 1-3)\n" \
          "\t\t-c  (--config)            = config file [CURRENT: \"$(realpath $(dirname $0))/configs/segpy.config.ini\"]\n" \
          "\t\t-V  (--verbose)           = verbose output\n"
        echo
}


# ===============================================
# step 0 create folder 
# ===============================================

if ! options=$(getopt --name pipeline --alternative --unquoted --options hv:p:d:s:c:a:V --longoptions dir:,steps:,vcf:,ped:,clean:,config:,account:,verbose,help -- "$@")
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
    --clean) CLEAN="$2"; shift ;;
    (--) shift; break;;
    (-*) echo "$0: error - unrecognized option $1" 1>&2; exit 42;;
    (*) break;;
    esac
    shift
done

if [[ -z $CLEAN ]]; then  CLEAN="F"; fi

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
if [ -z $MODE ]; then echo "ERROR: missing mandatory option: --steps ('ALL' to run all, 1 to run step 1, step 1-3, run steps 1 through 3) must be specified"; FOUND_ERROR=1; fi
if (( $FOUND_ERROR )); then echo "Please check options and try again"; exit 42; fi
if [ $MODE == 'ALL' ]; then  MODE0=`echo {0..3}`; fi 

# set default variables
CONFIG_FILE=${CONFIG_FILE:-$PIPELINE_HOME/configs/segpy.config.ini}

# STEP 1: RUN setting 
# ===============================================
#

for d in $OUTPUT_DIR/logs/{slurm,spark}; do [[ ! -d $d ]] && mkdir -p $d; done
LAUNCH_LOG=$OUTPUT_DIR/logs/launch_log.$(TIMESTAMP)

if [[ ${MODE0[@]} =~ 0 ]]; then 
  if [[ -s $OUTPUT_DIR/$(basename $CONFIG_FILE) ]]; then
      echo "config file $(basename $CONFIG_FILE) already exists in PWD: $OUTPUT_DIR. Overwrite? y|n"
      read answer
      answer=${answer,,}; answer=${answer:0:1}  # reduce all possible versions of "yes" to "y" for simplicity
      [[ $answer == "y" ]] && cp $CONFIG_FILE $OUTPUT_DIR/ || echo "will not overwrite existing config file"
  else
    cp $CONFIG_FILE $OUTPUT_DIR/
  fi
  echo -e " The config file ($(basename $CONFIG_FILE)) is in \n $OUTPUT_DIR"
fi 

source $OUTPUT_DIR/$(basename $CONFIG_FILE)

# ===============================================
# STEP 1: Create hail matrix
# ===============================================
#
STEP=step_1
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
export MEM=${MEM_ARRAY[$STEP]}
if [[  ${MODE0[@]} =~ 1 ]] ; then
  if [[(! -s $VCF) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 1 submitted"  >> $LAUNCH_LOG
  step_1="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM}  \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},GRCH=${GRCH} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step1/pipeline.step1.qsub"
  step_1=$($step_1 | grep -oP "\d+")
  echo "[Q] STEP 1        : $step_1 " >> $LAUNCH_LOG
  DEPEND_step_1="--dependency=afterok:$step_1"
  echo step_1:$step_1
fi 



# ===============================================
# STEP 2: Run segregation
# ===============================================
#
STEP=step_2
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
export MEM=${MEM_ARRAY[$STEP]}
if [[  ${MODE0[@]}  =~  2 ]]  &&  [[  ${MODE0[@]} =~ 1 ]] ; then
   if [[ (! -s $VCF) && (! -s $PED) ]]; then echo "ERROR: missing mandatory option for steps 1-3: -v (--vcf) empty, not specified or does not exist"; FOUND_ERROR=1; fi
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 2 submitted following step 1"  >> $LAUNCH_LOG
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_1 \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},SPARKMEM=${SPARKMEM} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step2/pipeline.step2.qsub"
  step_2=$($step_2 | grep -oP "\d+")
  echo "[Q] STEP 2         : $step_2 " >> $LAUNCH_LOG
  DEPEND_step_2="--dependency=afterok:$step_2"
  echo step_2:$step_2
elif [[  ${MODE0[@]}  =~  2  ]]  &&  [[  ${MODE0[@]} != 1 ]]; then
  echo "just step 2 at" $(TIMESTAMP) >> $LAUNCH_LOG
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 2 submitted (without following  step 1) "  >> $LAUNCH_LOG
  step_2="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},SPARK_PATH=${SPARK_PATH},JAVATOOLOPTIONS=${JAVATOOLOPTIONS},ENV_PATH=${ENV_PATH},OUTPUT_DIR=${OUTPUT_DIR},JAVA_MODULE=${JAVA_MODULE},PYTHON_MODULE=${PYTHON_MODULE},PYTHON_RUN=${PYTHON_RUN},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},VCF=${VCF},PED=${PED},NCOL=${NCOL},SPARKMEM=${SPARKMEM} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step2/pipeline.step2.qsub"
  step_2=$($step_2 | grep -oP "\d+")
  echo "[Q] STEP 2         : $step_2 " >> $LAUNCH_LOG 
  DEPEND_step_2="--dependency=afterok:$step_2"
  echo step_2:$step_2
fi 




# ===============================================
# STEP 3: Final cleanup and formatting
# ===============================================
#
STEP=step_3
export THREADS=${THREADS_ARRAY[$STEP]}
export WALLTIME=${WALLTIME_ARRAY[$STEP]}
export MEM=${MEM_ARRAY[$STEP]}
if [[  ${MODE0[@]}  =~  3 ]]  &&  [[  ${MODE0[@]} =~ 2 ]] ; then
  TIMESTAMP  >> $LAUNCH_LOG
  echo "--------"  >> $LAUNCH_LOG
  echo "STEP 3 submitted following step 2"  >> $LAUNCH_LOG
  step_3="$QUEUE -A $ACCOUNT  \
    --ntasks-per-node=${THREADS} \
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    $DEPEND_step_2 \
    --export PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_MODULE=${PYTHON_MODULE},CLEAN=${CLEAN} \
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
    --mem=${MEM} \
    --time=${WALLTIME} \
    --job-name $STEP \
    --export PIPELINE_HOME=${PIPELINE_HOME},ENV_PATH=${ENV_PATH},PYTHON_RUN=${PYTHON_RUN},OUTPUT_DIR=${OUTPUT_DIR},PYTHON_LIB_PATH=${PYTHON_LIB_PATH},PYTHON_MODULE=${PYTHON_MODULE},CLEAN=${CLEAN} \
    --output $OUTPUT_DIR/logs/slurm/%x.o%j \
    $PIPELINE_HOME/scripts/step3/pipeline.step3.qsub"
  step_3=$($step_3 | grep -oP "\d+")
  echo "[Q] STEP 3         : $step_3 " >> $LAUNCH_LOG 
  DEPEND_step_3="--dependency=afterok:$step_3"
  echo step_3:$step_3
fi

exit 0

