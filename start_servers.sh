#!/bin/bash
# myprogram > foo.out 2> foo.err < /dev/null &
nohup python3 startNode.py 42069 </dev/null &>/dev/null &
nohup python3 startNode.py 50100 </dev/null &>/dev/null &
ssh node1 "cd ~/distributed ; screen -d -m python3 startNode.py 42069" &
ssh node1 "cd ~/distributed ; screen -d -m python3 startNode.py 50100" &

ssh node2 "cd ~/distributed ; screen -d -m python3 startNode.py 42069" &
ssh node2 "cd ~/distributed ; screen -d -m python3 startNode.py 50100" &

ssh node3 "cd ~/distributed ; screen -d -m python3 startNode.py 42069" &
ssh node3 "cd ~/distributed ; screen -d -m python3 startNode.py 50100" &

ssh node4 "cd ~/distributed ; screen -d -m python3 startNode.py 42069" &
ssh node4 "cd ~/distributed ; screen -d -m python3 startNode.py 50100" &