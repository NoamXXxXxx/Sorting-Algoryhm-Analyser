# Simplified Timsort: insertion sort on small runs, then merge the runs.
MIN_RUN = 32


def sort(arr):
    n = len(arr)
    for start in range(0, n, MIN_RUN):
        yield from insertion(arr, start, min(start + MIN_RUN, n))
    size = MIN_RUN
    while size < n:
        for lo in range(0, n, 2 * size):
            mid = lo + size
            hi = min(lo + 2 * size, n)
            if mid < hi:
                yield from merge(arr, lo, mid, hi)
        size *= 2


def insertion(arr, lo, hi):
    for i in range(lo + 1, hi):
        j = i
        while j > lo:
            yield (j - 1, j)
            if arr[j - 1] > arr[j]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
                j -= 1
            else:
                break


def merge(arr, lo, mid, hi):
    left = arr[lo:mid]
    right = arr[mid:hi]
    i = j = 0
    k = lo
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            arr[k] = left[i]
            i += 1
        else:
            arr[k] = right[j]
            j += 1
        yield (k,)
        k += 1
    while i < len(left):
        arr[k] = left[i]
        i += 1
        yield (k,)
        k += 1
    while j < len(right):
        arr[k] = right[j]
        j += 1
        yield (k,)
        k += 1
