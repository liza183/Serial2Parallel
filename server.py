import socket 
import threading
import os

def get_jobs_ready():
    global list_of_jobs
    list_of_jobs = []
    f = open("scripts/scripts.txt","r")
    while True:
        line = f.readline()
        if not line: break
        list_of_jobs.append(line.strip())    

from _thread import *

no_of_pop_jobs = 1
global list_of_jobs
get_jobs_ready()
#list_of_jobs = list_of_jobs[:10]
print(len(list_of_jobs), "scripts ready in que")

# 쓰레드에서 실행되는 코드입니다. 
global total_no_connected
total_no_connected = 0

# 접속한 클라이언트마다 새로운 쓰레드가 생성되어 통신을 하게 됩니다. 
def threaded(client_socket, addr): 

    global total_no_connected
    print('Connected by :', addr[0], ':', addr[1]) 
    lock = threading.Lock()
    lock.acquire()
    total_no_connected+=1
    lock.release()

    # 클라이언트가 접속을 끊을 때 까지 반복합니다. 
    while True: 

        try:

            # 데이터가 수신되면 클라이언트에 다시 전송합니다.(에코)
            data = client_socket.recv(1024)

            if not data: 
                print('Remaining jobs in que:', len(list_of_jobs))
                print('Disconnected by ' + addr[0],':',addr[1])
                lock = threading.Lock()
                lock.acquire()
                total_no_connected-=1
                print("Total # of remaining processes:", total_no_connected)
                lock.release()
                break

            print('Received from ' + addr[0],':',addr[1] , data.decode())
            lock = threading.Lock()
            lock.acquire() # will block if lock is already held
                
            list_of_popped = []
            
            if(data.decode()=="pull"):    
                print("pop jobs from list_of_jobs")

                for i in range(0,no_of_pop_jobs):
                    if len(list_of_jobs)==0:
                        break
                    else:
                        popped = list_of_jobs.pop()
                        list_of_popped.append(popped)
                print(len(list_of_jobs), "jobs remaining in que")
                #print(list_of_popped)
            
            #client_socket.send(data) 
            if len(list_of_popped)==0:
                message = b'done'
            else:
                message = str(list_of_popped).encode()
            
            client_socket.send(message) 
        
            lock.release()

        except ConnectionResetError as e:
	
            print('Remaining jobs in que:', len(list_of_jobs))
            print('Disconnected by ' + addr[0],':',addr[1])
            lock = threading.Lock()
            lock.acquire()
            total_no_connected-=1
            print("Total # of remaining processes:", total_no_connected)
            lock.release()

            break
             
    client_socket.close() 


HOST = 'localhost'
PORT = 9999

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT)) 
server_socket.listen() 

print('Scripts pool server v. 0.0.1 by Matt Lee')


# 클라이언트가 접속하면 accept 함수에서 새로운 소켓을 리턴합니다.

# 새로운 쓰레드에서 해당 소켓을 사용하여 통신을 하게 됩니다. 
while True: 

    print('Waiting for request ..')
    client_socket, addr = server_socket.accept() 
    start_new_thread(threaded, (client_socket, addr)) 

server_socket.close() 
