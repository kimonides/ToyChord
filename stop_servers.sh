killall -9 python3 > /dev/null
ssh node1 "killall -s SIGINT python3 > /dev/null"
ssh node2 "killall -s SIGINT python3 > /dev/null"
ssh node3 "killall -s SIGINT python3 > /dev/null"
ssh node4 "killall -s SIGINT python3 > /dev/null" 
rm ./logs/*