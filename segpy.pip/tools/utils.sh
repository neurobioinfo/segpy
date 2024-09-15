#!/bin/bash

function call_parameter () {
   a=$1
   my_string=${a#*=}
   my_array=($(echo $my_string | tr "," "\n"))
   for i in "${my_array[@]}"
   do
      eval  $i
   done
}

function remove_argument_local () {
    X=(ACCOUNT MODULEUSE= THREADS MEM_ARRAY WALLTIME_ARRAY step JAVA_VERSION SPARK_PATH  ENV_PATH JAVA_CMD NCOL PYTHON_CMD JUST_PHENOTYPE)
    for item in ${X[@]}; do
        sed -i $1 -e "/${item}/d"
    done
}

function remove_argument_slurm () {
    X=(SPARK_PATH ENV_PATH PYTHON_CMD JAVA_CMD JAVA_VERSION NCOL JUST_PHENOTYPE)
    for item in ${X[@]}; do
        sed -i $1 -e "/${item}/d"
    done
}

function depend_other () {
    output1=$(ps -o args)
    output2=$(echo $output1 | grep -n $1)
    while [[ $(echo $output2 | grep -n $1) =~ $1 ]]; do
            sleep 60
            output1=$(ps -o args)
            output2=$(echo $output1 | grep -n $1)
    done
}
