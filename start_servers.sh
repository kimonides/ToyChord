# !/bin/bash
python3 -u startNode.py 42069 > ./logs/"$(date +node0-42069_%F_%H-%M-%S.txt)" &
python3 -u startNode.py 50100 > ./logs/"$(date +node0-50100_%F_%H-%M-%S.txt)" &

ssh -t -t node1 "(cd distributed && python3 startNode.py 42069)" > ./logs/"$(date +node1-42069_%F_%H-%M-%S.txt)" 2>&1 &
ssh -t -t node1 "(cd distributed && python3 startNode.py 50100)" > ./logs/"$(date +node1-50100_%F_%H-%M-%S.txt)" 2>&1 &

ssh -t -t node2 "(cd distributed && python3 startNode.py 42069)" > ./logs/"$(date +node2-42069_%F_%H-%M-%S.txt)" 2>&1 &
ssh -t -t node2 "(cd distributed && python3 startNode.py 50100)" > ./logs/"$(date +node2-50100_%F_%H-%M-%S.txt)" 2>&1 &

ssh -t -t node3 "(cd distributed && python3 startNode.py 42069)" > ./logs/"$(date +node3-42069_%F_%H-%M-%S.txt)" 2>&1 &
ssh -t -t node3 "(cd distributed && python3 startNode.py 50100)" > ./logs/"$(date +node3-50100_%F_%H-%M-%S.txt)" 2>&1 &
 
ssh -t -t node4 "(cd distributed && python3 startNode.py 42069)" > ./logs/"$(date +node4-42069_%F_%H-%M-%S.txt)" 2>&1 &
ssh -t -t node4 "(cd distributed && python3 startNode.py 50100)" > ./logs/"$(date +node4-50100_%F_%H-%M-%S.txt)" 2>&1 &
