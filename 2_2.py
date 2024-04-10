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
    # Master process reads the string
    input_string = input("Enter a string: ")
    print("Master process: String =", input_string)

    # Send the string to process 1 (vowels)
    comm.send(input_string, dest=1)

    # Send the string to process 2 (consonants)
    comm.send(input_string, dest=2)

elif rank == 1:
    # Process 1 (vowels) receives the string from the master
    received_string = comm.recv(source=0)

    # Find and print vowels
    vowels = [char for char in received_string if char.lower() in 'aeiou']
    print("Process 1: Vowels =", ''.join(vowels))

elif rank == 2:
    # Process 2 (consonants) receives the string from the master
    received_string = comm.recv(source=0)

    # Find and print consonants
    consonants = [char for char in received_string if char.lower() not in 'aeiou']
    print("Process 2: Consonants =", ''.join(consonants))

MPI.Finalize()
