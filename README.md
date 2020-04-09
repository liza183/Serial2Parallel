# Serial2Parallel
serial2parallel: Running serial scripts/binary parallel on a MPI cluster

# How to use
- You need to edit `scripts/scripts.txt` and add lines. Each line will be distributed across multiple nodes.
- You need to run server.py first
- You may need to recompile `mpiexec`
- You need to run `mpiexec` using `mpirun`

# Things I need to do before the release
- Can I replace mpiexec with pympi
- I need better documentation
- I need an example
