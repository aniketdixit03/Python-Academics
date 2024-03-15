from mpi4py import MPI
import numpy as np

ARRAY_SIZE = 1000

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Master process
if rank == 0:
    master_array = np.empty(ARRAY_SIZE, dtype=int)

    # Receive data from each slave and gather them in master_array
    for i in range(1, size):
        temp_array = np.empty(ARRAY_SIZE // (size - 1), dtype=int)
        comm.Recv(temp_array, source=i, tag=0)

        # Copy temp_array to master_array
        offset = (i - 1) * (ARRAY_SIZE // (size - 1))
        master_array[offset: offset + len(temp_array)] = temp_array

    # Count multiples of 5
    count_multiples_of_5 = np.sum(master_array % 5 == 0)
    print(f"Master Process: Count of multiples of 5 = {count_multiples_of_5}")

# Slave processes
else:
    # Generate local array of random numbers
    local_array = np.random.randint(1, 1001, size=ARRAY_SIZE // (size - 1))

    # Send local array to the master
    comm.Send(local_array, dest=0, tag=0)

# Ensure all processes have finished
comm.Barrier()
