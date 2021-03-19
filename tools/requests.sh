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
    if [ "$requestType" = "insert" ]; then
        echo '{"responseNodePort": "'"${strarr[1]}"'", "insert": {"key": "'"$key"'", "replicaCount": 0, "value": "'"$value"'"}, "type": "insert", "responseNodeIP": "'"${strarr[0]}"'"}'\
        | nc ${strarr[0]} ${strarr[1]} > /dev/null &
    else
        echo '{"responseNodePort": "'"${strarr[1]}"'", "query": {"key": "'"$key"'"}, "type": "query", "responseNodeIP": "'"${strarr[0]}"'"}'\
        | nc ${strarr[0]} ${strarr[1]} > /dev/null &
    fi
done < requests.txt

wait

