'''
Created on 24 Jun 2015

@author: Satish
'''


import socket
import sys
from ctypes.wintypes import MSG


class devicemanager():
    
    def __init__(self):
        self.ipaddress="localhost"
        self.port=2800
        self.server_address=""
        self.sock=socket
        self.result=1
        
    def setup(self,ipaddr,port):
        self.ipaddress=ipaddr     #overwrite default values
        self.port=port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = (self.ipaddress,self.port)
        
    def connect(self):
        
        try:
            self.sock.connect(self.server_address)
        except socket.error as msg:
            self.result=0
            
        return self.result
        
    def sendcommand(self,cmd):
        try:
            self.sock.sendall(cmd)
        except socket.errno as msg:
            print "Data not sent,connection could be down",msg
    def recievedata(self):
        try:
            data = self.sock.recv(1024)
        except socket.error as msg: 
            print "Socket error in read",msg
        return data
         

    

    
    
   