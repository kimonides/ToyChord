printf "1\n192.168.1.5\n50100" | python3 client.py 192.168.1.5 42069 

printf "1\n192.168.1.1\n42069" | python3 client.py 192.168.1.5 42069 
printf "1\n192.168.1.1\n50100" | python3 client.py 192.168.1.5 42069 

printf "1\n192.168.1.2\n42069" | python3 client.py 192.168.1.5 42069 
printf "1\n192.168.1.2\n50100" | python3 client.py 192.168.1.5 42069 

printf "1\n192.168.1.3\n42069" | python3 client.py 192.168.1.5 42069
printf "1\n192.168.1.3\n50100" | python3 client.py 192.168.1.5 42069

printf "1\n192.168.1.4\n42069" | python3 client.py 192.168.1.5 42069
printf "1\n192.168.1.4\n50100" | python3 client.py 192.168.1.5 42069
