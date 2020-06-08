import socket 
import threading
import os
import sys
from _thread import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--host',default='localhost',
                    help='server hostname')
parser.add_argument('--script',default='./scripts.sh',
                    help='script file location')
parser.add_argument('--port',default=9999, type=int,
                    help='server port')
parser.add_argument('--chunksize',default=1, type=int,
                    help='how many scripts to deligate to client at once')

args = parser.parse_args()


### Global Variables ##

no_of_pop_scripts = args.chunksize
total_no_connected = 0
lock = threading.Lock()
script = args.script

### Getting the scripts ready

def get_scripts_ready():
    global list_of_scripts
    list_of_scripts = []
    f = open(script,"r")
    while True:
        line = f.readline()
        if not line: break
        list_of_scripts.append(line.strip())    

def threaded(client_socket, addr): 

    global total_no_connected
    global lock
    print('Connected by :', addr[0], ':', addr[1]) 
    lock.acquire()
    total_no_connected+=1
    lock.release()

    while True: 

        try:

            data = client_socket.recv(1024)

            if not data: 
                print('Disconnected by ' + addr[0],':',addr[1])
                lock.acquire()
                total_no_connected-=1
                print("Total # of remaining processes:", total_no_connected)
                lock.release()

                if total_no_connected==0:
                    print("ALL DONE.")
                    os._exit(0)
                    
                break

            lock.acquire()
            list_of_popped = []
            
            if(data.decode()=="pull"):    
                for i in range(0,no_of_pop_scripts):
                    if len(list_of_scripts)==0:
                        break
                    else:
                        popped = list_of_scripts.pop()
                        list_of_popped.append(popped)
                print(len(list_of_scripts), "scripts remaining in que")
            
            if len(list_of_popped)==0:
                message = b'done'
            else:
                message = str(list_of_popped).encode()
            
            client_socket.send(message) 
        
            lock.release()
        
        except ConnectionResetError as e:
	
            print('Remaining scripts in que:', len(list_of_scripts))
            print('Disconnected by ' + addr[0],':',addr[1])
            lock.acquire()
            total_no_connected-=1
            print("Total # of remaining processes:", total_no_connected)
            lock.release()

            break
             
    client_socket.close() 


## Getting the scripts que ready

get_scripts_ready()

if __name__=="__main__":

    HOST = args.host
    PORT = args.port

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT)) 
    server_socket.listen() 

    print('Serial2Parallel Server v0.1 by Matt Lee')
    print()
    print("To see how to use: python server.py --help")
    print('Please add lines in ',script)    
    print(len(list_of_scripts), "scripts ready in que")
    print("--------------------------------------------")
    print('Waiting for client request ..')
    
    while True: 

        client_socket, addr = server_socket.accept() 
        start_new_thread(threaded, (client_socket, addr)) 

    server_socket.close() 
