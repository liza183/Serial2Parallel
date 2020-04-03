import os
import socket 
import time
import ast
import sys

HOST = 'localhost'
PORT = 9999

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 

client_socket.connect((HOST, PORT)) 

def do_something(job, rank):
    os.system(job)
global total_processed
total_processed = 0

def do_works(data, rank):
    global total_processed
    idx = 1
    for job in data:
        print("rank=", rank, " processing '", job.strip(), "' started")
        start_time = time.time()

        do_something(job, rank)
                
        elapsed_time = time.time() - start_time
        print(idx,"/",len(data), " rank = ", rank, " ", elapsed_time, " sec elapsed to process", job.strip(), total_processed)
        total_processed+=1
        idx+=1 

rank = int(sys.argv[1])

while True: 

    message = 'pull'
    #print('rank=', rank, ' Sending to the server :',message) 
    client_socket.send(message.encode()) 
    data = client_socket.recv(1024) 

    decoded_data = data.decode()
    if decoded_data == "done":
        print(rank, " All scripts are done")
        break
    try:
        decoded_data = ast.literal_eval(decoded_data)
    
        print('rank=',rank,' Received from the server :', len(decoded_data), "jobs") 
        time.sleep(1)

        do_works(decoded_data, rank)
    except:
         print(decoded_data, "couldn't be parsed.")

client_socket.close() 
sys.exit()
