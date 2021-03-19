from remote import Remote
from server import Server

import hashlib
from uuid import uuid4
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

masterIP = '192.168.1.5'
masterPort = 42069

ringSize = int(config['DEFAULT']['ringSize'])
k = int(config['DEFAULT']['k'])


class Node:
    def __init__(self, ip, port) -> None:
        print('K is %s' % k)
        self.ip = ip
        self.port = int(port)
        self.id = self.hash('%s:%s' % (self.ip,self.port))
        self.next = self
        self.previous = self
        self.connection = None
        self.data = {}

    def start(self):
        self.server = Server(self.ip,self.port, self)

    def send(self,request,targetNode):
        requestID = None
        if 'requestID' not in request:
            requestID = uuid4()
            request['requestID'] = str(requestID)
        print('Sending %s to %s:%s' % (repr(request),targetNode.ip,targetNode.port))
        targetNode.connection.send(json.dumps(request))
        return requestID
    def sendResponse(self,request,response):
        responseNodeIP = request['responseNodeIP']
        responseNodePort = int(request['responseNodePort'])
        if(self.ip == responseNodeIP and self.port == responseNodePort and 'requestID' not in request):
            return response
        try:
            requestID = request['requestID']
        except:
            return None
        conn = Remote(responseNodeIP,responseNodePort)
        res = json.dumps({'type':'response','requestID':requestID,'response':response})
        conn.send(res)
        return None

    def hash(self,key):
        return int(hashlib.sha1((key).encode()).hexdigest(), 16) % ringSize

    def redistribute(self,request) -> None:
        key = request['redistribute']['key']
        value = request['redistribute']['value']
        ownerID = request['redistribute']['ownerID']
        replicaCount = int(request['redistribute']['replicaCount'])
        self.data[key] = {'value':value,'replicaCount': k-replicaCount,'ownerID':ownerID }
        request['redistribute']['replicaCount'] = replicaCount + 1
        if( self.next.id != ownerID and request['redistribute']['replicaCount'] == k):
            print('Sending %s to %s' % (repr(request),self.next.ip))
            self.next.connection.send(json.dumps(request))

    def insert(self, request):
        key = request['insert']['key']
        hash_key = self.hash(key)
        value = request['insert']['value']
        replicaCount = int(request['insert']['replicaCount'])
        if(self.isResponsible(hash_key) or replicaCount > 0):
            self.data[key] = {'value':value,'replicaCount': replicaCount }
            if(self.isResponsible(hash_key)):
                print("I'm responsible for insert with hash key %s and value %s" % (hash_key,value))
                request['insert']['ownerID']=self.id
            else:
                print("I'm replica number %s for hash key %s" % (replicaCount,hash_key))
            self.data[key]['ownerID']=int(request['insert']['ownerID'])
            request['insert']['replicaCount'] = replicaCount + 1
            if( request['insert']['replicaCount'] == k or self.data[key]['ownerID'] == self.next.id):
                return self.sendResponse(request,'Finished adding all replicas\n')
            else:
                self.send(request,self.next)
        else:
            print("I'm not responsible for id %s send to previous with ip %s" % (hash_key,self.previous.ip))
            return self.send(request,self.previous)

    def delete(self,request):
        key = request['delete']['key']
        if( key in self.data ):
            v = self.data.pop(key)
            self.sendResponse(request,'OK')
            if v['replicaCount'] == k-1 or self.isNextNodeTerminal(request) :
                self.sendResponse(request,'OK')
            else:
                self.send(request,self.next)
        else:
            return self.send(request,self.next)

    def isResponsible(self, hash) -> bool:
        hash = int(hash)
        rv = False
        if(self.next is self):
            return True
        if(self.id < self.previous.id):
            if(0 <= hash <= self.id or self.previous.id < hash < ringSize):
                rv = True
        else:
            if(self.previous.id < hash <= self.id):
                rv = True
        return rv

    def redistributeData(self, targetNode, force=False) -> None:
        print('Redistributing data to %s with id %s' % (targetNode.ip,targetNode.id))
        for key in list(self.data):
            if(not self.isResponsible(key) or force == True):
                data = self.data.pop(key)
                value = data['value']
                replicaCount = data['replicaCount']
                ownerID = data['ownerID']
                if(ownerID != targetNode.id):
                    ownerID = targetNode.id if not self.isResponsible(key) else ownerID
                    print('Sending key hash %s to %s' % (key,targetNode.ip))
                    targetNode.connection.send(json.dumps({'type':'redistribute','redistribute':{'key':key,'value':value,'replicaCount':replicaCount,'ownerID':ownerID}}))

    def depart(self, request):
        if(request['depart']['id'] == self.id):
            msg = json.dumps({ 'type':'next','ip':self.next.ip,'port':self.next.port })
            self.previous.connection.send(msg)
            msg = json.dumps({ 'type':'prev','ip':self.previous.ip,'port':self.previous.port })
            self.next.connection.send(msg)
            self.redistributeData(self.next,force=True)
            return self.sendResponse(request,'OK')
        else:
            return self.send(request,self.next)

    def isNextNodeTerminal(self,request):
        return self.next.ip == request['responseNodeIP'] and self.next.port == int(request['responseNodePort'])

    def query(self,request):
        key = request['query']['key']
        hash_key = self.hash(key)
        if(key == '*'):
            for kk,v in self.data.items():
                if v['replicaCount'] == 0 :
                    if('response' in request):
                        request['response'] += ', %s:%s' % (kk,v['value'])
                    else:
                        request['response'] = '%s:%s' % (kk,v['value'])
            if(self.isNextNodeTerminal(request)):
                response = request['response']
                return self.sendResponse(request,response)
            else:
                return self.send(request,self.next)
        elif(key in self.data and (self.data[key]['replicaCount'] == k-1 or self.isNextNodeTerminal(request))):
            resp = 'Query result is %s from %s:%s with id %s' % (self.data[key],self.ip,self.port,self.id)
            return self.sendResponse(request,resp)
        elif(self.isResponsible(hash_key) and key not in self.data):
            return self.sendResponse(request,"Key %s doesn't exist in the DHT" % key)
        else:
            return self.send(request,self.next)

    def join(self, request):
        ip = request['join']['ip']
        port = request['join']['port']
        joinID = self.hash('%s:%s' % (ip,port))
        if(self.isResponsible(joinID)):
            oldPrevIP = self.previous.ip
            oldPrevPort = self.previous.port
            if(self.previous is self):
                self.setNext(ip, port)
            else:
                self.previous.connection.send(json.dumps({ 'type':'next','ip':ip,'port':port }))
            self.setPrevious(ip, port)
            self.previous.connection.send(json.dumps({ 'type':'prev','ip':oldPrevIP,'port':oldPrevPort }))
            self.previous.connection.send(json.dumps({ 'type':'next','ip':self.ip,'port':self.port }))

            self.redistributeData(self.previous)
            return self.sendResponse(request,'OK')
        else:
            return self.send(request,self.next)

    def setNext(self, ip, port) -> None:
        if(ip==self.ip and int(port)==self.port):
            self.next = self
        else:
            self.next = Node(ip, port)
            self.next.connection = Remote(self.next.ip, self.next.port)
        print('Added %s:%s as next' % (ip,port))

    def setPrevious(self, ip, port) -> None:
        if(ip==self.ip and int(port)==self.port):
            self.previous = self
        else:
            self.previous = Node(ip, port)
            self.previous.connection = Remote(self.previous.ip, self.previous.port)
        print('Added %s:%s as previous' % (ip,port))

    def __str__(self) -> None:
        return "(%s,%s,%s)-->" % (self.ip, self.port, self.id)

    def ping(self,request) -> None:
        if('response' in request):
            request['response'] += str(self)
        else:
            request['response'] = str(self)
        if(self.isNextNodeTerminal(request)):
            response = request['response']
            return self.sendResponse(request,response)
        return self.send(request,self.next)

# TODO CHANGE IS RESPONSIBLE TO TAKE KEY NOT HASH KEY