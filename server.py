import socket 
import threading
import os
import sys
from _thread import *
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--host',default='localhost',
                    help='server hostname')
parser.add_argument('--port',default=9999,
                    help='server port')
parser.add_argument('--chunksize',default=1, type=int,
                    help='how many scripts to deligate to client at once')

args = parser.parse_args()


### Global Variables ##

no_of_pop_scripts = args.chunksize
total_no_connected = 0
lock = threading.Lock()

### Getting the scripts ready

def get_scripts_ready():
    global list_of_scripts
    list_of_scripts = []
    f = open("scripts/scripts.txt","r")
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

    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data: 
                print('Remaining scripts in que:', len(list_of_scripts))
                print('Disconnected by ' + addr[0],':',addr[1])
                lock.acquire()
                total_no_connected-=1
                print("Total # of remaining processes:", total_no_connected)
                lock.release()

                if total_no_connected==0:
                    print("ALL DONE.")
                    os._exit(0)
                    
                break

            #print('Received from ' + addr[0],':',addr[1] , data.decode())
            lock.acquire() # will block if lock is already held
                
            list_of_popped = []
            
            if(data.decode()=="pull"):    
                for i in range(0,no_of_pop_scripts):
                    if len(list_of_scripts)==0:
                        break
                    else:
                        popped = list_of_scripts.pop()
                        list_of_popped.append(popped)
                print(len(list_of_scripts), "scripts remaining in que")
                #print(list_of_popped)
            
            #client_socket.send(data) 
            if len(list_of_popped)==0:
                message = b'done'
            else:
                message = str(list_of_popped).encode()
            
            client_socket.send(message) 
        
            lock.release()
        except SystemExit as e:
            sys.exit()

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
    print('Waiting for client request ..')
    print()
    print('Please add lines in scripts/scripts.txt')    
    print(len(list_of_scripts), "scripts ready in que")
    print("--------------------------------------------")

    # 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

    # 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
    while True: 

        client_socket, addr = server_socket.accept() 
        start_new_thread(threaded, (client_socket, addr)) 

    server_socket.close() 
