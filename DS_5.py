#Q_5 (Ex-5)
from mpi4py import MPI

def main():
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        n = int(input("Enter the number of elements: "))
        numbers = [int(input(f"Enter number {i+1}: ")) for i in range(n)]
    else:
        numbers = None

    numbers = comm.bcast(numbers, root=0)

    local_n = len(numbers) // size
    local_numbers = numbers[rank * local_n: (rank + 1) * local_n]

    partial_sum = sum(local_numbers)

    for i in range(1, size):
        if rank % (2**i) == 0:
            data = comm.recv(source=rank + 2**(i-1))
            partial_sum += data
        elif rank % (2**i) == 2**(i-1):
            dest = rank - 2**(i-1)
            comm.send(partial_sum, dest=dest)

    if rank == 0:
        print("Final sum:", partial_sum)

if __name__ == "__main__":
    main()
