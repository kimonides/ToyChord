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

while IFS=',' read key value
do
    index=$(($RANDOM % $size))
    read -a strarr <<< "${VMs[$index]}"
    printf "3\n$key\n$value" | python3 client.py ${strarr[0]} ${strarr[1]} > /dev/null & 
done < insert.txt

wait $!


