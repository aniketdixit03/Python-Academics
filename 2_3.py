from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if size != 2:
    if rank == 0:
        print("Error: This program requires exactly 2 processes.")
    MPI.Finalize()
    exit()

if rank == 0:
    # Master process
    n = int(input("Enter the size of the array: "))
    array = np.random.randint(0, 100, n)
    print("The array generated is: ")
    for element in array:
        print(element)
    
    # Share the size of the array with the slave
    comm.send(n, dest=1)

    # Share the array with the slave
    comm.Send(array, dest=1)

    # Count numbers less than 50
    count_less_than_50 = np.sum(array < 50)
    print("Master process: Count of numbers less than 50 =", count_less_than_50)

    # Receive the sum from the slave
    total_sum = np.empty(1, dtype='i')
    comm.Recv(total_sum, source=1)
    print("Master process: Sum of numbers calculated by the slave =", total_sum[0])

elif rank == 1:
    # Slave process
    # Receive the size of the array from the master
    n = comm.recv(source=0)

    # Initialize the array
    array = np.empty(n, dtype='i')

    # Receive the array from the master
    comm.Recv(array, source=0)

    # Calculate the sum
    total_sum = np.sum(array)

    # Send the sum back to the master
    comm.Send(total_sum, dest=0)
