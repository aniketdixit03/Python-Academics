#Q_2 (Ex-5)
from mpi4py import MPI
import random

# Initialize MPI
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

# Number of digits in the input (maximum 3 in this case)
num_digits = 3

def get_digit(number, position):
    return (number // (10 ** position)) % 10

def bucket_sort(numbers):
    # Partition numbers into buckets based on their digits
    buckets = [[] for _ in range(10)]
    for num in numbers:
        digit = get_digit(num, rank)
        buckets[digit].append(num)
    
    # Sort each bucket
    sorted_buckets = [sorted(bucket) for bucket in buckets]
    
    # Gather sorted buckets at master process
    all_sorted_buckets = comm.gather(sorted_buckets, root=0)
    
    # Concatenate sorted buckets
    if rank == 0:
        sorted_numbers = []
        for i in range(10):
            for bucket in all_sorted_buckets:
                sorted_numbers.extend(bucket[i])
        return sorted_numbers

if rank == 0:
    # Generate random numbers
    n = 10  # Total numbers
    random_numbers = [random.randint(0, 999) for _ in range(n)]
else:
    random_numbers = None

# Broadcast random numbers to all processes
random_numbers = comm.bcast(random_numbers, root=0)

# Perform bucket sort
sorted_numbers = bucket_sort(random_numbers)

# Output sorted numbers from master process
if rank == 0:
    print("Sorted Numbers:", sorted_numbers)
