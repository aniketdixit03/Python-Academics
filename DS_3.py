from mpi4py import MPI
import numpy as np

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Function to generate random numbers between 1 and 1000
def generate_random_numbers(n):
    return np.random.randint(1, 1001, size=n)

# Master process
if rank == 0:
    x = 1000  # Size of the array held by the master process
    total_count = 0
    master_array = np.empty(x, dtype=int)

    # Receive data from each slave process and gather in master array
    for i in range(1, size):
        slave_array = np.empty(x // size, dtype=int)
        comm.Recv(slave_array, source=i)
        master_array[(i - 1) * (x // size):i * (x // size)] = slave_array

    # Count multiples of 5 in the master array
    total_count += np.sum(master_array % 5 == 0)

    # Print the count of elements which are multiples of 5
    print("Total count of elements which are multiples of 5:", total_count)

# Slave processes
else:
    n = x // size
    slave_array = generate_random_numbers(n)
    comm.Send(slave_array, dest=0)

# Finalize MPI
comm.barrier()
MPI.Finalize()
