from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

print(f"Rank {rank} of {size} processes")

if size != 3:
    print("Error: This program requires exactly 3 processes.")
    MPI.Finalize()
    exit()

if rank == 0:
    # Master process reads the list
    input_list = []
    list_length = int(input("Enter the length of the list: "))
    print("Enter the elements of the list:")
    for i in range(list_length):
        element = int(input())
        input_list.append(element)

    print("Master process: List =", input_list)

    # Send the list to process 1
    comm.send(input_list, dest=1)

    # Send the list to process 2
    comm.send(input_list, dest=2)

    # Calculate and print the sum of the list elements
    total_sum = sum(input_list)
    print("Master process: Total sum =", total_sum)

elif rank == 1:
    # Process 1 receives the list from the master
    received_list = comm.recv(source=0)

    # Calculate and print the sum of even elements
    even_sum = sum(num for num in received_list if num % 2 == 0)
    print("Process 1: Sum of even elements =", even_sum)

elif rank == 2:
    # Process 2 receives the list from the master
    received_list = comm.recv(source=0)

    # Calculate and print the sum of odd elements
    odd_sum = sum(num for num in received_list if num % 2 != 0)
    print("Process 2: Sum of odd elements =", odd_sum)

MPI.Finalize()
