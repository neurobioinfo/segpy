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

function remove_argument () {
    X=(ACCOUNT MODULEUSE= THREADS MEM_ARRAY WALLTIME_ARRAY step JAVA_VERSION)
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
