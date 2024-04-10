#Q_2 (Ex-3) 
from mpi4py import MPI
import numpy as np

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Function to generate random numbers between 1 and 50
def generate_random_numbers():
    return np.random.randint(1, 51, size=1000)

# Master process
if rank == 0:
    print("Master process is generating random numbers...")
    master_array = generate_random_numbers()

    even_sum = 0
    odd_sum = 0

    print("Master process is distributing work to slaves...")

    if size > 1:
        # Calculate size of portion for each slave
        portion_size = len(master_array) // (size - 1)
        
        for i in range(1, size):
            start_idx = (i - 1) * portion_size
            end_idx = i * portion_size if i < size - 1 else len(master_array)
            portion = master_array[start_idx:end_idx]
            print(f"Master process is sending data to Slave {i} to compute sum.")
            comm.send(portion, dest=i)
    else:
        print("Only one process available, performing computation locally.")
        even_sum = np.sum(master_array[master_array % 2 == 0])
        odd_sum = np.sum(master_array[master_array % 2 != 0])

    # Combine results from master process
    total_sum = even_sum + odd_sum
    print("Final output:")
    print("Sum of even numbers:", even_sum)
    print("Sum of odd numbers:", odd_sum)
    print("Total sum:", total_sum)

# Slave processes
else:
    print(f"Slave {rank} is computing sum of {'even' if rank % 2 == 0 else 'odd'} numbers.")
    portion = comm.recv(source=0)
    if rank % 2 == 0:
        even_sum = np.sum(portion[portion % 2 == 0])
        comm.send(even_sum, dest=0)
    else:
        odd_sum = np.sum(portion[portion % 2 != 0])
        comm.send(odd_sum, dest=0)

# Finalize MPI
comm.barrier()
MPI.Finalize()
