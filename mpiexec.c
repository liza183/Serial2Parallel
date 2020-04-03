#include <mpi.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char** argv) {
    MPI_Init(NULL, NULL);
    int rank;
    int size;
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    
    printf("MPI task executed: rank %d, size: %d\n", rank, size);
   
    char command[50];

    sprintf(command, "./run.sh %d %d", rank, size); 

    system(command);

    MPI_Finalize();
}
