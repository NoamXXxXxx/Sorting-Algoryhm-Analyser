import random


def sort(arr):
    yield from quick(arr, 0, len(arr) - 1)


def quick(arr, lo, hi):
    if lo >= hi:
        return
    r = random.randint(lo, hi)               # random pivot, avoids worst case
    arr[r], arr[hi] = arr[hi], arr[r]
    pivot = arr[hi]
    i = lo
    for j in range(lo, hi):
        yield (j, hi)
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[hi] = arr[hi], arr[i]
    yield (i, hi)
    yield from quick(arr, lo, i - 1)
    yield from quick(arr, i + 1, hi)
