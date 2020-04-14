# Serial2Parallel
serial2parallel: Running any serial scripts in parallel on a MPI cluster!

# How to use
- You need to edit `scripts/scripts.txt` and add lines. Each line will be distributed and run across multiple nodes.
- You need to run server.py first. The server manages the script pool and handles requests from clients.

```
$ python server.py --host localhost --port 9999 --chunksize 1
Serial2Parallel Server v0.1 by Matt Lee

Please add lines in scripts/scripts.txt
126 scripts ready in que
--------------------------------------------
Waiting for client request ..
```

- `chunksize` means the number of scripts that are assigned to a client at once, and the default value is 1.
- `host` is for the server's hostname. The default value is `localhost`
- `port` is for the server's port number. The default value is 9999.

- Now you can run the scripts using `mpiexec` by doing
```
$ mpiexec -n 4 python s2p.py --host localhost --port 9999
MPI client started running scripts in parallel: this process is rank = 3, total # of processes: 4
1 / 1  rank =  3   5.005801200866699  sec elapsed to process a script
MPI client started running scripts in parallel: this process is rank = 0, total # of processes: 4
1 / 1  rank =  0   5.005622148513794  sec elapsed to process a script
MPI client started running scripts in parallel: this process is rank = 1, total # of processes: 4
1 / 1  rank =  1   5.005718946456909  sec elapsed to process a script
MPI client started running scripts in parallel: this process is rank = 2, total # of processes: 4
1 / 1  rank =  2   5.005543231964111  sec elapsed to process a script
1 / 1  rank =  2   5.008765935897827  sec elapsed to process a script
1 / 1  rank =  3   5.008672714233398  sec elapsed to process a script
1 / 1  rank =  0   5.009006977081299  sec elapsed to process a script
1 / 1  rank =  1   5.008861303329468  sec elapsed to process a script```
...
```
- Enjoy!

# Note
- This software is for running many jobs in parallel (embarrassingly parallel) on many nodes, 
not for running a single big job on many nades (this will require a magic!)

# License
Please contact the developer, Matt Lee (lees4@ornl.gov) for more details.
