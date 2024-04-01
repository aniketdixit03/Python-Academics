from mpi4py import MPI
import numpy as np

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Function to generate random numbers
def generate_random_numbers(n):
    return np.random.randint(1, 101, size=n)

# Master process
if rank == 0:
    n = 1000  # Size of the array
    print("Master process is generating random numbers...")
    master_array = generate_random_numbers(n)
    
    print("Master process is sending data to Slave 1...")
    comm.send(master_array, dest=1)
    
    print("Master process is receiving the sum from Slave 1...")
    slave_sum = comm.recv(source=1)
    
    # Count numbers less than 50 in the array
    count_less_than_50 = np.sum(master_array < 50)
    
    print("Result returned by the slave:", slave_sum)
    print("Count of numbers less than 50 in the array:", count_less_than_50)

# Slave process
elif rank == 1:
    print("Slave process is receiving data from Master...")
    slave_array = comm.recv(source=0)
    
    # Calculate sum of numbers
    slave_sum = np.sum(slave_array)
    
    print("Slave process is sending the sum to Master...")
    comm.send(slave_sum, dest=0)

# Finalize MPI
comm.barrier()
MPI.Finalize()
