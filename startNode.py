#!/usr/bin/env python3
import socket
import fcntl
import struct
import sys
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

use_eventual = int(config['DEFAULT']['use_eventual'])

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', bytes(ifname[:15], 'utf-8'))
    )[20:24])

if __name__ == "__main__":
    if(use_eventual):
        from node_eventual_consistency import Node
        print('Using eventual consistency')
    else:
        from node import Node
        print('Using chain replication')
    ip = get_ip_address('eth1')
    port = int(sys.argv[1])
    print('My ip is %s' % ip)
    node = Node(ip,port)
    node.start()