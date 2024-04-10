#Q_3 (Ex-3) 
from mpi4py import MPI
import random  # Import the random module

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size % 2 != 0:
    print("Error: Even number of processes required!")
    comm.Abort()

partner_rank = (rank + size // 2) % size

if rank % 2 == 1:
    # Odd process: send random number first
    data = random.randint(1, 100)
    comm.Send(data, partner_rank)
    print(f"Process {rank} sent {data} to process {partner_rank}")
    # Now receive the result from the partner
    received_result = comm.Recv(source=partner_rank)
    print(f"Process {rank} received final result: {received_result}")
else:
    # Even process: receive number, calculate square, and send back
    data = comm.Recv(source=partner_rank)
    result = data * data
    comm.Send(result, partner_rank)
    print(f"Process {rank} received {data} and sent back square {result}")
    # Now receive the final result from the partner
    received_result = comm.Recv(source=partner_rank)
    print(f"Process {rank} received final result: {received_result}")

# Both processes receive the final message (their partner's result)

MPI.Finalize()
