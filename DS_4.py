#Q_3 (Ex-3)
from mpi4py import MPI
import random

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Check if there are an even number of processes
if size % 2 != 0:
    if rank == 0:
        print("Error: The number of processes must be even.")
    MPI.Finalize()
    exit()

# Determine partner rank
partner_rank = size - rank - 1

# Generate a random number if odd process
if rank % 2 != 0:
    random_number = random.randint(1, 100)
    print(f"Process {rank} sending {random_number} to Process {partner_rank}")
    comm.send(random_number, dest=partner_rank)
    received_number = comm.recv(source=partner_rank)
    print(f"Process {rank} received {received_number} from Process {partner_rank}")
else:  # Even process
    received_number = comm.recv(source=partner_rank)
    squared_number = received_number ** 2
    print(f"Process {rank} received {received_number} from Process {partner_rank} and sending {squared_number} back")
    comm.send(squared_number, dest=partner_rank)
