def sort(arr):
    n = len(arr)
    for i in range(n - 1):
        smallest = i
        for j in range(i + 1, n):
            yield (smallest, j)
            if arr[j] < arr[smallest]:
                smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]
        yield (i, smallest)
