def sort(arr):
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            j = i
            while j >= gap:
                yield (j - gap, j)
                if arr[j - gap] > arr[j]:
                    arr[j - gap], arr[j] = arr[j], arr[j - gap]
                    j -= gap
                else:
                    break
        gap //= 2
