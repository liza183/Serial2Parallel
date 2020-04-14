from mpi4py import MPI
import socket 
import threading
import os
from _thread import *
import sys
import ast
import time
import argparse

total_processed = 0
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

parser = argparse.ArgumentParser()
parser.add_argument('--host',default='localhost',
                    help='server hostname')
parser.add_argument('--port',default=9999,
                    help='server port')
args = parser.parse_args()
HOST = args.host
PORT = args.port

# 쓰레드에서 실행되는 코드입니다. 
total_no_connected = 0
list_of_tasks = []

def do_something(script, rank):
    os.system(script)

def do_works(data, rank):
    global total_processed
    global comm
    idx = 1
    for script in data:
        #print("rank=", rank, " processing '", script.strip(), "' started")
        start_time = time.time()

        do_something(script, rank)
                
        elapsed_time = time.time() - start_time    
        
        print(idx,"/",len(data), " rank = ", rank, " ", elapsed_time, " sec elapsed to process a script", flush=True)
        total_processed+=1
        idx+=1 


print("MPI client started running scripts in parallel: this process is rank = {}, total # of processes: {}".format(rank, size));

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
client_socket.connect((HOST, PORT)) 

while True: 

    message = 'pull'
    #print('rank=', rank, ' Sending to the server :',message) 
    client_socket.send(message.encode()) 
    data = client_socket.recv(1024) 

    decoded_data = data.decode()
    if decoded_data == "done":
        print("All scripts assigned for rank",rank," have been done")
        break
    try:
        decoded_data = ast.literal_eval(decoded_data)
        #print('rank=',rank,' Received from the server :', len(decoded_data), "scripts") 
        #time.sleep(1)
        do_works(decoded_data, rank)
    except:
         print(decoded_data, "couldn't be parsed.")

client_socket.close() 
sys.exit()
