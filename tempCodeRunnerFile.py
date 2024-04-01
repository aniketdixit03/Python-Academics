from mpi4py import MPI

# Function to compute factorial of a given number
def factorial(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Number whose factorial is to be computed
n = 6  # Change this to the desired value of n

if size != 2:
    if rank == 0:
        print("This program requires exactly 2 processes.")
    comm.Abort()

# Each process computes its part of the factorial
start = 1 if rank == 0 else n // 2 + 1
end = n // 2 if rank == 0 else n

partial_result = 1
for i in range(start, end + 1):
    partial_result *= i

# Master process combines partial results
total_result = comm.reduce(partial_result, op=MPI.PROD, root=0)

if rank == 0:
    print(f"Factorial of {n} is: {total_result}")

# Finalize MPI
comm.barrier()
MPI.Finalize()
