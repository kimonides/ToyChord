cd ..

printf "1\n192.168.1.5\n50100" | python3 client.py 192.168.1.5 42069 > /dev/null

printf "1\n192.168.1.1\n42069" | python3 client.py 192.168.1.5 42069 > /dev/null
printf "1\n192.168.1.1\n50100" | python3 client.py 192.168.1.5 42069 > /dev/null

printf "1\n192.168.1.2\n42069" | python3 client.py 192.168.1.5 42069 > /dev/null
printf "1\n192.168.1.2\n50100" | python3 client.py 192.168.1.5 42069 > /dev/null

printf "1\n192.168.1.3\n42069" | python3 client.py 192.168.1.5 42069 > /dev/null
printf "1\n192.168.1.3\n50100" | python3 client.py 192.168.1.5 42069 > /dev/null

printf "1\n192.168.1.4\n42069" | python3 client.py 192.168.1.5 42069 > /dev/null
printf "1\n192.168.1.4\n50100" | python3 client.py 192.168.1.5 42069 > /dev/null


# declare -a VMs=(
#     "192.168.1.1 42069"
#     "192.168.1.1 50100"
#     "192.168.1.2 42069"
#     "192.168.1.2 50100"
#     "192.168.1.3 42069"
#     "192.168.1.3 50100"
#     "192.168.1.4 42069"
#     "192.168.1.4 50100"
#     "192.168.1.5 50100"
# )


# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.1", "port": "42069"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069
# sleep 1
# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.1", "port": "50100"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069 

# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.2", "port": "42069"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069
# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.2", "port": "50100"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069 

# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.3", "port": "42069"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069
# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.3", "port": "50100"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069 

# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.4", "port": "42069"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069
# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.5", "port": "50100"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069 

# echo '{"responseNodePort": "42069", "join": {"ip": "192.168.1.5", "port": "50100"}, "type": "join", "responseNodeIP": "192.168.1.5"}'\
# | nc 192.168.1.5 42069







