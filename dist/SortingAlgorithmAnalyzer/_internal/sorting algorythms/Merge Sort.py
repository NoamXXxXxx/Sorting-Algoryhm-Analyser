def sort(arr):
    yield from merge_sort(arr, 0, len(arr))


def merge_sort(arr, lo, hi):
    if hi - lo < 2:
        return
    mid = (lo + hi) // 2
    yield from merge_sort(arr, lo, mid)
    yield from merge_sort(arr, mid, hi)
    yield from merge(arr, lo, mid, hi)


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
