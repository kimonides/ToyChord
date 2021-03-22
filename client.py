import socket
import hashlib
import json
import configparser
import sys

config = configparser.ConfigParser()
config.read('config.ini')

ringSize = int(config['DEFAULT']['ringSize'])
k = config['DEFAULT']['k']

def hash(key):
    return int(hashlib.sha1((key).encode()).hexdigest(), 16) % ringSize


responseIP = sys.argv[1]
responsePort = int(sys.argv[2])


print('1)Join')
print('2)Depart')
print('3)Insert')
print('4)Delete')
print('5)Query')
print('6)Ping')
print('7)Help')
cmd = input('Input the number of the command you with to run:')
# cmd = input()

msg = {}

if(cmd=='1' or cmd=='join'):
    ip = input('IP:')
    port = input('Port:')
    msg['type'] = 'join'
    msg['join'] = {
        'ip':ip,
        'port':port
    }
elif(cmd=='2' or cmd=='depart'):
    msg['type'] = 'depart'
    id = input('ID:')
    msg['depart'] = {
        'id':id
    }
elif(cmd=='3' or cmd=='insert'):
    key = input('Key:')
    value = input('Value:')
    # key_hash = hash(key)
    msg['type'] = 'insert'
    msg['insert'] = {
        'key':key,
        'value':value,
        'replicaCount':0
    }
elif(cmd=='4' or cmd=='delete'):
    key = input('Key:')
    # key_hash = hash(key)
    msg['type'] = 'delete'
    msg['delete'] = {
        'key':key
    }
elif(cmd=='5' or cmd=='query'):
    key = input('Key:')
    msg['type'] = 'query'
    msg['query'] = {
        'key':key
    }
elif(cmd=='6' or cmd=='ping' or cmd=='overlay'):
    msg['type'] = 'ping'
elif(cmd=='7' or cmd=='help'):
    print(" -------------------------------------------------------------------------- ")
    print("|   This is a client able to send requests to the distributed hash table  |")
    print("|                                                                         |")
    print('|        join    Inserts a new node into the DHT                          |')
    print('|                Data will be redistributed as needed to the new node     |')
    print('|        depart  Removes a node from the DHT                              |')
    print("|                Finds the node by ID and redistributed it's data         |")
    print('|        insert  Inserts a new key value pair into the DHT                |')
    print("|                The system finds the key's id by it's hash and           |")
    print('|                determines the responsible node                          |')
    print('|        delete  Deletes a key from the DHT                               |')
    print("|                The system finds the key's id by it's hash and           |")
    print('|                deletes the key and any replica of it                    |')
    print("|        query   Find's the value of a key in the DHT                     |")
    print("|                The system finds the key's id by it's hash and           |")
    print("|                finds the key's value in the system                      |")
    print("|        overlay Prints the DHT's topology                                |")
    print("|        help    I wonder what help does                                  |")
    print("---------------------------------------------------------------------------")
    exit(0)
else:
    exit(-1)

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((responseIP,responsePort))

msg['responseNodeIP'] = responseIP
msg['responseNodePort'] = str(responsePort)
msg = json.dumps(msg)

print(repr('Sending %s' % msg))
socket.sendall(msg.encode())
print('Received %s' % socket.recv(999999999).decode())




