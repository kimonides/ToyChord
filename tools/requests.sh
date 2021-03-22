#!/bin/bash

declare -a VMs=(
    "192.168.1.1 42069"
    "192.168.1.1 50100"
    "192.168.1.2 42069"
    "192.168.1.2 50100"
    "192.168.1.3 42069"
    "192.168.1.3 50100"
    "192.168.1.4 42069"
    "192.168.1.4 50100"
    "192.168.1.5 42069"
    "192.168.1.5 50100"
)
size=${#VMs[@]}

while IFS=',' read requestType key value
do
    index=$(($RANDOM % $size))
    read -a strarr <<< "${VMs[$index]}"
    key=$(echo $key | awk '{$1=$1;print}')
    if [ "$requestType" = "insert" ]; then
        value=$(echo $value | awk '{$1=$1;print}')
        # echo '{"responseNodePort": "'"${strarr[1]}"'", "insert": {"key": "'"$key"'", "replicaCount": 0, "value": "'"$value"'"}, "type": "insert", "responseNodeIP": "'"${strarr[0]}"'"}'\
        # | nc ${strarr[0]} ${strarr[1]} > request_output 
        echo "insert $key $value => $(echo '{"responseNodePort": "'"${strarr[1]}"'", "insert": {"key": "'"$key"'", "replicaCount": 0, "value": "'"$value"'"}, "type": "insert", "responseNodeIP": "'"${strarr[0]}"'"}' | nc ${strarr[0]} ${strarr[1]} )" >> request_output
    else
        # echo '{"responseNodePort": "'"${strarr[1]}"'", "query": {"key": "'"$key"'"}, "type": "query", "responseNodeIP": "'"${strarr[0]}"'"}'\
        # | nc ${strarr[0]} ${strarr[1]} > request_output 
        echo "query $key => $(echo '{"responseNodePort": "'"${strarr[1]}"'", "query": {"key": "'"$key"'"}, "type": "query", "responseNodeIP": "'"${strarr[0]}"'"}' | nc ${strarr[0]} ${strarr[1]} )" >> request_output
    fi
done < requests.txt

# wait

