#Q_2 (Ex-5)
from mpi4py import MPI

def bucket_sort(numbers):
    buckets = [[] for _ in range(10)]  # 10 buckets for digits 0-9

    # Distribute numbers into buckets based on first digit
    for num in numbers:
        first_digit = num // 100 if num >= 100 else num // 10
        buckets[first_digit].append(num)

    # Sort each bucket
    for i in range(len(buckets)):
        buckets[i].sort()

    return buckets

def merge_sorted_buckets(sorted_buckets):
    return [num for bucket in sorted_buckets for num in bucket]

if __name__ == "__main__":
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    if rank == 0:
        n = int(input("Enter the number of elements: "))
        numbers = [int(input(f"Enter number {i+1}: ")) for i in range(n)]
    else:
        numbers = None

    # Broadcast numbers to all processes
    numbers = comm.bcast(numbers, root=0)

    # Divide numbers into buckets
    local_bucket_size = len(numbers) // size
    local_numbers = numbers[rank * local_bucket_size : (rank + 1) * local_bucket_size]

    # Perform bucket sort locally
    local_sorted_buckets = bucket_sort(local_numbers)

    # Gather all sorted buckets at the master process
    all_sorted_buckets = comm.gather(local_sorted_buckets, root=0)

    if rank == 0:
        # Merge sorted buckets to get final sorted list
        sorted_numbers = merge_sorted_buckets(all_sorted_buckets)
        print("Sorted numbers:", sorted_numbers)
