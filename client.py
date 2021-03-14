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


socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((responseIP,responsePort))

# print('1)Join')
# print('2)Depart')
# print('3)Insert')
# print('4)Delete')
# print('5)Query')
# print('6)Ping')
# cmd = input('Input the number of the command you with to run:')
cmd = input()

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
    key_hash = hash(key)
    msg['type'] = 'insert'
    msg['insert'] = {
        'key':key_hash,
        'value':value,
        'replicaCount':0
    }
elif(cmd=='4' or cmd=='delete'):
    key = input('Key:')
    key_hash = hash(key)
    msg['type'] = 'delete'
    msg['delete'] = {
        'key':key_hash
    }
elif(cmd=='5' or cmd=='query'):
    key = input('Key:')
    if(key != '*'):
        key = hash(key)
    msg['type'] = 'query'
    msg['query'] = {
        'key':key
    }
elif(cmd=='6' or cmd=='ping'):
    msg['type'] = 'ping'
else:
    exit(-1)

msg['responseNodeIP'] = responseIP
msg['responseNodePort'] = str(responsePort)
msg = json.dumps(msg)

print(repr('Sending %s' % msg))
socket.sendall(msg.encode())
print('Received %s' % socket.recv(1023).decode())




